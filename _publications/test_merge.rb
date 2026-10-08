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

under_review = accepted.merge('status' => 'under_review').reject { |key, _| key == 'accepted_date' }
check(publication_records([], [under_review])[0]['status'] == 'under_review', 'Review status changed without publication evidence')
records = publication_records([], [under_review], [update])
check(records.length == 1 && records[0]['status'] == 'published', 'Under-review manuscript did not advance without duplication')
check(records[0]['title'] == under_review['title'] && records[0]['authors'] == under_review['authors'], 'Under-review curation overwritten')

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

people = [
  {'id' => 'jae-ik-park', 'names' => ['Jae-ik Park', '박재익']},
  {'id' => 'seung-ryeol-oh', 'names' => ['Snyoll Oghim', 'Seungryeol Oh', '오승렬']},
  {'id' => 'jungju-bae', 'names' => ['Jungju Bae', 'Jung-Ju Bae', '배정주']}
]
shared = {'id' => 'doi:10.1234/shared', 'title' => 'Shared output', 'authors' => ['Jae-ik Park', '오승렬'],
          'category' => 'conference', 'year' => 2026}
personal = {'id' => 'doi:10.1234/personal', 'title' => 'Historical output', 'authors' => ['Jung-Ju Bae', 'Junwoo Park'],
            'category' => 'journal', 'year' => 2023, 'researcher_ids' => ['jungju-bae']}
duplicate = personal.merge('title' => 'Remote spelling', 'researcher_ids' => ['seung-ryeol-oh'])
records = publication_records([], [shared, personal, duplicate], [], people)
check(records.size == 2, 'Shared curated records were counted twice')
check(publications_for_researcher(records, 'jae-ik-park').map { |r| r['title'] } == ['Shared output'],
      'Collaborator-only or other Park output leaked into main Publications')
check(publications_for_researcher(records, 'seung-ryeol-oh').size == 2, 'Shared output missing from collaborator profile')
check(publications_for_researcher(records, 'jungju-bae').size == 1, 'Bae career output missing')
check(publications_for_researcher(records, '').empty?, 'Empty researcher scope exposed all records')
check(personal['researcher_ids'] == ['jungju-bae'], 'Membership union mutated source data')

unverified_coauthor = {'id' => 'doi:10.1234/new', 'title' => 'Automatic output', 'category' => 'journal',
                      'authors' => ['Snyoll Oghim', 'Jae-ik Park'], 'researcher_ids' => ['seung-ryeol-oh']}
records = publication_records([], [], [unverified_coauthor], people)
check(publications_for_researcher(records, 'jae-ik-park').empty?, 'Automatic coauthor name alone established participation')

patch = {'_target' => shared['id'], 'category' => 'conference', 'researcher_ids' => ['jungju-bae']}
records = publication_records([], [shared], [patch], people)
check(publications_for_researcher(records, 'jungju-bae').size == 1, 'Verified participant patch was lost')

patent_kr = {'title' => 'Same invention', 'category' => 'patent', 'country' => 'KR', 'year' => 2020,
             'application_number' => '10-2020-123', 'researcher_ids' => ['jae-ik-park']}
patent_us = patent_kr.merge('country' => 'US', 'application_number' => '16/999999')
check(publication_records([], [patent_kr, patent_us]).size == 2, 'Patent jurisdictions collapsed')
software_a = {'title' => 'Program', 'category' => 'software', 'year' => 2020, 'registration_number' => 'C-2020-0001'}
software_b = software_a.merge('registration_number' => 'C-2020-0002')
check(publication_records([], [software_a, software_b]).size == 2, 'Distinct software registrations collapsed')
check(publication_records([], [shared, shared.merge('category' => 'journal')]).size == 2,
      'Conference and journal categories collapsed')
spring = {'title' => 'Repeated presentation title', 'category' => 'conference', 'year' => 2026,
          'date' => '2026-04-24', 'link' => 'https://ksas.or.kr/proceedings/2026a/SessionPaperList.asp?code=1',
          'researcher_ids' => ['jae-ik-park']}
fall = spring.merge('date' => '2026-09-20', 'link' => 'https://sase.or.kr/proceedings/2026b/SessionPaperList.asp?code=1',
                    'researcher_ids' => ['jungju-bae'])
records = publication_records([], [spring, fall], [], people)
check(records.size == 2, 'Separate conference presentations collapsed by title and year')
check(publications_for_researcher(records, 'jae-ik-park').first['researcher_ids'] == ['jae-ik-park'],
      'Participant from another conference leaked into PI output')
check(publication_records([], [spring, fall.reject { |key, _| key == 'date' }]).size == 2,
      'Conflicting conference events collapsed without a full date')
check(publication_records([], [spring.reject { |key, _| key == 'link' }, fall.reject { |key, _| key == 'link' }]).size == 2,
      'Conflicting conference dates collapsed without event URLs')
puts 'Researcher attribution, deduplication and page scope checks passed'
