import os

import nltk
import pandas as pd
import re

from nltk import word_tokenize
from nltk.corpus import stopwords

from base import db, cur


def countOcurrencies():
    sql = 'select id, type from resolved_papers where downloaded = 1 and npages >= 5 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and type is not null;'
    papers = pd.read_sql(sql, con=db)

    for index, row in papers.iterrows():
        res = _countOccurencies(row[0], row[1])
        print("Id: %s. Keyword ocurrences processed: %s. Head: %s. Tail: %s" % (row[0], res[0], res[1], res[2]))


def _processText(line):
    line = line.lower()

    line = re.sub("cross\slanguage", "cross-language", line)

    line = re.sub("cross\slingual", "cross-lingual", line)

    line = re.sub("cross\slinguistic", "cross-linguistic", line)

    line = re.sub("multi\slanguage", "multi-language", line)

    line = re.sub("multi\slingual", "multi-lingual", line)

    line = re.sub("multi\slinguistic", "multi-linguistic", line)

    line = re.sub("machine\stranslation", "machine-translation", line)
    #             if line.startswith("cop"):
    #                 line = "copy"
    pattern = re.compile("copy.*")
    line = pattern.sub("copy", line)

    pattern = re.compile("duplicat.*")
    # pattern = re.compile(r"duplicat[\w]", re.DOTALL)
    line = pattern.sub("duplicate", line)

    pattern = re.compile("detect.*")
    line = pattern.sub("detection", line)

    pattern = re.compile("discover.*")
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


def _countOccurencies(id, type):
    keywords = ["Cross-language",
                "Crosslanguage",
                "Cross-lingual",
                "Crosslingual",
                "Cross-linguistic",
                "Crosslinguistic",
                "Multi-language",
                "Multilanguage",
                "Multi-lingual",
                "Multilingual",
                "Multi-linguistic",
                "Multilinguistic",
                "Machine-translation",
                "Copy",
                "Duplicate",
                "Plagiarism",
                "Detection",
                "Discovery"]
    nkeywords = len(keywords)
    text = ""
    # with open(os.path.join('data/txt', str(id) + '_head.txt')) as infile:
    with open(os.path.join('/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/txt', str(id) + '_head.txt')) as infile:
        for line in infile:
            line = _processText(line)
            text += line

    words = _processNL(text)
    fdist = nltk.FreqDist(words)

    i = 0
    head = False
    while i < nkeywords:

        if fdist[str(keywords[i]).lower()] > 0:
            sql = "insert into resolved_papers_occurrenciesv4 values (%s, '%s', '%s', '%s', %s);" % (
                id, type, "head", str(keywords[i]).lower(), fdist[str(keywords[i]).lower()])
            # print (sql)
            head = True
            try:
                cur.execute(sql)
                db.commit()
            except:
                db.rollback()
        i += 1
    #### tail
    text = ""
    # with open(os.path.join('data/txt', str(id) + '_tail_noreferences.txt')) as infile:
    with open(os.path.join('/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/txt', str(id) + '_tail_noreferences.txt')) as infile:
        for line in infile:
            line = _processText(line)
            text += line
    words = _processNL(text)
    fdist = nltk.FreqDist(words)

    i = 0
    tail = False
    while i < nkeywords:

        if fdist[str(keywords[i]).lower()] > 0:
            sql = "insert into resolved_papers_occurrenciesv4 values (%s, '%s', '%s', '%s', %s);" % (
                id, type, "tail", str(keywords[i]).lower(), fdist[str(keywords[i]).lower()])
            # print (sql)
            tail = True
            try:
                cur.execute(sql)
                db.commit()
            except:
                db.rollback()
        i += 1

    return ('Done',head, tail)
