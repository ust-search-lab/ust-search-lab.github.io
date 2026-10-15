require 'date'
require 'uri'

module Jekyll
  # Keep the YAML edited by Decap as the source of truth for bilingual courses.
  # Pages are generated in memory, so publishing a new course needs no wrappers.
  class MaterialsGenerator < Generator
    safe true
    priority :low

    def generate(site)
      courses = records(site, 'courses', 'courses')
      library = records(site, 'library', 'items')
      validate_ids(courses, 'courses')
      validate_ids(library, 'library')
      library.each do |item|
        localized(item['title'], 'library title')
        localized(item['description'], 'library description')
        fail_build('Unknown library category') unless %w[lecture research code].include?(item['category'])
        date(item['updated'], 'library updated')
        resource_url(site, item['url'])
        resource_url(site, item['url_en']) unless item['url_en'].to_s.empty?
      end
      courses.each do |course|
        localized(course['title'], 'course title')
        localized(course['description'], 'course description')
        localized(course['term'], 'course term')
        fail_build('term_order must be a positive integer') unless course['term_order'].is_a?(Integer) && course['term_order'].positive?
        date(course['updated'], 'course updated') if course['updated']
        materials(site, course['overview'])
        weeks = course['weeks'] || []
        fail_build('weeks must be a list') unless weeks.is_a?(Array)
        numbers = weeks.map do |week|
          fail_build('Each week needs a positive integer number') unless week.is_a?(Hash) && week['number'].is_a?(Integer) && week['number'].positive?
          localized(week['title'], 'week title')
          date(week['updated'], 'week updated') if week['updated']
          materials(site, week['materials'])
          week['number']
        end
        fail_build('Duplicate week numbers') unless numbers.uniq.size == numbers.size
        %w[ko en].each { |lang| generate_course(site, course, lang) }
      end
    end

    private

    def fail_build(message)
      raise Errors::FatalException, "Materials: #{message}"
    end

    def records(site, data_name, key)
      value = site.data.fetch(data_name, {}).fetch(key, [])
      fail_build("#{data_name}.#{key} must be a list") unless value.is_a?(Array)
      value
    end

    def validate_ids(rows, name)
      ids = rows.map do |row|
        id = row.is_a?(Hash) && row['id']
        fail_build("Invalid #{name} ID; use lowercase letters, numbers and hyphens") unless id.is_a?(String) && id.match?(/\A[a-z0-9]+(?:-[a-z0-9]+)*\z/)
        id
      end
      fail_build("Duplicate #{name} IDs") unless ids.uniq.size == ids.size
    end

    def localized(value, name)
      fail_build("#{name} needs ko and en text") unless value.is_a?(Hash) && %w[ko en].all? { |lang| value[lang].is_a?(String) && !value[lang].strip.empty? }
    end

    def date(value, name)
      fail_build("#{name} must be a YYYY-MM-DD string") unless value.is_a?(String) && value.match?(/\A\d{4}-\d{2}-\d{2}\z/)
      Date.iso8601(value)
    rescue Date::Error
      fail_build("Invalid #{name} date")
    end

    def materials(site, rows)
      return if rows.nil?
      fail_build('materials must be a list') unless rows.is_a?(Array)
      rows.each do |resource|
        fail_build('Each material must be an object') unless resource.is_a?(Hash)
        localized(resource['label'], 'material label')
        url = resource['url']
        if url.is_a?(Hash)
          resource_url(site, url['ko'])
          resource_url(site, url['en']) unless url['en'].to_s.empty?
        else
          resource_url(site, url)
        end
      end
    end

    def resource_url(site, value)
      fail_build('A material needs a file or HTTPS URL') unless value.is_a?(String) && !value.empty?
      if value.start_with?('/') && !value.start_with?('//')
        path = URI::DEFAULT_PARSER.unescape(value.split(/[?#]/, 2).first)
        target = File.expand_path(path.delete_prefix('/'), site.source)
        fail_build("Missing or invalid local material: #{value}") unless target.start_with?(File.expand_path(site.source) + '/') && File.file?(target)
      else
        uri = URI.parse(value)
        fail_build('External material links must use HTTPS') unless uri.scheme == 'https' && uri.host && !uri.userinfo
      end
    rescue URI::InvalidURIError, ArgumentError
      fail_build('Invalid material URL')
    end

    def generate_course(site, course, lang)
      dir = [lang == 'en' ? 'en' : nil, 'students', 'courses', course['id']].compact.join('/')
      url = "/#{dir}/"
      existing = site.pages.find { |page| page.url == url }
      if existing
        fail_build("Course URL already used: #{url}") unless existing.data['course_id'] == course['id']
        return # Preserve optional hand-written course content.
      end
      page = PageWithoutAFile.new(site, site.source, dir, 'index.html')
      page.content = ''
      page.data.merge!(
        'layout' => 'course', 'lang' => lang, 'ref' => "course-#{course['id']}",
        'parent_ref' => 'students', 'course_id' => course['id'],
        'title' => course['title'][lang], 'description' => course['description'][lang],
        # jekyll-last-modified-at otherwise tries to stat a non-existent wrapper.
        'last_modified_at' => course['updated'],
        'permalink' => url
      )
      site.pages << page
    end
  end
end
