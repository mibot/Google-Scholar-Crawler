#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing.pool import ThreadPool
import pymysql
import os
import re
import pandas as pd
from urllib.request import urlretrieve
import urllib.request
import requests
from my_fake_useragent import UserAgent

from base import db, cur

dataPath = os.path.abspath(os.path.relpath('../data'))

# def downloadPDF(i, main_link, direct_link):
def downloadPDF(ids):
    # keep this connection in order to use multiprocessing
    db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                         user="root",  # your username
                         passwd="iwJx0EAM",  # your password
                         db="clpd")  # name of the data base

    cur = db.cursor()

    try:
        i, main_link, direct_link = ids


        p = False
        downloaded = "False"
        count = 0

        print(i)
        print(main_link)
        print(direct_link)

        # url = _getUrl(i, "direct_link")
        url = direct_link

        while downloaded == "False" and count < 2:
            count += 1
            if url:
                # url = 'https://s3.amazonaws.com/academia.edu/download/30761819/book.pdf?response-content-disposition=inline%3B%20filename%3DUsing_monolingual_clickthrough_data_to_b.pdf&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWOWYYGZ2Y53UL3A%2F20190908%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20190908T222002Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=eee90437409f359612d0a47e04739fb0733d3eb347c3d6e4145596986966b26a#page=32'
                # https://s3.amazonaws.com/academia.edu.documents/30761819/book.pdf?response-content-disposition=inline%3B%20filename%3DUsing_monolingual_clickthrough_data_to_b.pdf&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWOWYYGZ2Y53UL3A%2F20190908%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20190908T222002Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=eee90437409f359612d0a47e04739fb0733d3eb347c3d6e4145596986966b26a#page=32
                url = "http://www.academia.edu/download/30761819/book.pdf#page=32"
                # http://www.academia.edu/download/30761819/book.pdf#page=32
                # url = 'http://google.com'
                i = 149
                destination = '/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/pdf/tocheck/'
                path = destination + str(i) + '.pdf'

                try:

                    ua = UserAgent()
                    headers = {'User-Agent': str(ua.random)}

                    r = requests.head('http://www.academia.edu/download/30761819/book.pdf#page=32', allow_redirects=True)
                    print(r.url)


                    s = requests.session()

                    res = s.get(url, headers=headers, allow_redirects=False)
                    print(res.url)
                    # print(finalurl)

                    p = urlretrieve(url, path)

                    if p[1].get_content_type() == 'application/pdf':
                        downloaded = "True"
                except:
                    pass
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

def main():
    sql = """select id, main_link, direct_link from resolved_papers where downloaded = 0 and id in (136,	149,	247,	292,	345,	414,	424,	588,	591,	716,	734,	735,	754,	816,	861,	1084,	1100,	1122,	1126,	1146,	1176,	1283,	1307,	1367,	1381,	1696,	1728,	2276,	2325,	2448,	2576,	2577,	2578,	2661,	2671,	2782,	2786,	2790,	2794,	2798,	2920,	3127,	3141,	3146,	3172,	3176,	3177,	3182,	3185,	3199,	3236,	3275,	3302,	3365,	3422,	3452,	3461,	3526,	3532,	3538,	3541,	3597,	3939,	3943,	3948,	3953,	3955,	3958,	3965,	3967,	3971,	3972,	3980,	4109,	4127,	4287,	4362,	4461,	4465,	4468,	4470,	4481,	4572,	4607,	4796,	4804,	4839,	5040,	5411,	5462,	5536,	5594,	5833,	5889,	6085,	6279,	6283,	6305,	6306,	6393,	6396,	6498,	6532,	6553,	6566,	6573,	6648,	6672,	6676,	6682,	6684,	6690,	6692,	6704,	6769,	6778,	6785,	6830,	6834,	6849,	6855,	6873,	6878,	6889,	6890,	7006,	7314,	7441,	7443,	7462,	7504,	7548,	7788,	7789,	7795,	7797,	7918,	7930,	7935,	7941,	7944,	8008,	8110,	8111,	8112,	8117,	8136,	8140,	8143,	8144,	8148,	8225,	8497,	8506,	8533,	8543,	8718,	8739,	8742,	8744,	8752,	8753,	8755,	8756,	8757,	8759,	8761,	8769,	8773,	8774,	9562,	10168,	10400,	10606,	10771,	10772,	10819,	11113,	11361,	11362,	11377,	11461,	11462,	11611,	11617,	11638,	11750,	11821,	11917,	11921,	11922,	11923,	11926,	11928,	12044,	12092,	12094,	12096,	12102,	12104,	12111,	12112,	12123,	12147,	12235,	12339,	12511,	12665,	12705,	12717,	12905,	12907,	13061,	13062,	13329,	13332,	13585,	13697,	13833,	13834,	13836,	14341,	14343,	14689,	14777,	14991,	14992,	14993,	14995,	15136,	15138,	15139,	15140,	15142,	15152,	15387,	15388,	15483,	15805,	15932,	16124,	16175,	16277,	16392,	16393,	16402,	16444,	16447,	16448,	16468,	16596,	16600,	16647,	16648,	16765,	17013,	17034,	17141,	17142,	17143,	17144,	17263,	17335,	17395,	17400,	17410,	17547,	17584,	17599,	17719,	17750,	17751,	17756,	17811,	17812,	17964,	17998,	18229,	18257,	18264,	18323,	18515,	18600,	18623,	18675,	18830,	18891,	18893,	18930,	18970,	18973,	18982,	18983,	18991,	19006,	19059,	19062,	19066,	19067,	19103,	19180,	19273,	19280,	19606,	19607,	19612,	19801,	19807,	19808,	19812,	19813,	19820,	19985,	20054,	20058,	20059,	20084,	20168,	20349,	20350,	20353,	20355,	20356,	20361,	20362,	20363,	20370,	20373,	20377,	20476,	20520,	20692,	20693,	20694,	20699,	20701,	20703,	20707,	20709,	20728,	20867,	20868,	20869,	20899,	21121,	21139,	21146,	21510,	21616,	21623,	21624,	21667,	21751,	21875,	21924,	21957,	21985,	21993,	21997,	22371,	22374,	22695,	22884,	22977,	23030,	23230,	23236,	23238,	23340,	23552,	23761,	24016,	24140,	24145,	24168,	24187,	24193,	24206,	24209,	24214,	24239,	24243,	24250,	24252,	24256,	24297,	24299,	24302,	24305,	24308,	24326,	24330,	24368,	24390,	24406,	24408,	24413,	24439,	24440,	24473,	24476,	24477,	24479,	24480,	24485,	24486,	24487,	24522,	24524,	24525,	24527,	24529,	24530,	24531,	24532,	24536,	24537,	24540,	24542,	24543,	24550,	24586,	24621,	24624,	24625,	24627,	24630,	24631,	24634,	24635,	24637,	24638,	24639,	24641,	24645,	24654,	24713,	24716,	24717,	24721,	24723,	24775,	24795,	24833,	24845,	24846,	24926,	25177,	25178,	25195,	25251,	25267,	25340,	25455,	25456,	25460,	25975,	25978,	26003,	26186,	26202,	26284,	26316,	26320,	26489,	26497,	27307,	27342,	27608,	27635,	27641,	28263,	28422,	28437,	28739,	28740,	28743,	28990,	28993,	29124,	29130,	29201,	29226,	29278,	29282,	29302,	29314,	29316,	29436,	29470,	29482,	29505,	29535,	29537,	29556,	29561,	29618,	29637,	29709,	29710,	29741,	29752,	29753,	30074,	30351,	30358,	30376,	30424,	30426,	30615,	30616,	30619,	31336,	31357,	31358,	31360,	31502,	31526,	31527,	31528,	31882,	31883,	31890,	31929,	31966,	32153,	32520,	32583,	32618,	32683,	33058,	33148,	33153,	33255,	33522,	33527,	33582,	33599,	33883,	33890,	33926,	33931,	34000,	34001,	34081,	34296,	34346,	34399,	34461,	34463,	34464,	34469,	34527,	34846,	34941,	35015,	35020,	35134,	35294,	35311,	35323,	35329,	35330,	35343,	35351,	35356,	35440,	35474,	35529,	35637,	35733,	35835,	35881,	35889,	35896,	35907,	35909,	35917,	35926,	35929,	35950,	35979,	36000,	36018,	36093,	36111,	36154,	36173,	36223,	36225,	36229,	36240,	36242,	36244,	36247,	36269,	36370,	36433,	36469,	36480,	36504,	36520,	36614,	36756,	36843,	36854,	36870,	36875,	36876,	36952,	36996,	37092,	37266,	37352,	37495,	37519,	37572,	37608,	37735,	37750,	37758,	37808,	37841,	37842,	37852,	37863,	38092,	38282,	38300,	38302,	38303,	38309,	38314,	38382,	38399,	38411,	38420,	38514,	38515,	38547,	38564,	38569,	38574,	38619);"""
    papers = pd.read_sql(sql, con=db)
    for index, row in papers.iterrows():
        # print(row['id'])
        ids = (str(row['id']), row['main_link'], row['direct_link'])
        # downloadPDF(row['id'], row['main_link'], row['direct_link'])
        downloadPDF(ids)
    # ids = list(zip(*[papers[c].values.tolist() for c in papers]))
    #
    # pool = ThreadPool()
    #
    # print(pool.imap_unordered(downloadPDF, ids))
    # pool.close()
    #
    # pool.join()

if __name__ == '__main__':
    main()