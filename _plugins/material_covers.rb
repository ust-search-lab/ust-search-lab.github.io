require 'digest'
require 'fileutils'
require 'timeout'
require 'uri'

module Jekyll
  # Render uploaded PDFs locally. External documents are never fetched at build time.
  class MaterialCovers
    def initialize(site)
      @site = site
      @source = File.realpath(site.source)
      @cache = File.join(site.source, '.jekyll-cache', 'material-covers')
      @results = {}
    end

    def for_item(item)
      %w[ko en].to_h do |lang|
        url = lang == 'en' && !item['url_en'].to_s.empty? ? item['url_en'] : item['url']
        cover = item['cover'].to_s.empty? ? from_pdf(url) : item['cover']
        [lang, cover]
      end
    end

    private

    def from_pdf(url)
      return @results[url] if @results.key?(url)
      @results[url] = nil
      return unless url.start_with?('/') && !url.start_with?('//')
      path = URI::DEFAULT_PARSER.unescape(url.split(/[?#]/, 2).first)
      return unless File.extname(path).downcase == '.pdf'
      path = File.realpath(File.join(@source, path.delete_prefix('/')))
      return unless path.start_with?(@source + '/')

      # A content hash also invalidates browser caches when the PDF is replaced.
      key = Digest::SHA256.hexdigest("first-page-700-jpeg85-v1:#{Digest::SHA256.file(path).hexdigest}")
      relative = "images/material-covers/#{key}.jpg"
      output = File.join(@cache, relative)
      unless File.size?(output)
        FileUtils.mkdir_p(File.dirname(output))
        render(path, output.delete_suffix('.jpg'))
      end
      return unless File.size?(output)

      unless @results.value?("/#{relative}")
        @site.static_files << StaticFile.new(@site, @cache, File.dirname(relative), File.basename(relative))
      end
      @results[url] = "/#{relative}"
    rescue SystemCallError, Timeout::Error => error
      FileUtils.rm_f(output) if output
      Jekyll.logger.warn('Material cover:', "#{File.basename(path.to_s)} (#{error.class}); using a file icon")
      nil
    end

    def render(path, prefix)
      pid = Process.spawn('pdftoppm', '-f', '1', '-l', '1', '-singlefile', '-scale-to', '700',
                          '-jpeg', '-jpegopt', 'quality=85', path, prefix,
                          out: File::NULL, err: File::NULL)
      _, status = Timeout.timeout(20) { Process.wait2(pid) }
      return if status.success?

      FileUtils.rm_f("#{prefix}.jpg")
      Jekyll.logger.warn('Material cover:', "#{File.basename(path)} could not be rendered; using a file icon")
    rescue Timeout::Error
      begin
        Process.kill('KILL', pid)
      rescue Errno::ESRCH
        # The renderer may have exited just as the timeout fired.
      end
      begin
        Process.wait(pid)
      rescue Errno::ECHILD
        # wait2 may already have reaped the process.
      end
      raise
    end
  end
end
