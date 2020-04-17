import pymysql

from base import db, cur

from os import listdir
from os.path import isfile, join


files = [f for f in listdir('data/manual') if isfile(join('data/manual', f))]

for file in files:
    name = file.split('.')[0]
    sql = "update resolved_papers set downloaded = 1 where id = %s" % (name)

    try:
        cur.execute(sql)
        db.commit()
        print("Id: %s. Updated!" % (name))
    except:
        db.rollback()
