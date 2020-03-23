# issue-automator
Automatically create issues from a csv. This program will read a csv file that you provide the relative path to. Using your github personal access token, the application will authenticate with the github api and create issues in the desired repository, so long as your github token has permissions for that repository. 

The input csv should have at least 2 column headers:
`id,title`.

The title is used to create the issue title. The id column should be left blank. This program will overwrite the csv when complete with the updated issue id relative to the target repository. That way, you can add new issues to the csv without having to create new csv files. The creation of issues is idempotent.

Any other headers you add beyond `id,title` will become attributes of the issue body in the format:
```
attribute1: row value,
attribute2: row value,
```

# Usage
```
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
```


e.g.
`python create_issues.py $GITHUB_TOKEN test.csv txross issue-automator`