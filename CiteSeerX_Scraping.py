#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time
from multiprocessing.pool import ThreadPool
from random import randint
from urllib.parse import urlencode

import pymysql
from base import db, cur
from bs4 import BeautifulSoup
import requests
from user_agent_list import get_random_ua
from proxy_list_gen import get_random_proxy
import pandas as pd
import unicodedata

requests.packages.urllib3.disable_warnings()

SCHOLARS_BASE_URL = 'http://citeseerx.ist.psu.edu'


# db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
#                      user="root",  # your username
#                      passwd="iwJx0EAM",  # your password
#                      db="clpd")  # name of the data base
#
# cur = db.cursor()
#
# sql = "SELECT id, title FROM `resolved_papers` WHERE `source` LIKE '%http://aclweb.org%' and downloaded = 0;"
# papers = pd.read_sql(sql, con=db)
#
# for index, row in papers.iterrows():
#
#     # title = 'From words to corpora: Recognizing translation'
#     # query = title
#     query = row['title']
#
#
#     params = urlencode(
#         {'q': query.lower()},
#         "UTF-8")
#
#     url = SCHOLARS_BASE_URL + "/search?" + params
#
#     print(url)
#
#     ua = str(get_random_ua())
#     # print(ua)
#
#     # proxy = str(get_random_proxy())
#     # print(proxy)
#
#     try:
#         response = requests.get(
#             url,
#             headers={
#                 'User-Agent': ua
#             }
#         )
#     except:
#         print("Connection refused")
#         time.sleep(5)
#         continue
#
#     print(response.status_code)
#     if response.status_code == 200:
#
#         data = response.text
#         soup = BeautifulSoup(data, "html.parser")
#
#         item = soup.find_all('div', {'class': 'result'})[0]
#
#         if item:
#             link = str(item.contents[1]).split('\n')
#             title = ""
#             title = re.sub('<[^<]+?>', '', link[2])
#         else:
#             continue
#
#         if query.lower() == title.lower():
#
#             # string = '/viewdoc/summary;jsessionid=4C1CD7E8F0D4A4E4BABAE601DE8D326F?doi=10.1.1.317.9673&rank=1'
#             # suffix = re.sub(';.*\?', '?', string)
#             # suffix = suffix.replace('summary', 'download').replace('&rank=1', '&rep=rep1&type=pdf')
#
#             soup = BeautifulSoup(link[1])
#             a = soup.find("a", class_="remove doc_details")
#             string = a.attrs['href']
#
#
#             suffix = re.sub(';.*\?', '?', string)
#             suffix = suffix.replace('summary', 'download').replace('&rank=1', '&rep=rep1&type=pdf')
#
#             url_pdf = SCHOLARS_BASE_URL + suffix
#             print(url_pdf)
#
#             res = requests.get(url_pdf)
#             content_type = res.headers.get('content-type')
#
#             if 'application/pdf' in str(content_type):
#                 destination = '/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/pdf/tocheck/'
#                 path = destination + str(row['id']) + '.pdf'
#
#                 with open(path, 'wb') as f:
#                     f.write(res.content)
#
#             sql = "update resolved_papers set downloaded = 1 where id = %s" % (row['id'])
#
#             try:
#                 cur.execute(sql)
#                 db.commit()
#                 print("Id: %s. Downloaded: True. Saved!" % (row['id']))
#             except:
#                 db.rollback()
#
#
#         else:
#             print('Title is not found with identifier %s'
#                   % (row['id']))
#     time.sleep(randint(1, 6))

def _download(ids):
    db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                         user="root",  # your username
                         passwd="iwJx0EAM",  # your password
                         db="clpd")  # name of the data base

    cur = db.cursor()

    try:
        id, query = ids

        params = urlencode(
            {'q': query.lower()},
            "UTF-8")

        url = SCHOLARS_BASE_URL + "/search?" + params

        print(url)

        ua = str(get_random_ua())

        try:
            response = requests.get(
                url,
                headers={
                    'User-Agent': ua
                }
            )
        except:
            print("Connection refused")
            time.sleep(5)

        print(response.status_code)
        if response.status_code == 200:

            data = response.text
            soup = BeautifulSoup(data, "html.parser")

            item = soup.find_all('div', {'class': 'result'})[0]

            if item:
                link = str(item.contents[1]).split('\n')
                title = ""
                title = re.sub('<[^<]+?>', '', link[2])

            if query.lower() == title.lower():

                # string = '/viewdoc/summary;jsessionid=4C1CD7E8F0D4A4E4BABAE601DE8D326F?doi=10.1.1.317.9673&rank=1'
                # suffix = re.sub(';.*\?', '?', string)
                # suffix = suffix.replace('summary', 'download').replace('&rank=1', '&rep=rep1&type=pdf')

                soup = BeautifulSoup(link[1])
                a = soup.find("a", class_="remove doc_details")
                string = a.attrs['href']

                suffix = re.sub(';.*\?', '?', string)
                suffix = suffix.replace('summary', 'download').replace('&rank=1', '&rep=rep1&type=pdf')

                url_pdf = SCHOLARS_BASE_URL + suffix
                print(url_pdf)

                res = requests.get(url_pdf)
                content_type = res.headers.get('content-type')

                if 'application/pdf' in str(content_type):
                    destination = '/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/pdf/tocheck/'
                    path = destination + str(id) + '.pdf'

                    with open(path, 'wb') as f:
                        f.write(res.content)

                sql = "update resolved_papers set downloaded = 1 where id = %s" % (id)

                try:
                    cur.execute(sql)
                    db.commit()
                    print("Id: %s. Downloaded: True. Saved!" % (id))
                except:
                    db.rollback()


            else:
                print('Title is not found with identifier %s'
                      % (id))
    except:
        print('Failed to fetch citeseerx page with identifier %s due to request exception.'
                       % (id))

    time.sleep(randint(1, 6))


def main():
    sql = 'select p.id, p.title FROM `resolved_papers` p inner join `resolved_papers_title` pt on pt.Id = p.Id WHERE downloaded = 0 and pt.`title_language` = "en" and p.id >= 38304;'
    papers = pd.read_sql(sql, con=db)
    ids = list(zip(*[papers[c].values.tolist() for c in papers]))

    pool = ThreadPool()

    print(pool.imap_unordered(_download, ids))
    pool.close()

    pool.join()

if __name__ == '__main__':
    main()

# 10.1.1.100.9010


# https://link.springer.com/article/10.1007/s10579-014-9282-3
# https://link.springer.com/content/pdf/10.1007%2Fs10579-014-9282-3.pdf

