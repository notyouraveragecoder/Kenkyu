import re
import fitz
import requests

# Find the trending papers from Arxiv
import json

def trendingPapers():
    r = requests.get(r'http://www.arxiv-sanity.com/toptwtr?timefilter=week')
    var_papers = re.compile(r'''var papers = (.*);
var''')
    data = var_papers.findall(r.text)[0]
    json_data = json.loads(data)
    return json_data


#Extract the textual data from the PDF
size_re = re.compile(r"'size': (\d+)")
content_re = re.compile(r"'text': '(.*?)'")

def findActualContent(documentName):
    all_content = []
    doc = fitz.open(documentName)
    for page in doc:
        size_dict = {}
        line_dict = {}
        page = str(page.getText('dict'))
        sizes = size_re.findall(page)
        lines = content_re.findall(page)
        for index, line in enumerate(lines):
            line_dict[line] = sizes[index]
        for size in sizes:
            size_dict.setdefault(size, 0)
            size_dict[size] = size_dict[size] + 1
        mostfreq = max(size_dict, key=size_dict.get)
        content = ''
        print(line_dict)
        for elem in line_dict:
            try:
                if line_dict[elem] == mostfreq:
                    content = content + ". " + elem
            except Exception as e:
                pass
        print(content)
        content = content.replace('..', '.')
        all_content.append(content)
    return all_content


#Extract Images
# Refrence - https://github.com/pymupdf/PyMuPDF/wiki/How-to-Extract-Images-from-a-PDF
def extractImages(documentName):
    doc = fitz.open(documentName)
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.writePNG("p%s-%s.png" % (i, xref))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None


#Most Important Reference
def findImpReference(documentName):
    doc = fitz.open(documentName)


# Cuz the shitty proxies
import os

proxies = {'https': 'https://172.31.2.3:8080',
           'http': 'http://172.31.2.3:8080',
           'ftp': 'ftp://172.31.2.3:8080'}
for proxy in proxies:
    os.environ[proxy + '_proxy'] = proxies[proxy]


# Default Query Statements
wikiQuery = '''https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={}&format=json'''
wikiExtract = '''https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={}'''

def findResults(query):
    source = requests.get(wikiQuery.format(query))
    source_json = source.json()
    print("Top three results are ")
    resultList = []
    for index, elem in enumerate(source_json['query']['search']):
        if index > 3:
            break
        print(elem['title'])
        resultList.append(elem['title'])
    return resultList


def showMeaning(query):
    source = requests.get(wikiExtract.format(query))
    source_json = source.json()
    meaning = source_json['query']['pages'][list(source_json['query']['pages'].keys())[0]]['extract']
    return meaning


# Search and Download Paper

def searchDownload(query):
    arxivQuery = "http://www.arxiv-sanity.com/search?q={}".format(query)
    var_paper = re.compile(r"""var papers = (.*);
var""")
    r = requests.get(arxivQuery)
    data = var_paper.findall(r.text)[0]
    data_json = json.loads(data)
    if 'arxiv.org/abs' in data_json[0]['link']:
        pdf_link = data_json[0]['link'].replace('abs', 'pdf')
        return pdf_link
        # response = requests.get(pdf_link)
        # with open('/{}.pdf'.format(query), 'wb') as f:
        #     f.write(response.content)
    else:
        return data_json[0]['link']


# Helper Main

def understand(sentence):
    default_statements = {
        'ABSTRACT': 'What is this research paper about?',
        'RECOMMENDATION': 'Can I find some more research papers like this?',
        'DEFINITION': 'Can you tell me the meaning of this?',
        'TRENDS': "What's trending?",
        'NOTE': 'Make a note!',
        'SUB_QUESTION': 'What is this?',
        'FILE_EXP': 'Can you open a file?',
        'TRENDING': 'What are some trending research papers?',
        'SCRAPE_IMAGE': 'I want to scrape all the images',
        'SEARCH_DOWNLOAD': 'I want to download this paper'
    }
    max_like = 0
    max_like_index = 0
    compare1 = sentence.lower().split(' ')
    for elem in default_statements:
        compare2 = default_statements[elem].lower().split(' ')
        if len(set(compare1) & set(compare2)) > max_like:
            max_like = len(set(compare1) & set(compare2))
            max_like_index = elem
    return max_like_index


