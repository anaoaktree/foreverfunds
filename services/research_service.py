from github import Github
import base64, os

def insertion_sort(files, new_file):
    name, time = new_file
    i = 0
    while i < len(files) and files[i][1] < time:
        i += 1
    files.insert(i, new_file)

def get_latest_research(username, password):
    documents = []
    github = Github(username, password)
    for repo in github.get_user().get_repos():
        if repo.name == 'research_example':
            documents = scan_repo(repo, '.')
    return documents

def get_pdfs_from_dir(dir):
    all_files = os.walk(dir)
    documents = []
    for dir, _, files in all_files:
        for file in files:
            if file.endswith('.pdf'):
                insertion_sort(documents, (file, os.stat(dir + '/'+file).st_mtime))
    documents = [x for (x, y) in documents]
    return documents


# recursively getting all pdfs
def scan_repo(repo, path):
    documents = []
    for file in repo.get_contents(path):
        if file.name.endswith('.pdf'):
            documents.append((file.name, base64.b64decode(file.content)))
        elif '.' not in file.name:
            documents += scan_repo(repo, file.path)
    return documents

