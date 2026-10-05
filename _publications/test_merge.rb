require_relative '../_plugins/publications'
include Jekyll::PublicationFilters

def check(condition, message)
  raise message unless condition
end

accepted = {'id' => 'accepted:test', 'title' => 'Owner title', 'authors' => ['Seongwon Kim'],
            'category' => 'journal', 'status' => 'accepted', 'accepted_date' => '2026-09-18',
            'verification_source' => 'Owner document'}
update = {'_target' => 'accepted:test', 'category' => 'journal', 'status' => 'published',
          'title' => 'Publisher spelling', 'authors' => ['Unwanted replacement'],
          'doi' => '10.1234/test', 'date' => '2026-10-01', 'year' => 2026,
          'details' => 'Journal, 2026', 'verification_source' => 'https://doi.org/10.1234/test'}
records = publication_records([], [accepted], [update])
check(records.length == 1, 'Accepted record duplicated')
check(records[0]['status'] == 'published', 'Publication status did not advance')
check(records[0]['authors'] == ['Seongwon Kim'], 'Curated author spelling overwritten')
check(records[0]['title'] == 'Owner title', 'Curated title overwritten')
check(records[0]['verification_source'] == 'Owner document', 'Original verification source overwritten')
check(records[0]['link'] == 'https://doi.org/10.1234/test', 'DOI not applied')
check(accepted['status'] == 'accepted', 'Input mutated')
check(publication_records([], [accepted.merge('exclude' => true)], [update]).empty?, 'Excluded record reintroduced')

patent = {'audit_key' => 'pat-1', 'category' => 'patent', 'title' => 'Patent', 'status' => 'registered', 'details' => 'Grant'}
old = {'_target' => 'pat-1', 'category' => 'patent', 'status' => 'application', 'details' => 'Application'}
result = publication_records([], [patent], [old])[0]
check(result['status'] == 'registered' && result['details'] == 'Grant', 'Grant was downgraded')
software = {'audit_key' => 'sw-1', 'category' => 'software', 'title' => 'Program', 'year' => 2025,
            'year_basis' => 'internal_reference_year', 'status' => 'unknown'}
registration = {'_target' => 'sw-1', 'category' => 'software', 'year' => 2026,
                'registration_date' => '2026-09-01', 'year_basis' => 'registration_year', 'status' => 'registered'}
result = publication_records([], [software], [registration])[0]
check(result['year'] == 2026 && result['year_basis'] == 'registration_year', 'Internal year was used instead of verified registration year')
puts 'Publication rendering merge checks passed'
