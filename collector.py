try:
    import Crawler.crawler as GitCrawler
    import Crawler.repository as GitRepository
    import multiprocessing
    from datetime import datetime
    from functools import partial
    import json
    import csv
    import os
except ImportError as error:
    raise ImportError(error)

class Repository():
    def __init__(self, collector, folder):
        self.collector = collector
        self.folder = folder

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    # General information about the repository (Source: API)
    def about(self):
        about_file = self.folder + '/about.json'

        if not os.path.isfile(about_file):
            about = self.collector.get()

            with open(about_file, 'w') as file:
                json.dump(about, file, indent = 4)

    # Pull requests of the repository (Source: API)
    def pull_requests(self):
        pulls_file = self.folder + '/pull_requests.json'

        if not os.path.isfile(pulls_file):
            pull_requests = self.collector.pull_requests(state='all')
    
            with open(pulls_file, 'w') as file:
                json.dump(pull_requests, file, indent = 4)

    # Contributors of the repository (Source: API)
    def contributors(self):
        contributors_file = self.folder + '/contributors.json'

        if not os.path.isfile(contributors_file):
            contributors = self.collector.contributors(anonymous='true')

            for contributor in contributors:
                if 'site_admin' in contributor.keys():
                    # We moved this developers to the internals because we found qualitative evidences that they worked at GitHub
                    if 'atom' in self.folder:
                        if contributor['login'] == 'benogle' or contributor['login'] == 'thedaniel' or contributor['login'] == 'jlord':
                            print contributor['login']
                            contributor['site_admin'] = True
                    if 'hubot' in self.folder:
                        if contributor['login'] == 'bhuga' or contributor['login'] == 'aroben':
                            contributor['site_admin'] = True
                    if 'linguist' in self.folder:
                        if contributor['login'] == 'arfon' or contributor['login'] == 'aroben' or contributor['login'] == 'tnm' or contributor['login'] == 'brandonblack' or contributor['login'] == 'rick':
                            contributor['site_admin'] = True            
                    if 'electron' in self.folder:
                        if contributor['login'] == 'miniak' or contributor['login'] == 'codebytere':
                            contributor['site_admin'] = True

            with open(contributors_file, 'w') as file:
                json.dump(contributors, file, indent = 4)

    def update_manual_values(self):
        pulls_summary_file = self.folder + '/merged_pull_requests_summary.csv'
        pulls_summary_file_updated = self.folder + '/merged_pull_requests_summary_updated.csv'

        if 'atom' in self.folder:
            manual_file = self.folder + '/atom.csv'
            print 'atom'
        if 'hubot' in self.folder:
            manual_file = self.folder + '/hubot.csv'
            print 'hubot'
        if 'electron' in self.folder:
            manual_file = self.folder + '/electron.csv'
            print 'electron'
        if 'git-lfs' in self.folder:
            manual_file = self.folder + '/git-lfs.csv'
            print 'git-lfs'
        if 'linguist' in self.folder:
            manual_file = self.folder + '/linguist.csv'
            print 'linguist'

        reader_pull = csv.DictReader(open(pulls_summary_file, 'r'))
        reader_manual = csv.DictReader(open(manual_file, 'r'))
        writer = csv.DictWriter(open(pulls_summary_file_updated, 'w'), fieldnames=reader_pull.fieldnames)
        writer.writeheader()

        updates = {}
        for row_m in reader_manual:
            updates[int(row_m['pull_request'])] = row_m

        for row_p in reader_pull:
            if int(row_p['pull_request']) in updates.keys():
                row_m = updates[int(row_p['pull_request'])]
                row_p['number_of_additions'] = row_m['number_of_additions']
                row_p['number_of_deletions'] = row_m['number_of_deletions']
                row_p['number_of_files_changed'] = row_m['number_of_files_changed']

            writer.writerow(row_p)


    # Summary with informations of merged pull requests. (Source: API and pull_requests.json)
    def merged_pull_requests_summary(self):
        pulls_file = self.folder + '/pull_requests.json'
        pulls_summary_file = self.folder + '/merged_pull_requests_summary.csv'

        if os.path.isfile(pulls_file) and not os.path.isfile(pulls_summary_file):
            with open(pulls_file, 'r') as pulls:
                data = json.load(pulls)

                with open(pulls_summary_file, 'a') as output:
                    fieldnames = ['pull_request', 'number_of_commits', 'number_of_comments','number_of_reviews','user_type', 'user_login', 'merged_at', 'number_of_additions', 'number_of_deletions','number_of_files_changed','number_of_days', 'message']
                    writer = csv.DictWriter(output, fieldnames=fieldnames)
                    writer.writeheader()

                    for pull_request in data:
                        if pull_request['merged_at'] != None:
                            number_of_commits = self.collector.commits_in_pull_request(pull_request['number'])
                            number_of_comments = self.collector.comments_in_pull_request(pull_request['number'])
                            number_of_reviews = self.collector.reviews_in_pull_request(pull_request['number'])
                            pull_request_data = self.collector.pull_request(pull_request['number'])

                            number_of_files_changed = None
                            number_of_additions = None
                            number_of_deletions = None
                            message = ''

                            if pull_request_data:
                                if 'changed_files' in pull_request_data:
                                    number_of_files_changed = pull_request_data['changed_files']
                                if 'additions' in pull_request_data:
                                    number_of_additions = pull_request_data['additions']
                                if 'deletions' in pull_request_data:
                                    number_of_deletions = pull_request_data['deletions']
                                if 'body' in pull_request_data:
                                    if pull_request_data['body'] != None:
                                        message = pull_request_data['body'].encode('utf-8')

                            created_at = datetime.strptime(pull_request['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                            merged_at = datetime.strptime(pull_request['merged_at'], '%Y-%m-%dT%H:%M:%SZ')
                            number_of_days = (merged_at - created_at).days

                            if pull_request['user']['site_admin'] == True:
                                writer.writerow({'pull_request': pull_request['number'], 'number_of_commits': len(number_of_commits), 'number_of_comments': len(number_of_comments), 'number_of_reviews': len(number_of_reviews), 'user_type': 'Internals', 'user_login': pull_request['user']['login'], 'merged_at':pull_request['merged_at'], 'number_of_additions': number_of_additions, 'number_of_deletions': number_of_deletions, 'number_of_files_changed': number_of_files_changed, 'number_of_days': number_of_days, 'message': message})
                            else:
                                writer.writerow({'pull_request': pull_request['number'], 'number_of_commits': len(number_of_commits), 'number_of_comments': len(number_of_comments), 'number_of_reviews': len(number_of_reviews), 'user_type': 'Externals', 'user_login': pull_request['user']['login'], 'merged_at':pull_request['merged_at'], 'number_of_additions': number_of_additions, 'number_of_deletions': number_of_deletions, 'number_of_files_changed': number_of_files_changed, 'number_of_days': number_of_days, 'message': message})

    # Summary with informations of closed pull requests. (Source: API and pull_requests.json)
    def closed_pull_requests_summary(self):
        pulls_file = self.folder + '/pull_requests.json'
        pulls_summary_file = self.folder + '/closed_pull_requests_summary.csv'

        if os.path.isfile(pulls_file) and not os.path.isfile(pulls_summary_file):
            with open(pulls_file, 'r') as pulls:
                data = json.load(pulls)

                with open(pulls_summary_file, 'a') as output:
                    fieldnames = ['pull_request', 'number_of_commits', 'number_of_comments','number_of_reviews','user_type', 'user_login', 'closed_at', 'number_of_additions', 'number_of_deletions','number_of_files_changed','number_of_days', 'message']
                    writer = csv.DictWriter(output, fieldnames=fieldnames)
                    writer.writeheader()

                    for pull_request in data:
                        if pull_request['state'] == 'closed' and pull_request['merged_at'] == None:
                            try:
                                number_of_commits = self.collector.commits_in_pull_request(pull_request['number'])
                                number_of_comments = self.collector.comments_in_pull_request(pull_request['number'])
                                number_of_reviews = self.collector.reviews_in_pull_request(pull_request['number'])
                                pull_request_data = self.collector.pull_request(pull_request['number'])

                                number_of_files_changed = None
                                number_of_additions = None
                                number_of_deletions = None
                                message = ''

                                if pull_request_data:
                                    if 'changed_files' in pull_request_data:
                                        number_of_files_changed = pull_request_data['changed_files']
                                    if 'additions' in pull_request_data:
                                        number_of_additions = pull_request_data['additions']
                                    if 'deletions' in pull_request_data:
                                        number_of_deletions = pull_request_data['deletions']
                                    if 'body' in pull_request_data:
                                        if pull_request_data['body'] != None:
                                            message = pull_request_data['body'].encode('utf-8')

                                created_at = datetime.strptime(pull_request['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                                closed_at = datetime.strptime(pull_request['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                                number_of_days = (closed_at - created_at).days

                                if pull_request['user']['site_admin'] == True:
                                    writer.writerow({'pull_request': pull_request['number'], 'number_of_commits': len(number_of_commits), 'number_of_comments': len(number_of_comments), 'number_of_reviews': len(number_of_reviews), 'user_type': 'Internals', 'user_login': pull_request['user']['login'], 'closed_at': closed_at, 'number_of_additions': number_of_additions, 'number_of_deletions': number_of_deletions, 'number_of_files_changed': number_of_files_changed, 'number_of_days': number_of_days, 'message': message})
                                else:
                                    writer.writerow({'pull_request': pull_request['number'], 'number_of_commits': len(number_of_commits), 'number_of_comments': len(number_of_comments), 'number_of_reviews': len(number_of_reviews), 'user_type': 'Externals', 'user_login': pull_request['user']['login'], 'closed_at': closed_at, 'number_of_additions': number_of_additions, 'number_of_deletions': number_of_deletions, 'number_of_files_changed': number_of_files_changed, 'number_of_days': number_of_days, 'message': message})
                            except Exception as ex:
                                with open('errors.log', 'a') as errors:
                                    errors.write(ex)
                                    errors.write('\n Repository:' + self.folder + '\n')


    # Reviews from merged pull requests. (Source: API and pull_requests.json)
    def merged_pull_requests_reviews(self):
        pulls_file = self.folder + '/pull_requests.json'
        reviews_file = self.folder + '/merged_reviews.csv'
        fieldnames = ['pull_request', 'creator', 'creator_type', 'reviewer', 'reviewer_type', 'is_equal']

        if os.path.isfile(pulls_file):
            with open(reviews_file, 'a') as output:
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()

                with open(pulls_file, 'r') as pulls:
                    data = json.load(pulls)

                    for pull_request in data:
                        if pull_request['merged_at'] != None:
                            p = self.collector.pull_request(pull_request['number'])

                            creator = p['user']['login']

                            # We moved this developers to the internals because we found qualitative evidences that they worked at GitHub
                            if 'atom' in self.folder:
                                if p['user']['login'] == 'benogle' or p['user']['login'] == 'thedaniel' or p['user']['login'] == 'jlord':
                                    p['user']['site_admin'] = True
                            if 'hubot' in self.folder:
                                if p['user']['login'] == 'bhuga' or p['user']['login'] == 'aroben':
                                    p['user']['site_admin'] = True
                            if 'linguist' in self.folder:
                                if p['user']['login'] == 'arfon' or p['user']['login'] == 'aroben' or p['user']['login'] == 'tnm' or p['user']['login'] == 'brandonblack' or p['user']['login'] == 'rick':
                                    p['user']['site_admin'] = True            
                            if 'electron' in self.folder:
                                if p['user']['login'] == 'miniak' or p['user']['login'] == 'codebytere':
                                    p['user']['site_admin'] = True

                            if p['user']['site_admin'] == True:
                                creator_type = 'Internals'
                            else:
                                creator_type = 'Externals'

                            reviewer = p['merged_by']['login']

                            # We moved this developers to the internals because we found qualitative evidences that they worked at GitHub
                            if 'atom' in self.folder:
                                if p['merged_by']['login'] == 'benogle' or p['merged_by']['login'] == 'thedaniel' or p['merged_by']['login'] == 'jlord':
                                    p['merged_by']['site_admin'] = True
                            if 'hubot' in self.folder:
                                if p['merged_by']['login'] == 'bhuga' or p['merged_by']['login'] == 'aroben':
                                    p['merged_by']['site_admin'] = True
                            if 'linguist' in self.folder:
                                if p['merged_by']['login'] == 'arfon' or p['merged_by']['login'] == 'aroben' or p['merged_by']['login'] == 'tnm' or p['merged_by']['login'] == 'brandonblack' or p['merged_by']['login'] == 'rick':
                                    p['merged_by']['site_admin'] = True            
                            if 'electron' in self.folder:
                                if p['merged_by']['login'] == 'miniak' or p['merged_by']['login'] == 'codebytere':
                                    p['merged_by']['site_admin'] = True    

                            if p['merged_by']['site_admin'] == True:
                                reviewer_type = 'Internals'
                            else:
                                reviewer_type = 'Externals'

                            if creator == reviewer:
                                is_equal = 'Yes'
                            else:
                                is_equal = 'No'

                            writer.writerow({'pull_request': pull_request['number'], 'creator': creator, 'creator_type': creator_type, 'reviewer': reviewer, 'reviewer_type': reviewer_type, 'is_equal': is_equal})

def repositories_in_parallel(project):
    collector = GitRepository.Repository(project['organization'], project['name'], crawler)
    folder = dataset_folder + project['name']

    R = Repository(collector, folder)
    # R.about()
    # R.pull_requests()
    # R.contributors()
    # R.merged_pull_requests_summary()
    R.closed_pull_requests_summary()
    # R.merged_pull_requests_reviews()
    # R.update_manual_values()

if __name__ == '__main__':
    dataset_folder = 'Dataset/'
    projects = [
    {'organization':'electron','name':'electron'},
    {'organization':'github','name':'linguist'},
    {'organization':'git-lfs','name':'git-lfs'},
    {'organization':'hubotio','name':'hubot'},
    {'organization':'atom','name':'atom'}
    ]

    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)

    api_client_id = '4161a8257efaea420c94' # Please, specify your own client id
    api_client_secret = 'd814ec48927a6bd62c55c058cd028a949e5362d4' # Please, specify your own client secret
    crawler = GitCrawler.Crawler(api_client_id, api_client_secret)

    # Multiprocessing technique
    parallel = multiprocessing.Pool(processes=4) # Define number of processes
    parallel.map(partial(repositories_in_parallel), projects)

