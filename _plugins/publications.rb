require 'liquid'

module Jekyll
  module PublicationFilters
    # Keep the imported record in a separate, curated file so citation refreshes
    # cannot overwrite it. Merge only automatic entries into this source list.
    def publication_records(citations, legacy, updates = [])
      curated_records = Array(legacy).map { |entry| normalize_publication(entry) }
      excluded, records = curated_records.partition { |entry| entry['exclude'] == true }

      Array(updates).select { |entry| entry['_target'] }.each do |update|
        record = records.find { |entry| (entry['audit_key'] || entry['id']) == update['_target'] }
        next unless record && record['category'] == update['category']

        # Automatic refreshes may add verified metadata and advance status, while
        # preserving the owner's title, author spelling, provenance and exclusions.
        advancing = (record['status'] == 'accepted' && update['status'] == 'published') ||
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

      automatic_records = Array(citations) + Array(updates).reject { |entry| entry['_target'] }
      automatic_records.each do |entry|
        automatic = normalize_publication(entry)
        next if excluded.any? { |record| excluded_publication?(record, automatic) }

        index = records.index { |record| same_publication?(record, automatic) }

        if index
          curated = records[index].reject { |_key, value| value.nil? || value == '' }
          records[index] = automatic.merge(curated)
          records[index]['search'] = [automatic['search'], curated['search'],
                                      automatic['authors']].flatten.compact.join(' ')
        else
          records << automatic
        end
      end

      records.sort_by { |record| [-record.fetch('year', 0).to_i, record['title'].to_s] }
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
      left_doi = publication_doi(left)
      right_doi = publication_doi(right)
      return left_doi == right_doi if left_doi && right_doi

      return false unless left['category'] == right['category']
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

    def publication_title(record)
      record['title'].to_s.unicode_normalize(:nfkc).downcase.gsub(/[^\p{L}\p{N}]/, '')
    end
  end
end

Liquid::Template.register_filter(Jekyll::PublicationFilters)
