import os
import sys
import base64
import datetime

from github import Github

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import BytesIO

# local access functions.

def insertion_sort(files, new_file, path):
    name, time = new_file
    fp = open(path, 'rb')
    title, abstract = get_title_abstract(fp)
    i = 0
    while i < len(files) and files[i]['time'] < time:
        i += 1
    files.insert(i, {'filename':name, 'title':title, 'abstract':abstract, 'time':time})



def get_pdfs_from_dir(dir):
    all_files = os.walk(dir)
    documents = []
    for dir, _, files in all_files:
        if 'figs' not in dir:
            for file in files:
                if file.endswith('.pdf'):
                    insertion_sort(documents, (file, os.stat(dir + '/'+file).st_mtime), dir + '/'+file)
    for file in documents:
        file.pop('time', None)
    return documents

def get_path(file_name):
    all_files = os.walk('./research_docs')
    path = None
    for dir, _, files in all_files:
        if file_name in files:
            path = dir
            break
    return path+'/'+file_name


# pdf reading and processing functions

def get_title_abstract(fp):
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.all_texts = True
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    extracted_text = ''
    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()
    if len(extracted_text) == 0:
        return '', ''
    splited_extracted_text = extracted_text.split('\n')
    title = splited_extracted_text[2]
    abstract = ''
    i = 3
    while len(abstract) < 350:
        abstract += splited_extracted_text[i] + ' '
        i += 1
    abstract += '...'
    return title, abstract


# methods for github

def get_latest_research(user, passwd):
    github = Github(user, passwd)
    documents = []
    for repo in github.get_user().get_repos():
        if repo.name == 'research_example':
            for file in repo.get_contents('db/research'):
                data = file.raw_data
                if type(data) is dict and '.pdf' in data.name:
                    insertion_sort2(documents, get_research_dict(file))
                elif type(data) is list:
                    docs =  get_research_list(data, repo)
                    for doc in docs:
                        insertion_sort2(documents, doc)
    return documents


def get_research_dict(file):
    """

    :param file: the pdf from github we want to process
    :return: dictionary with the relevant information about the pdf
    """
    time = datetime.datetime.strptime(file.last_modified, '%a, %d %b %Y %H:%M:%S GMT')
    file = file.raw_data
    name = file.get('name')
    data = base64.b64decode(file.get('content'))
    title, abstract = get_title_abstract(BytesIO(data))
    path = file.get('path')
    return {'filename': name, 'time': time, 'title': title, 'abstract': abstract, 'path': path}


def get_research_list(directory, repo):
    documents = []
    for file in directory:
        if '.pdf' in file.get('name'):
            actual_file = repo.get_contents(file.get('path'))
            documents.append(get_research_dict(actual_file))
    return documents


def insertion_sort2(documents, research):
    i = 0
    while i < len(documents) and documents[i]['time'] < research['time']:
        i += 1
    documents.insert(i, research)

def get_content(path, user, passwd):
    github = Github(user, passwd)
    repo = github.get_user().get_repo('research_example')
    file = repo.get_contents(path)
    data = base64.b64decode(file.content)
    return data
