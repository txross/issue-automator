#!/bin/python
import requests, csv, json, sys, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
GITHUB_ENDPOINT = 'https://api.github.com/repos'
ISSUE_TEMPLATE = {'title': '', 'body': ''}

def issue_exists(repo_owner, repo_name, issue_number, token):
    url = '{}/{}/{}/issues/{}'.format(GITHUB_ENDPOINT,repo_owner, repo_name,issue_number)
    headers = {'Authorization': 'token {}'.format(token)}
    r = requests.get(url, headers=headers, verify=False)
    return (r.status_code == 200)

def create_issue(issue, token, repo_owner, repo_name):
    url = '{}/{}/{}/issues'.format(GITHUB_ENDPOINT, repo_owner, repo_name)
    headers = {'Authorization': 'token {}'.format(token)}
    r = requests.post(url, json.dumps(issue), headers=headers, verify=False)
    if r.status_code == 201:
        print( 'Successfully created Issue "%s"' % issue['title'])
        resp = json.loads(r.content)
        return resp['number']
    else:
        print('Could not create Issue "%s"' % issue['title'])
        print('Response:', r.content)

def define_issue(headers, row):
    issue = ISSUE_TEMPLATE.copy()
    issue['title'] = row['title']
    
    if len(headers) > 2:
        body = get_issue_body(headers[2:], row)

    issue['body'] = body
    return issue

def get_issue_body(headers, row):
    body = ""
    for i in range(len(headers)):
        body += "{}: {}\n".format(headers[i], row[headers[i]])
    return body

def usage():
    return """
    Usage:
    python create_issues.py token csv_file repo_owner repo_name

    Provide the following arguments:
        token       Github Personal Access Token used to authenticate with the github api
                    Learn how to create one here: 
                    https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line

        csv_file    relative path of a comma-delimited, utf-8 encoded csv containing the header
                    id, title, [any number of fields for the issue body]
        
        repo_owner  the name of the owner of repo_name
                    e.g. txross
        
        repo_name   the name of the github repository to create issues in
                    e.g. issue-automator

        
    """

def main():
    """ Reads csv and create issues for each row. Update id column in csv. """
    
    if len(sys.argv) < 5:
        print(usage())
        exit(1)

    token = sys.argv[1]
    csv_file = sys.argv[2]
    repo_owner = sys.argv[3]    
    repo_name = sys.argv[4]

    table = []
    headers = []
    with open(csv_file, newline='') as f:
        data = csv.DictReader(f)
        table = [row for row in data]
        headers = data.fieldnames

    for row in table:
        issue = define_issue(headers, row)
        print(issue)
        if issue_exists(repo_owner, repo_name, row['id'], token):
            print("issue {} exists. Skipping...".format(row['id']))
            continue
        id = create_issue(issue, token, repo_owner, repo_name)
        row['id'] = id
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in table:
            writer.writerow(row)


if __name__ == "__main__":
    main()