require 'date'
require 'digest'
require 'json'
require 'open3'
require 'time'
require 'yaml'
require_relative 'publications'

module Jekyll
  # Use committed bibliographic changes, never the build time or a file's mtime.
  # Comparing merged records keeps checks, provenance-only edits, and changes to
  # a different researcher's works from advancing this person's update time.
  class PublicationHistory
    include PublicationFilters

    CURATED = %w[legacy-publications discovered-publications ip-publications
                 accepted-publications under-review-publications
                 collaborator-publications-oh collaborator-publications-bae].freeze
    PATHS = (CURATED + %w[citations auto-publications]).map { |name| "_data/#{name}.yaml" }.push(
      '_data/publication-automation.json'
    ).freeze
    VISIBLE_FIELDS = %w[category year status title link authors contributor_role subtype scope
                        details details_en publisher date id doi accepted_date document_link].freeze

    def initialize(source)
      @source = source
      @blobs = {}
    end

    def fingerprints(data, researchers)
      records = publication_records(data['citations'], CURATED.flat_map { |name| Array(data[name]) },
                                    data['auto-publications'], data.dig('publication-automation', 'researchers') || researchers)
      researchers.to_h do |person|
        scoped = publications_for_researcher(records, person['id'])
        scoped = scoped.reject { |r| r['category'] == 'intellectual-property' } unless person['main_publications']
        visible = scoped.map { |record| VISIBLE_FIELDS.to_h { |field| [field, record[field]] } }
        [person['id'], Digest::SHA256.hexdigest(JSON.generate(visible))]
      end
    end

    def updated_at(data)
      researchers = data.dig('publication-automation', 'researchers') || []
      current = fingerprints(data, researchers)
      pending = current.keys
      candidates, result = {}, {}
      history = git('log', '--first-parent', '--format=%H %cI', 'HEAD', '--', *PATHS)
      return {} unless history

      history.lines.each do |line|
        commit, timestamp = line.strip.split(' ', 2)
        timestamp = Time.iso8601(timestamp).utc.iso8601
        snapshot = fingerprints(data_at(commit), researchers)
        pending.dup.each do |person|
          if snapshot[person] == current[person]
            candidates[person] = timestamp
          else
            result[person] = candidates[person] if candidates[person]
            pending.delete(person)
          end
        end
        break if pending.empty?
      end
      # A shallow clone cannot establish when the first available version changed.
      unless git('rev-parse', '--is-shallow-repository').to_s.strip == 'true'
        pending.each { |person| result[person] = candidates[person] if candidates[person] }
      end
      result
    end

    private

    def git(*args)
      out, _error, status = Open3.capture3('git', '-C', @source, *args)
      status.success? ? out : nil
    end

    def data_at(commit)
      tree = git('ls-tree', '-r', commit, '--', *PATHS)
      raise "Cannot read publication history at #{commit}" unless tree

      tree.lines.to_h do |line|
        metadata, path = line.strip.split("\t", 2)
        blob = metadata.split.last
        value = @blobs.fetch(blob) do
          raw = git('cat-file', 'blob', blob)
          raise "Cannot read publication data #{path}" unless raw

          @blobs[blob] = YAML.safe_load(raw, permitted_classes: [Date, Time], aliases: true)
        end
        [File.basename(path, File.extname(path)), value]
      end
    end
  end

  module PublicationTimeFilters
    def publication_time_kst(value)
      Time.iso8601(value.to_s).getlocal('+09:00').strftime('%Y.%m.%d %H:%M KST')
    rescue ArgumentError
      ''
    end
  end

  class PublicationFreshnessGenerator < Generator
    safe true
    def generate(site)
      site.data['publication-update-times'] = PublicationHistory.new(site.source).updated_at(site.data)
    end
  end
end

Liquid::Template.register_filter(Jekyll::PublicationTimeFilters)
