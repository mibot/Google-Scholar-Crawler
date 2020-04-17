# import pymysql
# import os
# import re
# import pandas as pd
#
# dataPath = os.path.abspath(os.path.relpath('../data'))
#
# db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
#                      user="root",  # your username
#                      passwd="iwJx0EAM",  # your password
#                      db="clpd")  # name of the data base
#
# cur = db.cursor()
#
# def getPapers_0():
#     sql = 'select id, title from resolved_papers where downloaded = 0;'
#     papers = pd.read_sql(sql, con=db)
#
#
#
#
#
# if __name__ == '__main__':
#     getPapers_0()

from bs4 import BeautifulSoup

import requests
import re

# url = raw_input("http://citeseerx.ist.psu.edu/search?q=attitude&submit=Search&sort=rlv&t=doc")

r  = requests.get("http://citeseerx.ist.psu.edu/search?q=attitude&submit=Search&sort=rlv&t=doc")

data = r.text

soup = BeautifulSoup(data)
# soup.prettify

papers_on_page = soup.findAll('a', {'class':'remove doc_details'})

for paper_on_page in papers_on_page:
    print(paper_on_page.get('href'))

string = '/viewdoc/summary;jsessionid=4C1CD7E8F0D4A4E4BABAE601DE8D326F?doi=10.1.1.317.9673&rank=1'
# print(string)

paper_suffix = re.sub(';.*\?', '?', string)

paper_url = 'http://citeseerx.ist.psu.edu' + paper_suffix
print(paper_url)

r  = requests.get('http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.317.9673&rank=1')

data = r.text

soup = BeautifulSoup(data)

soup.findAll('div', id='docAuthors')

url_pdf = 'http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.477.1021&rep=rep1&type=pdf'

res = requests.get(url_pdf)
content_type = res.headers.get('content-type')