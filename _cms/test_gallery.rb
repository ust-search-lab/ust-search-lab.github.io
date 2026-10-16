require 'jekyll'
require 'tmpdir'
require 'fileutils'
require 'yaml'
require 'nokogiri'
require 'jekyll-last-modified-at'
require_relative '../_plugins/materials'
require_relative '../_plugins/news'
require_relative '../_plugins/regex'

ROOT = File.expand_path('..', __dir__)
$checks = 0
def check(condition, message)
  raise message unless condition
  $checks += 1
end

def localized(ko, en)
  { 'ko' => ko, 'en' => en }
end

Dir.mktmpdir('search-lab-gallery-') do |dir|
  source = File.join(dir, 'source')
  write = lambda do |path, value|
    target = File.join(source, path)
    FileUtils.mkdir_p(File.dirname(target))
    File.write(target, value)
  end
  %w[gallery.html post-album.html post-photos.html figure.html fallback.html].each do |name|
    write.call("_includes/#{name}", File.read(File.join(ROOT, '_includes', name)))
  end
  write.call('_includes/icon.html', '<i aria-hidden="true"></i>')
  write.call('_layouts/default.html', '<html lang="{{ page.lang }}">{{ content }}</html>')
  write.call('_layouts/post.html', "---\nlayout: default\n---\n{{ content }}{% include post-photos.html %}{% include post-album.html %}")
  write.call('_layouts/album.html', File.read(File.join(ROOT, '_layouts/album.html')))
  %w[gallery-ui library-ui].each do |name|
    write.call("_data/#{name}.yaml", File.read(File.join(ROOT, '_data', "#{name}.yaml")))
  end
  %w[first.jpeg second.jpeg replacement.jpeg].each { |name| write.call("images/#{name}", 'image fixture') }
  album = {
    'id' => 'conference-2026', 'title' => localized('학회 & 방문', 'Conference & visit'),
    'description' => localized('활동 사진', 'Activity photos'), 'updated' => '2026-10-16',
    'photos' => [
      { 'image' => '/images/first.jpeg', 'alt' => localized('첫 번째 사진', 'First photo'), 'width' => '100%' },
      { 'image' => '/images/second.jpeg', 'alt' => localized('두 번째 사진', 'Second photo'), 'width' => '540px' }
    ]
  }
  write.call('_data/gallery.yaml', YAML.dump('albums' => [album]))
  %w[ko en].each do |lang|
    prefix = lang == 'en' ? 'en/' : ''
    write.call("#{prefix}resources/index.html", "---\nlayout: default\nlang: #{lang}\n---\n{% include gallery.html %}")
    post = {
      'layout' => 'post', 'title' => "NEWS #{lang}", 'ref' => 'conference-visit', 'lang' => lang,
      'date' => '2026-10-11 00:00:00 +0900', 'photo_album' => album['id']
    }
    write.call("_posts/2026-10-11-conference-visit-#{lang}.md", YAML.dump(post) + "---\n\nArticle body.\n")
  end
  link_post = {
    'layout' => 'post', 'title' => 'Link only', 'ref' => 'link-only', 'lang' => 'ko',
    'permalink' => '/news/existing-address/', 'date' => '2026-10-10 00:00:00 +0900',
    'photo_album' => album['id'], 'photo_album_display' => 'link'
  }
  write.call('_posts/2026-10-10-link-only.md', YAML.dump(link_post) + "---\n\nExisting news.\n")
  selected_photos = [
    { 'image' => '/images/first.jpeg', 'alt' => 'Selected <photo> & group', 'width' => '100%' },
    { 'image' => 'https://example.org/photo.jpeg?size=large&view=original', 'alt' => 'External photo', 'width' => '540px' }
  ]
  %w[ko en].each do |lang|
    selected_post = {
      'layout' => 'post', 'title' => 'Selected photos', 'ref' => 'selected-photos', 'lang' => lang,
      'date' => '2026-10-09 00:00:00 +0900', 'photo_album' => album['id'],
      'photo_album_display' => 'link', 'photos' => selected_photos
    }
    write.call("_posts/2026-10-09-selected-photos-#{lang}.md", YAML.dump(selected_post) + "---\n\nOnline post.\n")
  end
  config = Jekyll.configuration('source' => source, 'destination' => File.join(dir, 'site'),
                                'baseurl' => '/preview', 'plugins' => [], 'quiet' => true)
  site = Jekyll::Site.new(config)
  site.process
  check(site.pages.count { |page| page.data['album_id'] == album['id'] } == 2, 'Album generates paired language pages')
  %w[ko en].each do |lang|
    prefix = lang == 'en' ? 'en/' : ''
    album_path = "#{prefix}resources/albums/#{album['id']}/index.html"
    html = Nokogiri::HTML(File.read(File.join(site.dest, album_path)))
    check(html.at_css('h1').text == album['title'][lang], "#{lang}: escaped album title")
    check(html.css('.album-photo img').map { |image| image['src'] } == %w[/preview/images/first.jpeg /preview/images/second.jpeg], "#{lang}: album uses original files in order")
    check(html.css('[data-photo-original]').map { |a| a['href'] } == html.css('.album-photo img').map { |image| image['src'] }, "#{lang}: copy and original links use the displayed files")
    check(html.css('figcaption').empty?, "#{lang}: no visible photo captions")
    check(html.css('a').any? { |a| a['href'] == "/preview/#{prefix}news/2026/10/11/conference-visit/" }, "#{lang}: album links to related NEWS in the same language; links: #{html.css('a').map { |a| a['href'] }}")
    index = Nokogiri::HTML(File.read(File.join(site.dest, prefix, 'resources/index.html')))
    check(index.at_css('.album-cover')['href'] == "/preview/#{prefix}resources/albums/#{album['id']}/", "#{lang}: Resources links to album")
    article = Nokogiri::HTML(File.read(File.join(site.dest, prefix, 'news/2026/10/11/conference-visit/index.html')))
    check(article.css('.figure img').map { |image| image['src'] } == html.css('.album-photo img').map { |image| image['src'] }, "#{lang}: NEWS reuses album originals without copies")
    check(article.at_css('.album-news-link')['href'] == "/preview/#{prefix}resources/albums/#{album['id']}/", "#{lang}: NEWS links back to album")
    check(article.css('.figure img').last['style'].include?('540px'), "#{lang}: portrait width preserved")
  end
  link_only = Nokogiri::HTML(File.read(File.join(site.dest, 'news/existing-address/index.html')))
  check(link_only.css('.figure').empty? && link_only.at_css('.album-news-link'), 'Link-only mode preserves existing NEWS address and omits inline photos')
  %w[ko en].each do |lang|
    prefix = lang == 'en' ? 'en/' : ''
    article = Nokogiri::HTML(File.read(File.join(site.dest, prefix, 'news/2026/10/09/selected-photos/index.html')))
    check(article.css('.figure img').map { |img| img['src'] } == ['/preview/images/first.jpeg', selected_photos[1]['image']], "#{lang}: selected local and external photos render in order without album duplicates")
    check(article.at_css('.figure img')['alt'] == 'Selected photo group', "#{lang}: selected photo alt text is rendered as plain text")
    check(article.css('.figure img').last['style'].include?('540px'), "#{lang}: selected portrait retains its width")
    check(article.css('figcaption').empty? && article.at_css('.album-news-link'), "#{lang}: selected photos have no captions and keep the album link")
  end

  album['photos'][0]['image'] = '/images/replacement.jpeg'
  album['photos'] << { 'image' => '/images/replacement.jpeg', 'alt' => localized('추가 사진', 'Added photo') }
  write.call('_data/gallery.yaml', YAML.dump('albums' => [album]))
  refreshed = Jekyll::Site.new(config)
  refreshed.process
  news = Nokogiri::HTML(File.read(File.join(refreshed.dest, 'news/2026/10/11/conference-visit/index.html')))
  check(news.at_css('.figure img')['src'] == '/preview/images/replacement.jpeg', 'Editing the album updates photos in linked NEWS')
  selected = Nokogiri::HTML(File.read(File.join(refreshed.dest, 'news/2026/10/09/selected-photos/index.html')))
  check(selected.css('.figure img').map { |img| img['src'] } == ['/preview/images/first.jpeg', selected_photos[1]['image']], 'Album additions and replacements do not change individually selected NEWS photos')

  # Decap serializes its date-only widget as an unquoted YAML date when publishing.
  album['updated'] = Date.new(2026, 10, 17)
  album['photos'].shift
  write.call('_data/gallery.yaml', YAML.dump('albums' => [album]))
  deleted = Jekyll::Site.new(config)
  deleted.process
  %w[ko en].each do |lang|
    prefix = lang == 'en' ? 'en/' : ''
    html = Nokogiri::HTML(File.read(File.join(deleted.dest, prefix, 'resources/albums', album['id'], 'index.html')))
    check(html.css('.album-photo img').map { |img| img['src'] } == %w[/preview/images/second.jpeg /preview/images/replacement.jpeg], "#{lang}: CMS photo deletion publishes with an unquoted date")
    check(html.at_css('.album-meta time')['datetime'] == '2026-10-17', "#{lang}: CMS album date renders correctly")
    index = Nokogiri::HTML(File.read(File.join(deleted.dest, prefix, 'resources/index.html')))
    check(index.at_css('.album-cover img')['src'] == '/preview/images/second.jpeg', "#{lang}: deleting the cover updates the Resources thumbnail")
    check(index.at_css('.album-meta').text.include?(lang == 'ko' ? '사진 2장' : '2 photos'), "#{lang}: album photo count updates after deletion")
    article = Nokogiri::HTML(File.read(File.join(deleted.dest, prefix, 'news/2026/10/09/selected-photos/index.html')))
    check(article.css('.figure img').map { |img| img['src'] } == ['/preview/images/first.jpeg', selected_photos[1]['image']], "#{lang}: album deletion preserves independently selected NEWS photos")
  end

  [
    ['Unknown photo album', ->(s) { s.data['gallery']['albums'] = [] }],
    ['Duplicate albums IDs', ->(s) { s.data['gallery']['albums'] << album }],
    ['An album needs at least one photo', ->(s) { s.data['gallery']['albums'][0]['photos'] = [] }],
    ['Missing or invalid local material', ->(s) { s.data['gallery']['albums'][0]['photos'][0]['image'] = '/images/missing.jpeg' }],
    ['Invalid photo width', ->(s) { s.data['gallery']['albums'][0]['photos'][0]['width'] = 'invalid' }],
    ['NEWS photos must be a list', ->(s) { s.posts.docs.first.data['photos'] = 'invalid' }],
    ['Each NEWS photo must be an object', ->(s) { s.posts.docs.first.data['photos'] = ['invalid'] }],
    ['NEWS photos need alt text', ->(s) { s.posts.docs.first.data['photos'] = [{ 'image' => '/images/first.jpeg' }] }],
    ['Invalid NEWS photo width', ->(s) { s.posts.docs.first.data['photos'] = [{ 'image' => '/images/first.jpeg', 'alt' => 'Photo', 'width' => 'invalid' }] }],
    ['External material links must use HTTPS', ->(s) { s.posts.docs.first.data['photos'] = [{ 'image' => 'javascript:alert(1)', 'alt' => 'Photo' }] }]
  ].each do |expected, mutate|
    invalid = Jekyll::Site.new(config)
    invalid.read
    mutate.call(invalid)
    begin
      Jekyll::MaterialsGenerator.new.generate(invalid)
      raise "Expected error: #{expected}"
    rescue Jekyll::Errors::FatalException => error
      check(error.message.include?(expected), "Expected #{expected}, got #{error.message}")
    end
  end
end

puts "Photo albums, shared NEWS photos and bilingual URLs: #{$checks} checks passed"
