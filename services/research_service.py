import os


def insertion_sort(files, new_file):
    name, time = new_file
    i = 0
    while i < len(files) and files[i][1] < time:
        i += 1
    files.insert(i, new_file)



def get_pdfs_from_dir(dir):
    all_files = os.walk(dir)
    documents = []
    for dir, _, files in all_files:
        for file in files:
            if file.endswith('.pdf'):
                insertion_sort(documents, (file, os.stat(dir + '/'+file).st_mtime))
    documents = [x for (x, y) in documents]
    return documents

def get_path(file_name):
    all_files = os.walk('./research_docs')
    path = None
    for dir, _, files in all_files:
        if file_name in files:
            path = dir
            break
    return path+'/'+file_name