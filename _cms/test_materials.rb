require 'jekyll'
require 'tmpdir'
require 'fileutils'
require 'yaml'
require 'nokogiri'
require 'jekyll-last-modified-at'
require 'jekyll-redirect-from'
require_relative '../_plugins/materials'

ROOT = File.expand_path('..', __dir__)
$checks = 0
def check(condition, message)
  raise message unless condition
  $checks += 1
end

def rejected(site, message)
  Jekyll::MaterialsGenerator.new.generate(site)
  raise "Expected rejection: #{message}"
rescue Jekyll::Errors::FatalException => error
  check(error.message.include?(message), "Wrong error: #{error.message}")
end

def bilingual(ko, en)
  {'ko' => ko, 'en' => en}
end

def fixture_course
  {
    'id' => 'orbital-mechanics-2027-spring', 'term_order' => 202701,
    'term' => bilingual('2027년 봄학기', 'Spring 2027'),
    'title' => bilingual('궤도역학 & 실습', 'Orbital Mechanics & Exercises'),
    'description' => bilingual('과목 설명', 'Course description'), 'updated' => '2027-03-01',
    'overview' => [{'label' => bilingual('계획서', 'Syllabus'), 'url' => '/downloads/shared.pdf', 'type' => 'PDF'}],
    'weeks' => [
      {'number' => 2, 'title' => bilingual('두 번째', 'Second'), 'materials' => [
        {'label' => bilingual('노트', 'Notes'), 'url' => {'ko' => '/downloads/notes.pdf', 'en' => ''}}
      ]},
      {'number' => 1, 'title' => bilingual('첫 번째', 'First'), 'materials' => [
        {'label' => bilingual('코드', 'Code'), 'url' => 'https://example.org/code?a=1&b=2'}
      ]}
    ]
  }
end

Dir.mktmpdir('search-lab-materials-') do |dir|
  source = File.join(dir, 'source')
  FileUtils.mkdir_p(source)
  write = lambda do |path, value|
    target = File.join(source, path)
    FileUtils.mkdir_p(File.dirname(target))
    File.write(target, value)
  end
  %w[course-materials.html course-materials-link.html course-resources.html library.html gallery.html].each do |name|
    write.call("_includes/#{name}", File.read(File.join(ROOT, '_includes', name)))
  end
  write.call('_includes/icon.html', '<i aria-hidden="true"></i>')
  write.call('_layouts/default.html', '<html lang="{{ page.lang }}"><meta name="modified" content="{{ page.last_modified_at | date_to_xmlschema }}">{{ content }}</html>')
  write.call('_layouts/course.html', File.read(File.join(ROOT, '_layouts/course.html')))
  %w[course-ui library-ui gallery-ui].each do |name|
    write.call("_data/#{name}.yaml", File.read(File.join(ROOT, '_data', "#{name}.yaml")))
  end
  %w[shared.pdf notes.pdf english.pdf].each { |name| write.call("downloads/#{name}", '%PDF fixture') }
  %w[ko en].each do |lang|
    prefix = lang == 'en' ? 'en/' : ''
    write.call("#{prefix}resources/index.html", "---\nlayout: default\nlang: #{lang}\n---\n{% include library.html %}")
    write.call("#{prefix}students/index.html", "---\nlayout: default\nlang: #{lang}\n---\n{% include course-materials-link.html %}")
    legacy_index = File.read(File.join(ROOT, prefix, 'students/courses/index.md'))
    write.call("#{prefix}students/courses/index.html", legacy_index.sub("---\n", "---\nlang: #{lang}\n"))
  end
  course = fixture_course
  item = {'id' => 'research-notes', 'title' => bilingual('연구 <노트>', 'Research <notes>'),
          'description' => bilingual('궤도 & 해석', 'Orbit & analysis'), 'category' => 'research',
          'updated' => '2027-03-02', 'url' => '/downloads/notes.pdf', 'url_en' => '/downloads/english.pdf', 'type' => 'PDF'}
  older = Marshal.load(Marshal.dump(item)).merge('id' => 'older-code', 'updated' => '2026-12-01', 'category' => 'code', 'url' => 'https://example.org/code?a=1&b=2', 'url_en' => '')
  write.call('_data/courses.yaml', YAML.dump({'courses' => [course]}))
  write.call('_data/library.yaml', YAML.dump({'items' => [older, item]}))
  write.call('_data/gallery.yaml', "albums: []\n")
  config = Jekyll.configuration('source' => source, 'destination' => File.join(dir, 'site'), 'baseurl' => '/preview', 'url' => 'https://example.org', 'plugins' => ['jekyll-redirect-from'], 'quiet' => true)
  site = Jekyll::Site.new(config)
  site.process
  generated = site.pages.select { |page| page.data['course_id'] == course['id'] }
  check(generated.size == 2, 'A CMS course must generate exactly two language pages')
  check(generated.map { |page| page.data['lang'] }.sort == %w[en ko], 'Generated language metadata')
  check(generated.map { |page| page.data['ref'] }.uniq.size == 1, 'Language switch pairing')
  check(generated.all? { |page| page.data['parent_ref'] == 'resources' }, 'Course pages belong to Resources navigation')
  %w[ko en].each do |lang|
    prefix = lang == 'en' ? 'en/' : ''
    path = "#{prefix}students/courses/#{course['id']}/index.html"
    html = Nokogiri::HTML(File.read(File.join(site.dest, path)))
    check(html.at_css('h1').text == course['title'][lang], "#{lang}: generated title and escaping")
    check(html.at_css('meta[name="modified"]')['content'].start_with?('2027-03-01'), "#{lang}: generated pages support last-modified metadata without a physical wrapper")
    check(html.css('.course-week h3').map { |h| h['id'] } == %w[week-1 week-2], "#{lang}: numerical weekly order")
    check(html.css('.course-resources a').map { |a| a['href'] } == ['/preview/downloads/shared.pdf', 'https://example.org/code?a=1&b=2', '/preview/downloads/notes.pdf'], "#{lang}: shared, external and fallback links")
    check(html.at_css('.course-back a')['href'] == "/preview/#{prefix}resources/#courses", "#{lang}: course returns to unified Resources list")
    index = Nokogiri::HTML(File.read(File.join(site.dest, prefix, 'students/courses/index.html')))
    check(index.at_css('link[rel="canonical"]')['href'] == "https://example.org/preview/#{prefix}resources/#courses", "#{lang}: legacy list redirects to Resources course section")
    students = Nokogiri::HTML(File.read(File.join(site.dest, prefix, 'students/index.html')))
    check(students.at_css('.course-entry')['href'] == "/preview/#{prefix}resources/#courses", "#{lang}: For Students links to the same course section")
    library = Nokogiri::HTML(File.read(File.join(site.dest, prefix, 'resources/index.html')))
    check(library.css('h1').size == 1 && library.css('section').map { |section| section['id'] } == %w[general courses albums], "#{lang}: one Resources page contains all material sections")
    check(library.at_css('#courses .course-card a')['href'] == "/preview/#{prefix}students/courses/#{course['id']}/", "#{lang}: Resources links to the generated course")
    check(library.css('[data-library-item]').map { |el| el['data-category'] } == %w[research code], "#{lang}: newest first")
    check(library.at_css('.library-card h3').text == item['title'][lang], "#{lang}: library title is escaped")
    expected = lang == 'en' ? 'english.pdf' : 'notes.pdf'
    check(library.at_css('.library-card a')['href'] == "/preview/downloads/#{expected}", "#{lang}: localized library file")
    check(library.css('.library-card a')[1]['href'] == 'https://example.org/code?a=1&b=2', "#{lang}: English file fallback and external query")
    check(library.at_css('[data-library-item]')['data-search'].include?('Research <notes>'), "#{lang}: bilingual search text")
  end
  # Existing wrappers are preserved, and deleting CMS data removes generated pages.
  write.call("students/courses/#{course['id']}/index.html", "---\nlayout: course\ncourse_id: #{course['id']}\nlang: ko\n---\n<p>Custom course content</p>")
  site = Jekyll::Site.new(config)
  site.process
  check(site.pages.count { |p| p.data['course_id'] == course['id'] } == 2, 'No duplicate hand-written wrapper')
  check(File.read(File.join(site.dest, "students/courses/#{course['id']}/index.html")).include?('Custom course content'), 'Preserve hand-written content')

  mutations = [
    ['Duplicate courses IDs', ->(s) { s.data['courses']['courses'] << fixture_course }],
    ['Invalid courses ID', ->(s) { s.data['courses']['courses'][0]['id'] = '../escape' }],
    ['Duplicate week numbers', ->(s) { s.data['courses']['courses'][0]['weeks'][1]['number'] = 2 }],
    ['Missing or invalid local material', ->(s) { s.data['library']['items'][0]['url'] = '/downloads/missing.pdf' }],
    ['Missing or invalid local material', ->(s) { s.data['library']['items'][0]['url'] = '/../outside.pdf' }],
    ['External material links must use HTTPS', ->(s) { s.data['library']['items'][0]['url'] = 'javascript:alert(1)' }],
    ['Invalid library updated date', ->(s) { s.data['library']['items'][0]['updated'] = '2027-02-30' }],
    ['Unknown library category', ->(s) { s.data['library']['items'][0]['category'] = 'unknown' }],
    ['library title needs ko and en', ->(s) { s.data['library']['items'][0]['title'].delete('en') }]
  ]
  mutations.each do |message, mutation|
    invalid = Jekyll::Site.new(config)
    invalid.read
    mutation.call(invalid)
    rejected(invalid, message)
  end
  FileUtils.rm_rf(File.join(source, 'students/courses', course['id']))
  write.call('_data/courses.yaml', "courses: []\n")
  write.call('_data/library.yaml', "items: []\n")
  empty = Jekyll::Site.new(config)
  empty.process
  check(!File.exist?(File.join(empty.dest, "en/students/courses/#{course['id']}/index.html")), 'Deleted course output must be cleaned')
  check(File.read(File.join(empty.dest, 'resources/index.html')).include?('아직 등록된 자료가 없습니다'), 'Empty state has no placeholder materials')
end

cms = YAML.load_file(File.join(ROOT, 'admin/config.yml'), aliases: true)
check(cms.dig('backend', 'repo') == 'ust-search-lab/ust-search-lab.github.io', 'CMS targets the correct repository')
check(cms.dig('backend', 'branch') == 'main', 'CMS uses the production source branch')
file_fields = lambda do |fields|
  fields.flat_map { |field| (field['widget'] == 'file' ? [field] : []) + file_fields.call(field['fields'] || []) }
end
uploads = cms['collections'].flat_map { |collection| (collection['files'] || []).flat_map { |file| file_fields.call(file['fields']) } }
check(uploads.size == 6 && uploads.all? { |field| field.dig('media_library', 'config', 'max_file_size') == 20 * 1024 * 1024 }, 'CMS file fields enforce the upload size limit')
check(cms['collections'][0]['files'].map { |f| f['file'] } == %w[_data/library.yaml _data/courses.yaml _data/gallery.yaml], 'CMS manages all material sources together')
puts "Materials rendering, generation and CMS configuration: #{$checks} checks passed"
