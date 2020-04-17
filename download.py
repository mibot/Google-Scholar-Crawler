# coding=utf-8
#coding:gb2312
import re

import pymysql
import requests
import os
from requests.auth import HTTPProxyAuth
import urllib
from bs4 import BeautifulSoup
import hashlib
import random
from random import randint
import time
from retrying import retry
from textblob import TextBlob

from user_agent_list import get_random_ua
from proxy_list_gen import get_random_proxy
import logging

from base import db, cur

dataPath = os.path.abspath(os.path.relpath('pdf'))

# log config
logging.basicConfig()
logger = logging.getLogger('Sci-Hub')
logger.setLevel(logging.DEBUG)

scihub_choices = ['https://sci-hub.tw/',
                  'http://sci-hub.se/',
                  ]

from mstranslator import Translator

key_choices = ["KEY",
               "KEY", ]

from api_google import translate_text, detect_language


class DownloadPDF():
    def __init__(self):
        pass

    @retry(wait_random_min=100, wait_random_max=1000, stop_max_attempt_number=10)
    # @retry(wait_random_min=1000, wait_random_max=2000, stop_max_attempt_number=2)
    def download(self, identifier, destination='', path=None, sh=False):
        res = False
        # print "sh: %s" %(sh)
        data = self.fetch(identifier, sh)

        if not 'err' in data:
            self._save(data['pdf'], os.path.join(destination, path if path else data['name']))
            res = True
        elif 'err' in data and sh == False:
            time.sleep(randint(10, 20))
            self.download(identifier, destination, path, sh=True)

        return res

    def fetch(self, identifier, sh):
        if sh == False:
            url = self._get_direct_url(identifier)
        else:
            url = self._search_direct_url(identifier)

        try:
            ua = get_random_ua()
            my_header = {'User-Agent': str(ua)}
            res = requests.get(url, headers=my_header)
            content_type = res.headers.get('content-type')

            if 'application/pdf' in str(content_type):
                return {
                    'pdf': res.content,
                    'url': url
                    # 'name': self._generate_name(res)
                }
            else:
                return {
                    'err': 'Failed to fetch pdf with identifier %s (resolved url %s) due to captcha'
                           % (identifier, url)
                }


        except requests.exceptions.RequestException as e:

            return {
                'err': 'Failed to fetch pdf with identifier %s (resolved url %s) due to request exception.'
                       % (identifier, url)
            }

    def _get_direct_url(self, identifier):
        id_type = self._classify(identifier)

        return identifier if id_type == 'url-direct' \
            else self._search_direct_url(identifier)

    def _search_direct_url(self, identifier):
        SCIHUB_BASE_URL = random.choice(scihub_choices)
        # print SCIHUB_BASE_URL
        try:
            ua = get_random_ua()
            my_header = {'User-Agent': str(ua)}
            res = requests.get(SCIHUB_BASE_URL + identifier, headers=my_header)

            # s = self._get_soup(res.content.decode('latin-1').decode('gbk').encode('utf-8'))
            # s = self._get_soup(res.content)
            s = self._get_soup(res.content.decode('latin-1').encode('utf-8'))
            iframe = s.find('iframe')
            if iframe:
                return iframe.get('src') if not iframe.get('src').startswith('//') \
                    else 'http:' + iframe.get('src')

        #         except TypeError:
        #             return {
        #                 'err': 'Failed to fetch sci-hub page with identifier during string formatting.'
        #                    % (identifier)
        #             }

        except requests.exceptions.RequestException as e:

            return {
                'err': 'Failed to fetch sci-hub page with identifier %s due to request exception.'
                       % (identifier)
            }

    def _classify(self, identifier):

        if (identifier.startswith('http') or identifier.startswith('https')):
            if 'pdf' in identifier:
                return 'url-direct'
            else:
                return 'url-non-direct'
        elif identifier.isdigit():
            return 'pmid'
        else:
            return 'doi'

    def _save(self, data, path):
        with open(path, 'wb') as f:
            f.write(data)
        # print "downloaded"

    def _get_soup(self, html):
        return BeautifulSoup(html, 'html.parser')

    def _generate_name(self, res):
        name = res.url.split('/')[-1]
        pdf_hash = hashlib.md5(res.content).hexdigest()
        return '%s-%s' % (pdf_hash, name[-20:])


# def downloadPDF():
#     ids = _getIdPub(1)
#     for id in ids:
#         print(id[0])
#         i = id[0]
#
#         p = False
#         downloaded = "False"
#         count = 0
#         if _checkPDFDownloaded(i):
#             # if _checkPDFinURL(i):  # or not _checkPDFinURL(i):
#             try:
#                 title = _getTitle(i)
#                 # print title
#                 res_title = _checkTitle(title)
#                 if res_title and res_title == "en":  # or not res_title:
#
#                     url = _getUrl(i, "direct_link")
#
#                     while downloaded == "False" and count < 2:
#                         count += 1
#                         if url:
#                             s = DownloadPDF()
#                             p = s.download(url,
#                                            destination='/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/pdf/tocheck/',
#                                            path=str(i) + '.pdf')
#                         if p == True:
#                             downloaded = "True"
#                         else:
#                             url = _getUrl(i, "main_link")
#
#             except UnicodeDecodeError:
#                 pass
#
#             if downloaded == "True":
#                 # sql = "update resolved_papers2019_unique set downloaded = 1 where id = %s" % (i)
#                 sql = "update resolved_papers set downloaded = 1 where id = %s" % (i)
#
#                 try:
#                     cur.execute(sql)
#                     db.commit()
#                 except:
#                     db.rollback()
#             print("Id: %s. Downloaded: %s" % (i, downloaded))
#             # i += 1


def downloadPDF(ids):
    # keep this connection in order to use multiprocessing
    db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                         user="root",  # your username
                         passwd="iwJx0EAM",  # your password
                         db="clpd")  # name of the data base

    cur = db.cursor()

    try:
        i, res_title, main_link, direct_link = ids


        p = False
        downloaded = "False"
        count = 0



        # to get the title language
        # sql = 'select title_language from resolved_papers_title where id = %s;' % (i)
        # cur.execute(sql)
        # res_title = cur.fetchall()[0][0]


        if res_title and res_title == "en":  # or not res_title:

            print(i)
            print(main_link)
            print(direct_link)

            # url = _getUrl(i, "direct_link")
            url = direct_link

            while downloaded == "False" and count < 2:
                count += 1
                if url:
                    s = DownloadPDF()
                    p = s.download(url,
                                   destination='/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/pdf/tocheck/',
                                   path=str(i) + '.pdf')
                if p == True:
                    downloaded = "True"
                else:
                    # url = _getUrl(i, "main_link")
                    url = main_link

            if downloaded == "True":
                # sql = "update resolved_papers2019_unique set downloaded = 1 where id = %s" % (i)
                sql = "update resolved_papers set downloaded = 1 where id = %s" % (i)

                try:
                    cur.execute(sql)
                    db.commit()
                    print("Id: %s. Downloaded: %s. Saved!" % (i, downloaded))
                except:
                    db.rollback()
            else: print("Id: %s. Downloaded: %s." % (i, downloaded))

    except UnicodeDecodeError:
        pass


    cur.close()
    # print("Id: %s. Downloaded: %s" % (i, downloaded))
    # i += 1


def downloadPDFIEEE(ids):
    # keep this connection in order to use multiprocessing
    db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                         user="root",  # your username
                         passwd="iwJx0EAM",  # your password
                         db="clpd")  # name of the data base

    cur = db.cursor()

    try:
        i, res_title, main_link, direct_link = ids


        p = False
        downloaded = "False"
        count = 0



        # to get the title language
        # sql = 'select title_language from resolved_papers_title where id = %s;' % (i)
        # cur.execute(sql)
        # res_title = cur.fetchall()[0][0]


        if res_title and res_title == "en":  # or not res_title:

            print(i)
            print(main_link)
            print(direct_link)

            # url = _getUrl(i, "direct_link")
            # toParse = direct_link
            # paper_id = (re.findall('\d+', toParse))[0]
            url = direct_link

            while downloaded == "False" and count < 2:

                count += 1
                if count == 2:
                    file = requests.get(url)
                    open('/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/pdf/tocheck/%s.pdf', 'wb').write(file.content) % (i)
                    p = True
                else:
                    if url:
                        s = DownloadPDF()
                        p = s.download(url,
                                       destination='/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/pdf/tocheck/',
                                       path=str(i) + '.pdf')
                if p == True:
                    downloaded = "True"
                else:
                    # url = _getUrl(i, "main_link")
                    toParse = main_link
                    paper_id = (re.findall('\d+', toParse))[0]
                    # url = 'http://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber=%s' % (paper_id)
                    url = 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=%s' % (paper_id)

            if downloaded == "True":
                # sql = "update resolved_papers2019_unique set downloaded = 1 where id = %s" % (i)
                sql = "update resolved_papers set downloaded = 1 where id = %s" % (i)

                try:
                    cur.execute(sql)
                    db.commit()
                    print("Id: %s. Downloaded: %s. Saved!" % (i, downloaded))
                except:
                    db.rollback()
            else: print("Id: %s. Downloaded: %s." % (i, downloaded))

    except UnicodeDecodeError:
        pass


    cur.close()
    # print("Id: %s. Downloaded: %s" % (i, downloaded))
    # i += 1


def _getIdPub(max):
    # sql = 'select id from resolved_papers2019_unique;'
    # sql = 'select id from resolved_papers where id >= %s;' % (max)
    sql = 'select id from resolved_papers where id >= %s and downloaded = 0;' % (max)
    cur.execute(sql)

    return cur.fetchall()


def _checkPDFDownloaded(id):
    # sql = 'select id from resolved_papers2019_unique where downloaded = 0 and id = %s;' % (id)
    sql = 'select id from resolved_papers where downloaded = 0 and id = %s;' % (id)
    cur.execute(sql)
    try:
        return cur.fetchall()[0][0]
    except IndexError:
        return ""


def _checkPDFinURL(id):
    # sql = 'select id from resolved_papers2019_unique where (lower(direct_link) like "%%pdf%%" or lower(main_link) like "%%pdf%%") and downloaded = 0 and id = %s;' % (
    #     id)
    sql = 'select id from resolved_papers where (lower(direct_link) like "%%pdf%%" or lower(main_link) like "%%pdf%%") and downloaded = 0 and id = %s;' % (
        id)
    cur.execute(sql)
    try:
        return cur.fetchall()[0][0]
    except IndexError:
        return ""


def _getTitle(id):
    # sql = 'select title from resolved_papers2019_unique where id = %s;' % (id)
    sql = 'select title from resolved_papers where id = %s;' % (id)
    cur.execute(sql)
    return cur.fetchall()[0][0]

# def _getTitleLang(id):
#     sql = 'select title_language from resolved_papers_title where id = %s;' % (id)
#     cur.execute(sql)
#     return cur.fetchall()[0][0]

def _checkTitle(title):
    res = ""
    try:
        translator = Translator(random.choice(key_choices))
        res = translator.detect_lang([title])
        #
        # # translator = Translator(random.choice(key_choices))
        # # res = translate_text(title,'es',)
        # # res = translator.detect_langs([title])
        # res = detect_language(title)
        print(res)
        # res = TextBlob(title).detect_language()

    except (IndexError, ValueError):
        pass
    return res


def _getUrl(id, linkName):
    # sql = 'select %s from resolved_papers2019_unique where id = %s;' % (linkName, id)
    sql = 'select %s from resolved_papers where id = %s;' % (linkName, id)
    cur.execute(sql)
    return cur.fetchall()[0][0]


def _getSource(url):
    res = ""
    try:
        res = url.split("/")[2]
    except (IndexError, ValueError):
        pass
    return res

# s = DownloadPDF()
# result = s.download(identifier='https://www.researchgate.net/profile/Lola_Ferre/publication/327938925_The_multi-cultural_origins_of_the_Salernitan_medical_school_A_historiographical_debate/links/5bb305ada6fdccd3cb814e30/The-multi-cultural-origins-of-the-Salernitan-medical-school-A-historiographical-debate.pdf', path='pdf/tocheck/paper.pdf')
