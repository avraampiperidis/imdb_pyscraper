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
import time
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    "Accept-Language": "en-US,en;q=0.5"}


def insert_episode(movieid,imdb,season,title,image,plot,episode):

    title = remove_all_special_chars(title)
    plot = remove_all_special_chars(plot)

    db = getCursor()
    cur = db.cursor()

    sql = "insert into Episodes(movieid,title,plot,poster,season,episode,imdb) values(%s,%s,%s,%s,%s,%s,%s)"

    try:
        cur.execute(sql,[movieid,title,plot,image,season,episode,imdb])
        db.commit()
    except MySQLdb.Error, e:
        print e




def insert_series(movieid,imdbid,poster):

    db = getCursor()
    cur = db.cursor()

    sql = "insert into Series(movieid,imdbid,poster) values(%s,%s,%s)"

    try:
        cur.execute(sql,[movieid,imdbid,poster])
        db.commit()
    except MySQLdb.Error ,e:
        print e


def insert_season(globalmovieid,imdb,seasonlink,season):
    print ''

    db = getCursor()
    cur = db.cursor()

    sql = "insert into Season(movieid,season,link) values(%s,%s,%s)"

    try:
        cur.execute(sql,[globalmovieid,season,seasonlink])
        db.commit()
    except MySQLdb.Error ,e:
        print e


    page = requests.get(seasonlink, headers=headers);
    tree = html.fromstring(page.content);
    tree.make_links_absolute(seasonlink)

    images = tree.xpath('//div[@class="list detail eplist"]//div[@class="image"]//img/@src')
    titles = tree.xpath('//div[@class="list detail eplist"]//div[@class="info"]//strong/a/@title')
    plot = tree.xpath('//div[@class="list detail eplist"]//div[@class="info"]//div[@class="item_description"]/text()')

    print len(images),len(titles),len(plot)

    for i in xrange(len(titles)):
        insert_episode(globalmovieid,imdb,season,titles[i].strip(),images[i].strip(),plot[i].strip(),i+1)


def insert_series_into_movie(imdb,globalmovieid,title,genre,content_rating,ratings,rating_value,plot,poster):

    db = getCursor()
    cur = db.cursor()

    if not rating_value:
        rating_value = 5

    if not content_rating:
        content_rating = "R"

    title = remove_all_special_chars(title)
    plot = remove_all_special_chars(plot)

    sql = "insert into Movie(movieid,imdbid,title,plot,altplot,genre,ratings,ratingvalue,contentrating,poster) " \
                  "values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % \
                  (globalmovieid,imdb,title.strip(),plot.strip()," ",genre,int(ratings),float(rating_value),content_rating,poster)

    try:
        cur.execute(sql)
        db.commit()
    except MySQLdb.Error, e:
        db.rollback()
        print e
