require 'jekyll'
require 'tmpdir'
require 'fileutils'
require_relative '../_plugins/publication_freshness'

def check(condition, message)
  raise message unless condition
end

people = [{'id' => 'park', 'names' => ['Park'], 'main_publications' => true},
          {'id' => 'oh', 'names' => ['Oh']}]
data = {'publication-automation' => {'researchers' => people},
        'legacy-publications' => [{'title' => 'Shared work', 'authors' => ['Park', 'Oh'], 'year' => 2025}]}

Dir.mktmpdir('publication-history') do |root|
  git = lambda do |*args, env: {}|
    out, error, status = Open3.capture3(env, 'git', '-C', root, *args)
    raise error unless status.success?
    out
  end
  git.call('init', '-q')
  git.call('config', 'user.name', 'Test')
  git.call('config', 'user.email', 'test@example.invalid')
  FileUtils.mkdir_p(File.join(root, '_data'))
  write = lambda do |name, value|
    File.write(File.join(root, '_data', "#{name}.yaml"), YAML.dump(value))
  end
  commit = lambda do |time|
    git.call('add', '.')
    git.call('commit', '-qm', 'Fixture change', env: {'GIT_AUTHOR_DATE' => time, 'GIT_COMMITTER_DATE' => time})
  end
  first = '2026-10-01T01:00:00Z'
  second = '2026-10-02T01:00:00Z'
  third = '2026-10-03T01:00:00Z'
  write.call('legacy-publications', data['legacy-publications'])
  File.write(File.join(root, '_data/publication-automation.json'), JSON.generate(data['publication-automation']))
  commit.call(first)
  history = Jekyll::PublicationHistory.new(root)
  check(history.updated_at(data) == {'park' => first, 'oh' => first}, 'Initial shared output must update both people')

  data['collaborator-publications-oh'] = [{'title' => 'Personal work', 'authors' => ['Oh'], 'year' => 2026}]
  write.call('collaborator-publications-oh', data['collaborator-publications-oh'])
  commit.call(second)
  check(history.updated_at(data) == {'park' => first, 'oh' => second}, 'Personal change must not update PI date')

  data['collaborator-publications-oh'][0]['verification_source'] = 'New audit source'
  write.call('collaborator-publications-oh', data['collaborator-publications-oh'])
  commit.call(third)
  write.call('publication-refresh', {'oh' => {'last_checked_at' => third}})
  commit.call('2026-10-04T01:00:00+00:00')
  check(history.updated_at(data) == {'park' => first, 'oh' => second}, 'Checks/provenance must not advance content date')

  data['legacy-publications'][0]['title'] = 'Corrected shared work'
  check(history.updated_at(data).empty?, 'Uncommitted changes must not claim a committed date')
  write.call('legacy-publications', data['legacy-publications'])
  fourth = '2026-10-05T01:00:00Z'
  commit.call(fourth)
  check(history.updated_at(data) == {'park' => fourth, 'oh' => fourth}, 'Shared correction must update both scopes')

  data['collaborator-publications-oh'] = []
  write.call('collaborator-publications-oh', [])
  fifth = '2026-10-06T01:00:00Z'
  commit.call(fifth)
  check(history.updated_at(data) == {'park' => fourth, 'oh' => fifth}, 'Removed outputs must advance only the relevant scope')

  Dir.mktmpdir('publication-shallow') do |clone|
    git.call('clone', '-q', '--depth=1', "file://#{root}", clone)
    check(Jekyll::PublicationHistory.new(clone).updated_at(data).empty?, 'Shallow history must not fabricate old change dates')
  end
end

include Jekyll::PublicationTimeFilters
check(publication_time_kst('2026-10-07T16:37:00Z') == '2026.10.08 01:37 KST', 'KST day rollover incorrect')
check(publication_time_kst(nil) == '', 'Missing time must not become build time')
puts 'Publication freshness history and timezone checks passed'
