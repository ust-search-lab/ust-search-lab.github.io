require 'liquid'

module Jekyll
  module PublicationFilters
    # Keep the imported record in a separate, curated file so citation refreshes
    # cannot overwrite it. Merge only automatic entries into this source list.
    def publication_records(citations, legacy, updates = [], researchers = [])
      curated_records = Array(legacy).map do |entry|
        attribute_publication(normalize_publication(entry), researchers)
      end
      excluded, included = curated_records.partition { |entry| entry['exclude'] == true }
      records = []
      included.each do |record|
        index = records.index { |entry| same_publication?(entry, record) }
        if index
          records[index] = merge_publication(records[index], record)
        else
          records << record
        end
      end

      Array(updates).select { |entry| entry['_target'] }.each do |update|
        record = records.find { |entry| (entry['audit_key'] || entry['id']) == update['_target'] }
        next unless record && record['category'] == update['category']

        record['researcher_ids'] = (Array(record['researcher_ids']) + Array(update['researcher_ids'])).uniq

        # Automatic refreshes may add verified metadata and advance status, while
        # preserving the owner's title, author spelling, provenance and exclusions.
        advancing = (%w[accepted under_review].include?(record['status']) && update['status'] == 'published') ||
                    ([nil, 'unknown', 'application'].include?(record['status']) && update['status'] == 'registered')
        software_enriched = record['category'] == 'software' &&
                            (%w[registration_number registration_date].any? { |key| update[key] && !record[key] } ||
                             (record['year_basis'] == 'internal_reference_year' && update['year_basis'] == 'registration_year'))
        fillable = %w[doi date year publisher application_number application_date
                      registration_number registration_date copyright_author contributor_role year_basis country]
        fillable.each do |key|
          record[key] = update[key] if update[key] && (record[key].nil? || record[key] == '')
        end
        if advancing || software_enriched
          %w[status details details_en link].each { |key| record[key] = update[key] if update[key] }
          if update['status'] == 'published'
            %w[year date doi publisher].each { |key| record[key] = update[key] if update[key] }
          end
          if record['category'] == 'software' && update['year_basis'] == 'registration_year'
            %w[year year_basis].each { |key| record[key] = update[key] if update[key] }
          end
        end
        if update['doi'] && record['doi'] == update['doi']
          record['id'] = "doi:#{record['doi']}"
          record['link'] = "https://doi.org/#{record['doi']}"
        end
        if update['verification_source']
          record['automatic_sources'] = (Array(record['automatic_sources']) + [update['verification_source']]).uniq
        end
      end

      # ORCID citations and curated bibliographies are already attributed sources.
      # New discovery records must carry the collector's confirmed identities;
      # a coauthor name alone cannot silently expand their publication scope.
      automatic_records = Array(citations).map do |entry|
        attribute_publication(normalize_publication(entry), researchers)
      end + Array(updates).reject { |entry| entry['_target'] }
      automatic_records.each do |entry|
        automatic = normalize_publication(entry)
        next if excluded.any? { |record| excluded_publication?(record, automatic) }

        index = records.index { |record| same_publication?(record, automatic) }

        if index
          records[index] = merge_publication(records[index], automatic)
        else
          records << automatic
        end
      end

      records.sort_by { |record| [-record.fetch('year', 0).to_i, record['title'].to_s] }
    end

    def publications_for_researcher(records, researcher_id)
      return [] if researcher_id.to_s.empty?

      Array(records).select { |record| Array(record['researcher_ids']).include?(researcher_id) }
    end

    # Preserve the citation's author spelling. Only explicitly verified aliases
    # identify an ORCID; a newly collected or ambiguous author remains plain text.
    def publication_authors(authors, registry)
      identifiers = {}
      aliases = {}
      Array(registry).each do |entry|
        names = ([entry['name']] + Array(entry['aliases'])).compact.map(&:to_s).uniq
        names.each { |name| (aliases[name] ||= []).concat(names) }
        next unless entry['status'] == 'verified'

        orcid = entry['orcid'].to_s.sub(%r{\Ahttps://orcid\.org/}, '')
        next unless orcid.match?(/\A\d{4}-\d{4}-\d{4}-\d{3}[\dX]\z/)

        names.each { |name| (identifiers[name] ||= []) << orcid }
      end

      Array(authors).map do |author|
        name = author.to_s
        matches = identifiers.fetch(name, []).uniq
        { 'name' => name,
          'orcid' => matches.one? ? matches.first : nil,
          'aliases' => aliases.fetch(name, []).uniq }
      end
    end

    private

    def attribute_publication(record, researchers)
      return record if record.key?('researcher_ids')

      authors = Array(record['authors']).map { |author| publication_name(author) }
      record['researcher_ids'] = Array(researchers).filter_map do |researcher|
        aliases = Array(researcher['names']).map { |name| publication_name(name) }
        researcher['id'] unless (authors & aliases).empty?
      end
      record
    end

    def publication_name(name)
      name.to_s.unicode_normalize(:nfkc).downcase.gsub(/[^\p{L}\p{N}]/, '')
    end

    def merge_publication(primary, additional)
      result = additional.merge(primary.reject { |_key, value| value.nil? || value == '' })
      result['researcher_ids'] = (Array(primary['researcher_ids']) + Array(additional['researcher_ids'])).uniq
      result['researcher_affiliations'] = (additional['researcher_affiliations'] || {}).merge(primary['researcher_affiliations'] || {})
      result['search'] = [primary['search'], additional['search'], additional['authors']].flatten.compact.join(' ')
      result['verification_sources'] = [primary['verification_sources'], additional['verification_sources'],
                                         primary['verification_source'], additional['verification_source']].flatten.compact.uniq
      result
    end

    def normalize_publication(entry)
      record = entry.to_h.dup
      record['category'] ||= case record['type']
                            when 'conference', 'conference-paper', 'proceedings-article'
                              'conference'
                            when 'patent'
                              'patent'
                            when 'software', 'computer-program'
                              'software'
                            else
                              'journal'
                            end
      year = record['year'].to_s
      year = record['date'].to_s[/\A\d{4}/] unless year.match?(/\A\d{4}\z/)
      record['year'] = year.to_i if year && year.match?(/\A\d{4}\z/)
      record['status'] ||= 'unknown' if record['category'] == 'patent'
      record['doi'] ||= publication_doi(record)
      record
    end

    def excluded_publication?(excluded, automatic)
      excluded_doi = publication_doi(excluded)
      automatic_doi = publication_doi(automatic)
      return true if excluded_doi && excluded_doi == automatic_doi

      return false unless excluded['year'] && excluded['year'] == automatic['year']

      title = publication_title(excluded)
      !title.empty? && title == publication_title(automatic)
    end

    def same_publication?(left, right)
      return false unless left['category'] == right['category']

      left_doi = publication_doi(left)
      right_doi = publication_doi(right)
      return left_doi == right_doi if left_doi && right_doi

      if left['category'] == 'conference'
        left_events = conference_events(left)
        right_events = conference_events(right)
        return false if !left_events.empty? && !right_events.empty? && (left_events & right_events).empty?

        left_date = left['date'].to_s
        right_date = right['date'].to_s
        if left_date.match?(/\A\d{4}-\d{2}(?:-\d{2})?\z/) && right_date.match?(/\A\d{4}-\d{2}(?:-\d{2})?\z/)
          precision = [left_date.length, right_date.length].min
          return false if left_date[0, precision] != right_date[0, precision]
        end
      end

      if %w[patent intellectual-property].include?(left['category'])
        return false if left['country'] && right['country'] && left['country'] != right['country']

        %w[application_number registration_number].each do |key|
          next unless left[key] && right[key]

          return publication_name(left[key]) == publication_name(right[key])
        end
      elsif left['category'] == 'software' && left['registration_number'] && right['registration_number']
        return left['registration_number'] == right['registration_number']
      end
      return false if left['year'] && right['year'] && left['year'] != right['year']

      title = publication_title(left)
      !title.empty? && title == publication_title(right)
    end

    def publication_doi(record)
      [record['doi'], record['id'], record['link']].each do |value|
        doi = value.to_s.strip.sub(%r{\A(?:doi:|https?://(?:dx\.)?doi\.org/)}i, '')
        return doi.downcase if doi.match?(%r{\A10\.\d{4,9}/\S+\z})
      end
      nil
    end

    def conference_events(record)
      [record['link'], record['source'], record['verification_source'], *Array(record['verification_sources'])]
        .compact.flat_map { |url| url.to_s.downcase.scan(%r{https?://(?:www\.)?([^/\s]+/(?:proceedings|wp)/\d{4}[a-z]+/)}) }.flatten.uniq
    end

    def publication_title(record)
      record['title'].to_s.unicode_normalize(:nfkc).downcase.gsub(/[^\p{L}\p{N}]/, '')
    end
  end
end

Liquid::Template.register_filter(Jekyll::PublicationFilters)
