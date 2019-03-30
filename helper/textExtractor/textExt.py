import fitz
import re
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
