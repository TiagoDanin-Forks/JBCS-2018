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

    # Collects general information about a project (Source: GitHub API)
    def about(self):
        about_file = self.folder + '/about.json'

        if not os.path.isfile(about_file):
            about = self.collector.get()

            with open(about_file, 'w') as file:
                json.dump(about, file, indent = 4)

    # Collects all the project's pull requests. (Source: GitHub API)
    def pull_requests(self):
        pulls_file = self.folder + '/pull_requests.json'

        if not os.path.isfile(pulls_file):
            pull_requests = self.collector.pull_requests(state='all')
    
            with open(pulls_file, 'w') as file:
                json.dump(pull_requests, file, indent = 4)

    # Collects all the project's contributors. (Source: GitHub API)
    def contributors(self):
        contributors_file = self.folder + '/contributors.json'

        if not os.path.isfile(contributors_file):
            contributors = self.collector.contributors(anonymous='true')

            with open(contributors_file, 'w') as file:
                json.dump(contributors, file, indent = 4)
        else:
            data = json.load(open(contributors_file,'r'))
            num_externals = 0
            num_internals = 0

            for contributor in data:
                if 'site_admin' in contributor.keys():
                    if contributor['site_admin'] == True:
                        num_internals = num_internals + 1
                    if contributor['site_admin'] == False:
                        num_externals = num_externals + 1

            print self.folder
            print 'Total: ' + str(len(data))
            print 'Internals: ' + str(num_internals)
            print 'Externals: ' + str(num_externals)

    # Creates a summary of pull request's information. (Source: pull_requests.json)
    # Contains: user position (volunteer/employee), user login, pull request merged date, num. of commits, comments and reviews.
    def merged_pull_requests_summary(self):
        pulls_file = self.folder + '/pull_requests.json'
        pulls_summary_file = self.folder + '/merged_pull_requests_summary.csv'

        if os.path.isfile(pulls_file) and not os.path.isfile(pulls_summary_file):
            with open(pulls_file, 'r') as pulls:
                data = json.load(pulls)

                with open(pulls_summary_file, 'a') as output:
                    fieldnames = ['pull_request', 'number_of_commits', 'number_of_comments','number_of_reviews','user_type', 'user_login', 'merged_at', 'number_of_additions', 'number_of_deletions','number_of_files_changed','number_of_days']
                    writer = csv.DictWriter(output, fieldnames=fieldnames)
                    writer.writeheader()

                    for pull_request in data:
                        if pull_request['merged_at'] != None:
                            number_of_commits = self.collector.commits_in_pull_request(pull_request['number'])
                            number_of_comments = self.collector.comments_in_pull_request(pull_request['number'])
                            number_of_reviews = self.collector.reviews_in_pull_request(pull_request['number'])

                            number_of_additions = 0
                            number_of_deletions = 0
                            number_of_files_changed = 0

                            created_at = datetime.strptime(pull_request['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                            merged_at = datetime.strptime(pull_request['merged_at'], '%Y-%m-%dT%H:%M:%SZ')
                            delta = merged_at - created_at

                            for commit in number_of_commits:
                                url = commit['url']
                                commit_information = self.collector.commit_information(url)

                                if 'stats' in commit_information:
                                    number_of_additions = number_of_additions + int(commit_information['stats']['additions'])
                                    number_of_deletions = number_of_deletions + int(commit_information['stats']['deletions'])
                                if 'files' in commit_information:
                                    number_of_files_changed = number_of_files_changed + len(commit_information['files'])

                            if pull_request['user']['site_admin'] == True:
                                writer.writerow({'pull_request': pull_request['number'], 'number_of_commits': len(number_of_commits), 'number_of_comments': len(number_of_comments), 'number_of_reviews': len(number_of_reviews), 'user_type': 'Internals', 'user_login': pull_request['user']['login'], 'merged_at':pull_request['merged_at'], 'number_of_additions': number_of_additions, 'number_of_deletions': number_of_deletions, 'number_of_files_changed': number_of_files_changed, 'number_of_days': delta.days})
                            else:
                                writer.writerow({'pull_request': pull_request['number'], 'number_of_commits': len(number_of_commits), 'number_of_comments': len(number_of_comments), 'number_of_reviews': len(number_of_reviews), 'user_type': 'Externals', 'user_login': pull_request['user']['login'], 'merged_at':pull_request['merged_at'], 'number_of_additions': number_of_additions, 'number_of_deletions': number_of_deletions, 'number_of_files_changed': number_of_files_changed, 'number_of_days': delta.days})
        else:
            if os.path.isfile(pulls_summary_file):
                input_file = csv.DictReader(open(pulls_summary_file, 'r'))
                output_file = csv.DictWriter(open(self.folder + '/merged_pull_requests_summary_updated.csv', 'a'), fieldnames=input_file.fieldnames + ['message'])
                output_file.writeheader()

                for pull_request in input_file:
                    pull_data = self.collector.pull_request(pull_request['number'])
                    pull_request['message'] = 
                    output_file.writerow(pull_request)


    def merged_pull_requests_reviews(self):
        pulls_file = self.folder + '/pull_requests.json'
        reviews_file = self.folder + '/reviews.csv'
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
    # R.merged_pull_requests_summary()
    # R.merged_pull_requests_reviews()
    R.contributors()

if __name__ == '__main__':
    dataset_folder = 'Dataset/'
    projects = [{'organization':'electron','name':'electron'},
    {'organization':'github','name':'linguist'},
    {'organization':'git-lfs','name':'git-lfs'},
    {'organization':'hubotio','name':'hubot'},
    {'organization':'atom','name':'atom'}]

    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)

    api_client_id = '4161a8257efaea420c94' # Please, specify your own client id
    api_client_secret = 'd814ec48927a6bd62c55c058cd028a949e5362d4' # Please, specify your own client secret
    crawler = GitCrawler.Crawler(api_client_id, api_client_secret)

    # Multiprocessing technique
    parallel = multiprocessing.Pool(processes=1) # Define number of processes
    parallel.map(partial(repositories_in_parallel), projects)

