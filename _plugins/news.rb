module Jekyll
  # CMS-created posts use the same bilingual URL convention as existing NEWS.
  class NewsPermalinkGenerator < Generator
    safe true
    priority :high

    def generate(site)
      site.posts.docs.each do |post|
        next unless post.data['permalink'].to_s.empty?
        ref = post.data['ref']
        lang = post.data['lang']
        unless ref.is_a?(String) && ref.match?(/\A[a-z0-9]+(?:-[a-z0-9]+)*\z/) && %w[ko en].include?(lang)
          raise Errors::FatalException, 'NEWS: New posts need a valid ref and ko/en language'
        end
        prefix = lang == 'en' ? '/en' : ''
        # Keep the Korean site's date stable across local and UTC build machines.
        date_path = post.date.getlocal('+09:00').strftime('%Y/%m/%d')
        post.data['permalink'] = "#{prefix}/news/#{date_path}/#{ref}/"
      end
      urls = site.posts.docs.map(&:url)
      raise Errors::FatalException, 'NEWS: Duplicate post URLs' unless urls.uniq.size == urls.size
    end
  end
end
