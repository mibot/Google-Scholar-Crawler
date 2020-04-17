import os
from multiprocessing.pool import ThreadPool

import nltk
import pandas as pd
import re

import pymysql
from nltk import word_tokenize
from nltk.corpus import stopwords

from base import db, cur


def countTitleOcurrencies():
    sql = "select p.id, p.title from resolved_papers as p inner join resolved_papers_title as pt on pt.id = p.id and pt.title_language = 'en';"
    papers = pd.read_sql(sql, con=db)

    print(sql)
    papers = pd.read_sql(sql, con=db)
    ids = list(zip(*[papers[c].values.tolist() for c in papers]))

    pool = ThreadPool()

    print(pool.imap_unordered(_countOccurencies, ids))
    pool.close()

    pool.join()

    # for index, row in papers.iterrows():
    #     res = _countOccurencies(row[0], row[1])
    #     print("Id: %s. Keywords processed: %s. Head: %s. Tail: %s" % (row[0], res[0], res[1], res[2]))


def _processText(line):
    line = line.lower()

    line = re.sub("‐", "-", line)

    line = re.sub("cross\slanguage", "cross-language", line)

    line = re.sub("cross\slingual", "cross-lingual", line)

    line = re.sub("cross\slinguistic", "cross-linguistic", line)

    line = re.sub("multi\slanguage", "multi-language", line)

    line = re.sub("multi\slingual", "multi-lingual", line)

    line = re.sub("multi\slinguistic", "multi-linguistic", line)

    line = re.sub("machine\stranslation", "machine-translation", line)
    #             if line.startswith("cop"):
    #                 line = "copy"
    pattern = re.compile("copy\.")
    line = pattern.sub("copy", line)

    pattern = re.compile("duplicat\.")
    # pattern = re.compile(r"duplicat[\w]", re.DOTALL)
    line = pattern.sub("duplicate", line)

    # pattern = re.compile("detect.*")
    pattern = re.compile("detect\.")
    line = pattern.sub("detection", line)

    pattern = re.compile("discover\.")
    line = pattern.sub("discovery", line)

    #             if line.startswith("detect"):
    #                 line = "detection"
    #             if line.startswith("discover"):
    #                 line = "discovery"
    line = re.sub("-\n", "", line)
    line = re.sub("\n", " ", line)

    return line


def _processNL(text):
    tokens = word_tokenize(text)
    punctuations = ['(', ')', ';', ':', '[', ']', ',']
    stop_words = stopwords.words('english')
    words = [word for word in tokens if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in stop_words]

    return words


def _countOccurencies(papers):
    # keep this connection in order to use multiprocessing
    db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                         user="root",  # your username
                         passwd="iwJx0EAM",  # your password
                         db="clpd")  # name of the data base

    cur = db.cursor()

    try:
        id, title = papers

        # title = 'CLEU‐A Cross‐Language English‐Urdu Corpus and Benchmark for Text Reuse Experiments'

        keywords = ["Cross-language".lower().strip(),
                    "Crosslanguage".lower().strip(),
                    "Cross-lingual".lower().strip(),
                    "Crosslingual".lower().strip(),
                    "Cross-linguistic".lower().strip(),
                    "Crosslinguistic".lower().strip(),
                    "Multi-language".lower().strip(),
                    "Multilanguage".lower().strip(),
                    "Multi-lingual".lower().strip(),
                    "Multilingual".lower().strip(),
                    "Multi-linguistic".lower().strip(),
                    "Multilinguistic".lower().strip(),
                    "Machine-translation".lower().strip(),
                    "Copy".lower().strip(),
                    "Duplicate".lower().strip(),
                    "Plagiarism".lower().strip(),
                    "Detection".lower().strip(),
                    "Discovery".lower().strip()]
        nkeywords = len(keywords)
        text = _processText(title)
        words = _processNL(text)
        fdist = nltk.FreqDist(words)


        i = 0
        while i < nkeywords:

            if fdist[str(keywords[i]).lower()] > 0:
                sql = "insert into resolved_papers_title_occurrencies values (%s, '%s', %s);" % (
                    id, str(keywords[i]).lower(), fdist[str(keywords[i]).lower()])
                # print (sql)
                try:
                    cur.execute(sql)
                    db.commit()
                    print('saved')
                except:
                    db.rollback()
            i += 1
    except:
        db.rollback()
        print('no saved')
    cur.close()