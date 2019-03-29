# Cuz the shitty proxies
import os

proxies = {'https': 'https://172.31.2.3:8080',
           'http': 'http://172.31.2.3:8080',
           'ftp': 'ftp://172.31.2.3:8080'}
for proxy in proxies:
    os.environ[proxy + '_proxy'] = proxies[proxy]

import requests

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