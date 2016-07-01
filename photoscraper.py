__author__ = 'abraham'

from lxml import html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import requests
from utils import *
from db import getCursor
from actorphotoscrap import actorphoto
from insert_actor_into_cast import *
from conf import photos_url_per_movie_series

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    "Accept-Language": "en-US,en;q=0.5"}

#photo scraper movie or series
def photoscrap(imdb,globalmovieid,moviephotosurl):
    print "photo scrap..."

    #only movies and series not actors,actors photos are pulling from actorscraper.py/actorphotoscrap.py
    if moviephotosurl:
        #get photo urls
        page = requests.get(moviephotosurl, headers=headers);
        tree = html.fromstring(page.content);
        tree.make_links_absolute(moviephotosurl)

        photosurl = tree.xpath('//div[@id="media_index_thumbnail_grid"]//a/img/@src')

        if photosurl:

            db = getCursor()
            cur = db.cursor()

            for i in xrange(len(photosurl)):
                img = photosurl[i]

                sql = "insert into Images(imageurl) values(%s)"

                try:
                    cur.execute(sql,[photosurl[i]])

                    sql = "select imageid from Images where imageurl = %s"

                    cur.execute(sql,[img])

                    result = cur.fetchall()

                    for row in result:
                        imageid = row[0]
                        sql = "insert into MovieImages(movieid,imageid) values(%s,%s)"
                        cur.execute(sql,[globalmovieid,imageid])
                        db.commit()
                except MySQLdb.Error, e:
                    print e
                    db.rollback()

                if i == photos_url_per_movie_series:
                    print 'max photos '+`i`
                    break

            db.commit()
            db.close()




