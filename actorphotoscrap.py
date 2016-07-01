# -*- coding: utf-8 -*-
__author__ = 'abraham'

from lxml import html
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')
from utils import *
from db import getCursor
from insert_actor_into_cast import *
import requests
from conf import photos_url_per_actor

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    "Accept-Language": "en-US,en;q=0.5"}


def actorphoto(personid,link):
    print "photo scrap..."
    print link

    page = requests.get(link, headers=headers);
    tree = html.fromstring(page.content);
    tree.make_links_absolute(link)

    imglinks = tree.xpath('//div[@id="media_index_thumbnail_grid"]//a/img/@src')

    if imglinks:
        db = getCursor()
        cur = db.cursor()

        for i in xrange(len(imglinks)):
            img = imglinks[i]

            sql = "insert into Images(imageurl) values(%s)"

            try:
                cur.execute(sql,[imglinks[i]])

                sql = "select imageid from Images where imageurl = %s"

                cur.execute(sql,[img])

                result = cur.fetchall()

                for row in result:
                    imageid = row[0]
                    sql = "insert into PersonImages(personid,imageid) values(%s,%s)"
                    cur.execute(sql,[personid,imageid])
                    db.commit()
            except MySQLdb.Error, e:
                print e
                db.rollback()

            if i == photos_url_per_actor:
                print 'max photos '+`i`
                break

        db.commit()
        db.close()


