from multiprocessing.pool import ThreadPool

import pandas as pd
import pymysql

from base import db, cur


def filterTitles():
    sql = "select p.id, p.title from resolved_papers as p inner join resolved_papers_title as pt on pt.id = p.id and pt.title_language = 'en';"
    print(sql)
    papers = pd.read_sql(sql, con=db)
    ids = list(zip(*[papers[c].values.tolist() for c in papers]))

    pool = ThreadPool()

    print(pool.imap_unordered(_filterTitle, ids))
    pool.close()

    pool.join()


def _filterTitle(papers):
    # keep this connection in order to use multiprocessing
    db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                         user="root",  # your username
                         passwd="iwJx0EAM",  # your password
                         db="clpd")  # name of the data base

    cur = db.cursor()

    try:

        id, title = papers

        threshold = 1

        # title = 'A New Approach for Cross-Language Plagiarism Analysis.'.lower()
        title = title.lower()


        k_dflanguage = 0
        k_copy = 0
        k_detection = 0

        diff_language = ["Cross-language",
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
                         "Machine-translation", ]

        copy = ["Copy",
                "Duplicate",
                "Plagiarism", ]

        detection = ["Detection",
                     "Discovery", ]

        for row in diff_language:
            if row.lower() in title:
                k_dflanguage += 1

        for row in copy:
            if row.lower() in title:
                k_copy += 1

        for row in detection:
            if row.lower() in title:
                k_detection += 1

        print("diff_language: %s." % (k_dflanguage))
        print("copy: %s." % (k_copy))
        print("detection: %s." % (k_detection))

        if (k_dflanguage >= threshold or k_detection >= threshold or k_detection >= threshold):
            # papers_selected.append(id, title)

            sql = "insert into resolved_papers_selected_title values (%s)" % (id)
            print(sql)
            # try:
            cur.execute(sql)
            db.commit()
            # except:
            db.rollback()

            return True
        else:
            return False
    except:
        db.rollback()
        print('no saved')
    cur.close()
