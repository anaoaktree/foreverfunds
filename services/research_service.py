import os

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine


# local access functions.

def insertion_sort(files, new_file, path):
    name, time = new_file
    title, abstract = get_title_abstract(path)
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

def get_title_abstract(pdf_file):
    print(pdf_file)
    fp = open(pdf_file, 'rb')
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