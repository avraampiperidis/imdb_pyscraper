# -*- coding: utf-8 -*-
__author__ = 'abraham'

from lxml import html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
from utils import is_date_older_2months
from utils import month_to_int
from utils import remove_all_special_chars
from db import getCursor

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    "Accept-Language": "en-US,en;q=0.5"}


def moviedb(i,globalmovieid,title,datelist,genre,content_rating,ratings,rating_value,plot,link,poster):
    MySQLdb.escape_string("'")

    plot = remove_all_special_chars(plot)

    #db utils
    db = getCursor()
    cur = db.cursor()

    #check if movie already in database
    cur.execute("select count(1) from Movie where imdbid = %s or movieid = %s ", [i,globalmovieid])
    if cur.fetchone()[0]:
        print 'Movie exits'
        #if record exists do nothing ,its movie,movie never changes
    else:
        print 'Movie not exists'
        print 'insert..'
        if len(datelist) < 4:
            datelist = ["1","January","1971"]
        #if movie is less than 2 months old
        #insert into movie
        if(is_date_older_2months(datelist) == False):
            print globalmovieid,i,title
            print ' '.join(datelist)
            if not rating_value:
                rating_value = 5
            if not content_rating:
                content_rating = "R"
            sql = "insert into Movie(movieid,imdbid,title,plot,altplot,date,year,month,day,genre,ratings,ratingvalue,contentrating,poster) " \
                  "values('%s','%s','%s','%s','%s','%s','%d','%s','%s','%s','%s','%s','%s','%s') " % \
                  (globalmovieid,i,title.strip(),plot.strip()," ",' '.join(datelist),int(datelist[2]),month_to_int(datelist[1]),0,genre,int(ratings),float(rating_value),content_rating,poster)
            try:
                cur.execute(sql)
                db.commit()
            except MySQLdb.Error, e:
                db.rollback()
                print e

            db.close()
        else:
            print 'do nothing'
            #coming soon will be maintained by other program












