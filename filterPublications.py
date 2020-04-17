from multiprocessing.pool import ThreadPool

import pandas as pd
import pymysql

from base import db, cur


def filterPub():
    papers_toread = []

    # sql = 'select id, type from resolved_papers where downloaded = 1 and npages >= 5 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and type is not null and toread is null;'
    sql = 'select id, type from resolved_papers where downloaded = 1 and npages >= 5 and pdf2text = 1 and english = 1 and head = 1 and tail = 1 and type is not null;'
    print(sql)
    papers = pd.read_sql(sql, con=db)
    ids = list(zip(*[papers[c].values.tolist() for c in papers]))

    pool = ThreadPool()

    papers_toread.append(pool.imap_unordered(_filterPub, ids))
    pool.close()

    pool.join()

    papers_toread_cleaned = filter(None, papers_toread)
    papers_toread_df = pd.DataFrame(papers_toread_cleaned)
    papers_toread_df.to_csv("papers_toread_threshold-5.1.csv", index=False, header=None, encoding='utf-8', sep='\n')

    # for index, row in papers.iterrows():
    #     res = _filterPub(row[0], 1)
    #     print("Id: %s. Filtered: %s. " % (row[0], res))


def _filterPub(papers):
    # keep this connection in order to use multiprocessing
    db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                         user="root",  # your username
                         passwd="iwJx0EAM",  # your password
                         db="clpd")  # name of the data base

    cur = db.cursor()

    try:

        id, type = papers

        threshold = 5


        k_dflanguage_head = 0
        k_dflanguage_tail = 0
        k_copy_head = 0
        k_copy_tail = 0
        k_detection_head = 0
        k_detection_tail = 0

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
                         "Machine-translation",]

        copy = ["Copy",
                "Duplicate",
                "Plagiarism",]

        detection = ["Detection",
                     "Discovery",]
        # id = 30061
        sql = "select section, sstring, freq from resolved_papers_occurrenciesv4 where id = %s and type = 'paper'" % (id)
        # res = pd.read_sql(sql, con=db)
        # print sql
        # try:
        cur.execute(sql)
        res = cur.fetchall()

        # except:
        #     res = ""
        for row in res:
            i = 0
            while i < len(diff_language):
                if str(diff_language[i]).lower() == row[1]:
                    if row[0] == "head":
                        k_dflanguage_head += row[2]
                    if row[0] == "tail":
                        k_dflanguage_tail += row[2]
                i += 1
            i = 0
            while i < len(copy):
                if str(copy[i]).lower() == row[1]:
                    if row[0] == "head":
                        k_copy_head += row[2]
                    if row[0] == "tail":
                        k_copy_tail += row[2]
                i += 1
            i = 0
            while i < len(detection):
                if str(detection[i]).lower() == row[1]:
                    if row[0] == "head":
                        k_detection_head += row[2]
                    if row[0] == "tail":
                        k_detection_tail += row[2]
                i += 1

        # print("diff_language_head: %s. diff_language_tail: %s" % (k_dflanguage_head, k_dflanguage_tail))
        # print("copy_head: %s. copy_tail: %s" % (k_copy_head, k_copy_tail))
        # print("detection_head: %s. detection_tail: %s" % (k_detection_head, k_detection_tail))

        # if (k_dflanguage_head >= threshold and k_dflanguage_tail >= threshold) and \
        #         (k_copy_head >= threshold and k_copy_tail >= threshold) and \
        #         (k_detection_head >= threshold and k_detection_tail >= threshold):
        if (k_dflanguage_head >= threshold and k_dflanguage_tail >= threshold) and \
                (k_copy_head >= threshold and k_copy_tail >= threshold):
            # sql = 'select title from resolved_query where id = %s;' % (id)
            # try:
            #     cur.execute(sql)
            #     # res = cur.fetchall()[0][0]
            #     res = db.fetchall()
            # except:
            #     res = ""
            # if res:
            # sql = "update resolved_papers set toread = 1 where id = %s" % (id)
            # print sql
            # try:
            # cur.execute(sql)
            # db.commit()
            # except:
            # db.rollback()
            # papers_toread.append(id)
            print (id)

            return id
        # else:
        #     return False
    except:
        pass
    #     db.rollback()
    #     print('no saved')
    # cur.close()
