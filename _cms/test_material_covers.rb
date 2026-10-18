require 'jekyll'
require 'tmpdir'
require 'fileutils'
require 'yaml'
require_relative '../_plugins/materials'

# A tiny, valid PDF keeps renderer tests independent of network downloads.
def pdf_fixture(title)
  stream = "BT /F1 24 Tf 40 220 Td (#{title}) Tj ET\n"
  objects = [
    '<< /Type /Catalog /Pages 2 0 R >>',
    '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
    '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 240 320] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
    '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
    "<< /Length #{stream.bytesize} >>\nstream\n#{stream}endstream"
  ]
  pdf = "%PDF-1.4\n"
  offsets = objects.each_with_index.map do |object, index|
    offset = pdf.bytesize
    pdf << "#{index + 1} 0 obj\n#{object}\nendobj\n"
    offset
  end
  xref = pdf.bytesize
  pdf << "xref\n0 6\n0000000000 65535 f \n"
  offsets.each { |offset| pdf << format('%010d 00000 n ', offset) + "\n" }
  pdf << "trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n#{xref}\n%%EOF\n"
end

checks = 0
check = lambda do |condition, message|
  raise message unless condition
  checks += 1
end

Dir.mktmpdir('material-covers-') do |dir|
  source = File.join(dir, 'source')
  FileUtils.mkdir_p(File.join(source, 'downloads'))
  FileUtils.mkdir_p(File.join(source, '_data'))
  File.write(File.join(source, 'downloads/notes.pdf'), pdf_fixture('Original cover'))
  File.write(File.join(source, 'downloads/english.PDF'), pdf_fixture('English cover'))
  File.write(File.join(source, 'downloads/broken.pdf'), 'not a valid PDF')
  File.write(File.join(source, 'index.html'), "---\n---\n{{ site.data.library.items[0]._covers.ko | relative_url }}")
  item = {
    'id' => 'sample', 'title' => {'ko' => '자료', 'en' => 'Notes'},
    'description' => {'ko' => '설명', 'en' => 'Description'}, 'category' => 'lecture',
    'updated' => '2026-10-17', 'url' => '/downloads/notes.pdf?download=1',
    'url_en' => '/downloads/english.PDF'
  }
  data_path = File.join(source, '_data/library.yaml')
  File.write(data_path, YAML.dump('items' => [item]))
  config = Jekyll.configuration('source' => source, 'destination' => File.join(dir, 'site'), 'baseurl' => '/preview', 'quiet' => true)
  build = -> { Jekyll::Site.new(config).tap(&:process) }
  site = build.call
  covers = site.data['library']['items'][0]['_covers']
  check.call(covers['ko'] != covers['en'], 'Each language must use its own PDF cover')
  covers.each_value do |url|
    bytes = File.binread(File.join(site.dest, url))
    check.call(bytes.start_with?("\xFF\xD8".b) && bytes.bytesize > 1000, 'The generated cover must be a nonempty JPEG in the published site')
  end
  check.call(File.read(File.join(site.dest, 'index.html')).strip == "/preview#{covers['ko']}", 'Generated cover URLs work under a preview base URL')
  cached = File.join(source, '.jekyll-cache/material-covers', covers['ko'])
  mtime = File.mtime(cached)
  build.call
  check.call(File.mtime(cached) == mtime, 'Unchanged PDFs reuse the existing cover')

  File.write(File.join(source, 'downloads/notes.pdf'), pdf_fixture('Replacement cover'))
  changed = build.call
  new_cover = changed.data['library']['items'][0]['_covers']['ko']
  check.call(new_cover != covers['ko'] && File.file?(File.join(changed.dest, new_cover)), 'Replacing a PDF publishes a new cover URL')
  check.call(!File.exist?(File.join(changed.dest, covers['ko'])), 'Old cover output is cleaned after replacement')

  helper = Jekyll::MaterialCovers.new(changed)
  manual = helper.for_item(item.merge('cover' => 'https://example.org/cover.jpg'))
  check.call(manual.values == ['https://example.org/cover.jpg'] * 2, 'Manual cover overrides both automatic language covers')
  check.call(helper.for_item('url' => 'https://example.invalid/document.pdf').values.all?(&:nil?), 'External PDFs are not fetched')
  check.call(helper.for_item('url' => '/downloads/broken.pdf').values.all?(&:nil?), 'Invalid PDFs preserve the resource with an icon fallback')
  # URL aliases for one PDF should not add duplicate static files.
  duplicate_site = Jekyll::Site.new(config)
  duplicate_helper = Jekyll::MaterialCovers.new(duplicate_site)
  shared = duplicate_helper.for_item('url' => '/downloads/notes.pdf', 'url_en' => '/downloads/notes.pdf?download=1')
  check.call(shared['ko'] == shared['en'] && duplicate_site.static_files.size == 1, 'Shared PDFs generate one published cover')
  original_path = ENV['PATH']
  begin
    ENV['PATH'] = ''
    File.write(File.join(source, 'downloads/new.pdf'), pdf_fixture('No renderer'))
    check.call(helper.for_item('url' => '/downloads/new.pdf').values.all?(&:nil?), 'A missing renderer does not break publishing')
  ensure
    ENV['PATH'] = original_path
  end
  File.write(data_path, YAML.dump('items' => []))
  empty = build.call
  check.call(Dir.glob(File.join(empty.dest, 'images/material-covers/*.jpg')).empty?, 'Deleting resources removes their generated covers from the site')
end

puts "PDF cover generation: #{checks} checks passed"
