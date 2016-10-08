__author__ = 'abraham'

from lxml import html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
from seriesdbutils import *
from db import getCursor
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    "Accept-Language": "en-US,en;q=0.5"}

def scrap_user_reviews(movieid,review_url):

    page = requests.get(review_url, headers=headers);
    tree = html.fromstring(page.content);
    tree.make_links_absolute(review_url)

    reviews = tree.xpath('//div[@class="yn"]/preceding-sibling::p/text()[1]')
    review_titles = tree.xpath('//h2/text()')

    print len(reviews)
    print len(review_titles)
    if reviews:
        if review_titles:
            if len(reviews) == len(review_titles):
                print movieid
                print 'insert review...'
                print review_url
                db = getCursor()
                for i in xrange(len(review_titles)):
                   title = review_titles[i].strip()
                   review = reviews[i].strip()
                   cur = db.cursor()
                   sql = "insert into reviews(movieid,title,review) values(%s,%s,%s)"
                   try:
                      cur.execute(sql,[movieid,title,review])
                      db.commit()
                   except MySQLdb.Error, e:
                      db.rollback()
                      print e
                db.close()









def test_scrap_user_reviews():
    scrap_user_reviews(-1,"http://www.imdb.com/title/adfasdf/reviews?ref_=tt_ov_rt")
    scrap_user_reviews(-2,"http://www.imdb.com/title/tt3949660/reviews?ref_=tt_ov_rt")
    scrap_user_reviews(-3,"http://www.imdb.com/title/tt0877057/reviews?ref_=tt_ov_rt")
    scrap_user_reviews(-4,"http://www.imdb.com/title/tt0944947/reviews?ref_=tt_ov_rt")
    scrap_user_reviews(-5,"http://www.imdb.com/title/tt0137523/reviews?ref_=tt_ov_rt")
    scrap_user_reviews(-6,"http://www.imdb.com/title/tt0241527/reviews?ref_=tt_ov_rt")


def test_get_review_links(link):

    page = requests.get(link, headers=headers);
    tree = html.fromstring(page.content);
    tree.make_links_absolute(link)
    review_link = tree.xpath('//div[@class="titleReviewBarItem titleReviewbarItemBorder"]//span[@class="subText"]/a/@href')
    if review_link:
        print review_link[0].strip()


def get_review_links():

    test_get_review_links("http://www.imdb.com/title/asdf/")
    test_get_review_links("http://www.imdb.com/title/tt0944947/")
    test_get_review_links("http://www.imdb.com/title/tt1888075/")
    test_get_review_links("http://www.imdb.com/title/tt2372162/")


