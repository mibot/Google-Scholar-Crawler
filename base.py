import pymysql


db = pymysql.connect(host="dbinstancephd.cikbkbxucwjr.us-east-2.rds.amazonaws.com",  # your host, usually localhost
                         user="root",  # your username
                         passwd="iwJx0EAM",  # your password
                         db="clpd")  # name of the data base

cur = db.cursor()