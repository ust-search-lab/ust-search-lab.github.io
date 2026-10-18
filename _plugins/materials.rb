require 'date'
require 'uri'
require_relative 'material_covers'

module Jekyll
  # Keep the YAML edited by Decap as the source of truth for bilingual courses.
  # Pages are generated in memory, so publishing a new course needs no wrappers.
  class MaterialsGenerator < Generator
    safe true
    priority :low

    def generate(site)
      courses = records(site, 'courses', 'courses')
      library = records(site, 'library', 'items')
      albums = records(site, 'gallery', 'albums')
      validate_ids(courses, 'courses')
      validate_ids(library, 'library')
      validate_ids(albums, 'albums')
      albums.each do |album|
        localized(album['title'], 'album title')
        localized(album['description'], 'album description')
        album['updated'] = date(album['updated'], 'album updated')
        photos = album['photos']
        fail_build('An album needs at least one photo') unless photos.is_a?(Array) && !photos.empty?
        photos.each do |photo|
          fail_build('Each photo must be an object') unless photo.is_a?(Hash)
          resource_url(site, photo['image'])
          localized(photo['alt'], 'photo alt')
          fail_build('Invalid photo width') unless [nil, '', '100%', '540px'].include?(photo['width'])
        end
        %w[ko en].each { |lang| generate_album(site, album, lang) }
      end
      site.posts.docs.each do |post|
        photos = post.data['photos'] || []
        fail_build('NEWS photos must be a list') unless photos.is_a?(Array)
        photos.each do |photo|
          fail_build('Each NEWS photo must be an object') unless photo.is_a?(Hash)
          resource_url(site, photo['image'])
          fail_build('NEWS photos need alt text') unless photo['alt'].is_a?(String) && !photo['alt'].strip.empty?
          fail_build('Invalid NEWS photo width') unless [nil, '', '100%', '540px'].include?(photo['width'])
        end
        album_id = post.data['photo_album']
        next if album_id.to_s.empty?
        fail_build("Unknown photo album: #{album_id}") unless albums.any? { |album| album['id'] == album_id }
        fail_build('Invalid photo album display') unless [nil, 'photos', 'link'].include?(post.data['photo_album_display'])
      end
      covers = MaterialCovers.new(site)
      library.each do |item|
        localized(item['title'], 'library title')
        localized(item['description'], 'library description')
        fail_build('Unknown library category') unless %w[lecture research code].include?(item['category'])
        item['updated'] = date(item['updated'], 'library updated')
        resource_url(site, item['url'])
        resource_url(site, item['url_en']) unless item['url_en'].to_s.empty?
        resource_url(site, item['cover']) unless item['cover'].to_s.empty?
        item['_covers'] = covers.for_item(item)
      end
      courses.each do |course|
        localized(course['title'], 'course title')
        localized(course['description'], 'course description')
        localized(course['term'], 'course term')
        fail_build('term_order must be a positive integer') unless course['term_order'].is_a?(Integer) && course['term_order'].positive?
        course['updated'] = date(course['updated'], 'course updated') if course['updated']
        materials(site, course['overview'])
        weeks = course['weeks'] || []
        fail_build('weeks must be a list') unless weeks.is_a?(Array)
        numbers = weeks.map do |week|
          fail_build('Each week needs a positive integer number') unless week.is_a?(Hash) && week['number'].is_a?(Integer) && week['number'].positive?
          localized(week['title'], 'week title')
          week['updated'] = date(week['updated'], 'week updated') if week['updated']
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
      # CMS saves date-only values without quotes; YAML reads those as Date objects.
      # Normalize both forms before Liquid sorts mixed CMS and hand-written records.
      value = value.iso8601 if value.instance_of?(Date)
      fail_build("#{name} must be a YYYY-MM-DD date") unless value.is_a?(String) && value.match?(/\A\d{4}-\d{2}-\d{2}\z/)
      Date.iso8601(value).iso8601
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
        'parent_ref' => 'resources', 'course_id' => course['id'],
        'title' => course['title'][lang], 'description' => course['description'][lang],
        # jekyll-last-modified-at otherwise tries to stat a non-existent wrapper.
        'last_modified_at' => course['updated'],
        'permalink' => url
      )
      site.pages << page
    end

    def generate_album(site, album, lang)
      dir = [lang == 'en' ? 'en' : nil, 'resources', 'albums', album['id']].compact.join('/')
      url = "/#{dir}/"
      fail_build("Album URL already used: #{url}") if site.pages.any? { |page| page.url == url }
      page = PageWithoutAFile.new(site, site.source, dir, 'index.html')
      page.content = ''
      page.data.merge!(
        'layout' => 'album', 'lang' => lang, 'ref' => "album-#{album['id']}",
        'parent_ref' => 'resources', 'album_id' => album['id'],
        'title' => album['title'][lang], 'description' => album['description'][lang],
        'last_modified_at' => album['updated'], 'permalink' => url
      )
      site.pages << page
    end
  end
end
