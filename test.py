# Read in from csv
# with open('sample_input.csv', 'r', encoding='gbk') as f:
#     for x in f:
#         x = x.split(',')
#         name = x[0]
#         url = x[1].strip()
#         print(name)
#         print(url)

# Test grab data from a child
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re

def name_too_long(arg):
    t = re.findall('\.\.\.',arg)
    if len(t) == 0:
        return False
    print(arg)
    return True

def is_author_column(tag):
    return (tag.string == '作者') and tag.has_attr('class') and (tag.get('class') == ['gsc_field'])

def is_magazine_column(tag):
    return (tag.string == '期刊' or tag.string == '研讨会论文') and tag.has_attr('class') and (tag.get('class') == ['gsc_field'])

def get_author_child(source):
    doc = bs(source, "lxml")
    x = doc.find(is_author_column)
    if not x:
        return ''
    x = x.find_next_sibling()
    print(x.string)
    return x.string

def get_magazine_child(source):
    doc = bs(source, "lxml")
    x = doc.find(is_magazine_column)
    if not x:
        return ''
    x = x.find_next_sibling()
    print(x.string)
    return x.string

paper_name = []
paper_author = []
paper_magazine = []

with open('person_homepage.txt', 'r', encoding='utf-8') as f:
    doc = bs(f.read(), 'lxml')
    x = doc.find_all("tr", class_="gsc_a_tr")
    len_x = len(x)
    for i in range(0,len_x):

        # grab the title of the paper
        paper_name_raw = x[i].find(class_="gsc_a_at")
        paper_name.append(paper_name_raw.string)

        # grab the authors of the paper
        paper_info_raw = x[i].find_all(class_="gs_gray")
        paper_author_add = paper_info_raw[0].string
        if not name_too_long(paper_author_add):
            paper_author.append(paper_author_add)
        else:
            url_child = paper_name_raw.get('href')
            url_child = 'https://scholar.google.com' + url_child
            dr = webdriver.PhantomJS()
            dr.get(url_child)
            source_child = dr.page_source
            dr.quit()
            paper_author.append(get_author_child(source_child))

        # grab the magazine of the paper
        magazine_raw = paper_info_raw[1]
        magazine_content = magazine_raw.contents
        if len(magazine_content) == 0:
            paper_magazine.append('')
        else:
            paper_magazine_add = magazine_content[0].string
            if not name_too_long(paper_magazine_add):
                paper_magazine.append(paper_magazine_add)
            else:
                url_child = paper_name_raw.get('href')
                url_child = 'https://scholar.google.com' + url_child
                dr = webdriver.PhantomJS()
                dr.get(url_child)
                source_child = dr.page_source
                dr.quit()
                paper_magazine.append(get_magazine_child(source_child))