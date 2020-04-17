#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
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

SCHOLARS_BASE_URL = 'http://link.springer.com'

def _downloadSpringer(ids):
    db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                         user="root",  # your username
                         passwd="iwJx0EAM",  # your password
                         db="clpd")  # name of the data base

    cur = db.cursor()

    try:
        id, main_link, direct_link = ids
        # direct_link = 'http://link.springer.com/article/10.1007/s10579-014-9282-3'

        # SPRINGER #

        if 'article' in main_link:
            # https://link.springer.com/article/10.1007/s10579-014-9282-3
            # https://link.springer.com/content/pdf/10.1007%2Fs10579-014-9282-3.pdf
            url_pdf = main_link.replace('article', 'content/pdf') + '.pdf'

        elif 'chapter' in main_link:
            # http://link.springer.com/chapter/10.1007/978-3-319-09846-3_4/fulltext.html
            # https://link.springer.com/content/pdf/10.1007%2F978-3-319-09846-3.pdf
            # direct_link = main_link.replace('/fulltext.html', '')
            url_pdf = main_link.replace('chapter', 'content/pdf') + '.pdf'

        # # IEEE
        #
        # paper_id = (re.findall('\d+', main_link))[0]
        # url_pdf = 'http://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber=%s' % (paper_id)
        # print(url_pdf)


        ua = str(get_random_ua())

        try:
            response = requests.get(
                url_pdf,
                headers={
                    'User-Agent': ua
                }
            )
        except:
            print("Connection refused")
            time.sleep(5)


        print(response.status_code)
        if response.status_code == 200:

            content_type = response.headers.get('content-type')

            if 'application/pdf' in str(content_type):
                destination = '/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/pdf/tocheck/'
                path = destination + str(id) + '.pdf'

                with open(path, 'wb') as f:
                    f.write(response.content)

                sql = "update resolved_papers set downloaded = 1 where id = %s" % (id)

                try:
                    cur.execute(sql)
                    db.commit()
                    print("Id: %s. Downloaded: True. Saved!" % (id))
                except:
                    db.rollback()

            else:
                print('Title with identifier %s not found'
                      % (id))
    except:
        print('Failed to fetch citeseerx page with identifier %s due to request exception.'
                       % (id))

    time.sleep(randint(1, 6))

def _downloadIEEE():
    db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                         user="root",  # your username
                         passwd="iwJx0EAM",  # your password
                         db="clpd")  # name of the data base

    cur = db.cursor()

    sql = "SELECT p.id, p.main_link, p.direct_link FROM `resolved_papers` p inner join `resolved_papers_title` pt on pt.Id = p.Id where p.source like '%ieee%' and p.downloaded = 0 and pt.`title_language` = 'en';"
    papers = pd.read_sql(sql, con=db)

    for index, row in papers.iterrows():


        # id, main_link, direct_link = ids
        # direct_link = 'http://link.springer.com/article/10.1007/s10579-014-9282-3'
        id = row['id']
        main_link = row['main_link']

        # IEEE

        destination = '/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/pdf/tocheck/'
        path = destination + str(id) + '.pdf'
        print(path)

        paper_id = (re.findall('\d+', main_link))[0]
        try:
            # path = '/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/pdf/tocheck/4254.pdf'
            # paper_id = '7911954'

            url_pdf = 'wget "https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber=%s" -O %s' % (paper_id, path)
            os.system(url_pdf)

            # os.system('wget "https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber=%s" -O %s') % (str(paper_id), path)
            # url_pdf = 'http://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber=%s' % (paper_id)
            # print(url_pdf)


            # ua = str(get_random_ua())
            #
            # try:
            #     response = requests.get(
            #         url_pdf,
            #         headers={
            #             'User-Agent': ua
            #         }
            #     )
            # except:
            #     print("Connection refused")
            #     time.sleep(5)
            #
            #
            # print(response.status_code)
            # if response.status_code == 200:
            #
            #     content_type = response.headers.get('content-type')
            #
            #     if 'application/pdf' in str(content_type):
            #         destination = '/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/pdf/tocheck/'
            #         path = destination + str(id) + '.pdf'
            #
            #         with open(path, 'wb') as f:
            #             f.write(response.content)
            #
            sql = "update resolved_papers set downloaded = 1 where id = %s" % (id)

            try:
                cur.execute(sql)
                db.commit()
                print("Id: %s. Downloaded: True. Saved!" % (id))
            except:
                db.rollback()

            # time.sleep(randint(1, 30))
        #
        #     else:
        #         print('Title with identifier %s not found'
        #               % (id))
        except:
            print('Failed to fetch citeseerx page with identifier %s due to request exception.'
                           % (id))

        time.sleep(randint(1, 6))

def main():

    # sql = "SELECT p.id, p.main_link, p.direct_link FROM `resolved_papers` p inner join `resolved_papers_title` pt on pt.Id = p.Id where p.source like '%ieee%' and p.downloaded = 0 and pt.`title_language` = 'en';"
    # papers = pd.read_sql(sql, con=db)
    # ids = list(zip(*[papers[c].values.tolist() for c in papers]))
    #
    # pool = ThreadPool()
    #
    # print(pool.imap_unordered(_downloadIEEE, ids))
    # pool.close()
    #
    # pool.join()

    _downloadIEEE()

if __name__ == '__main__':
    _downloadIEEE()


