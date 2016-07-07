# -*- coding: utf-8 -*-
__author__ = 'abraham'

from lxml import html
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.stdout.encoding
import requests
from initidarray import *
from actorscraper import scrapActor
from moviedbutil import moviedb
from photoscraper import photoscrap
from seriesscraper import seriesscrap
from db import getCursor
from utils import remove_all_special_chars
from utils import getMaxMovieid
from conf import imdb_min_ratings_count
from userreviews import scrap_user_reviews



headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    "Accept-Language": "en-US,en;q=0.8"}

idarr = initidarray()


globalmovieid = getMaxMovieid()
for i in idarr:

    print '\n'
    print '|--->scraping->', i, '\n'
    link = 'http://www.imdb.com/title/tt' +i+ '/'

    page = requests.get(link, headers=headers);
    tree = html.fromstring(page.content);
    tree.make_links_absolute(link)

    try:

        title = tree.xpath('//h1/text()')
        titleoriginal = tree.xpath('//div[@class="originalTitle"]/text()')
        if titleoriginal:
            title = titleoriginal

        year = tree.xpath('//h1/span[@id="titleYear"]/a/text()')
        content_rating = tree.xpath('//div[@class="titleBar"]/div[@class="title_wrapper"]/div[@class="subtext"]/meta/@content')
        genre = tree.xpath('//div[@class="titleBar"]//span[@class="itemprop"]/text()')
        imgurl = tree.xpath('//div[@class="poster"]//img/@src')
        plot = tree.xpath('//div[@class="plot_summary_wrapper"]//div[@class="summary_text"]/text()')
        casts = tree.xpath('//table[@class="cast_list"]//tr[position() > 1]//td[@class="itemprop"]//span[@class="itemprop"]/text()')
        castslink = tree.xpath('//table[@class="cast_list"]//tr[position() > 1]//td[@class="itemprop"]/a/@href')
        castusername = tree.xpath('//table[@class="cast_list"]//tr[position() > 1]//td[@class="character"]/div/a[1]/text()')
        ratings = tree.xpath('//div[@class="imdbRating"]//span[@itemprop="ratingCount"]/text()')
        rating_value = tree.xpath('//div[@class="imdbRating"]/div[@class="ratingValue"]//span[@itemprop="ratingValue"]/text()')
        poster = tree.xpath('//div[@class="poster"]//img/@src')
        moviephotosurl = tree.xpath('//div[@class="combined-see-more see-more"]/a[1]/@href')
        release_date = tree.xpath('//div[@class="titleBar"]//div[@class="subtext"]/a[last()]/text()')
        review_link = tree.xpath('//div[@class="titleReviewBarItem titleReviewbarItemBorder"]//span[@class="subText"]/a/@href')

        date = release_date[0]
        datelist = date.split()

        print len(casts)
        print len(castslink)
        print len(castusername)

        ratings = ratings[0].replace(",","")


        # usualy tv series dont have year in title only in genre stats
        if not year:
            year = release_date

        # skip all the adult content
        if "Adult" not in genre:
                if "Short" not in genre:
                    if "18" not in content_rating:
                        if "X" not in content_rating:
                            if int(ratings) > imdb_min_ratings_count:
                                if imgurl:
                                  if plot:
                                    if casts:

                                        print genre
                                        print content_rating
                                        print ratings
                                        print rating_value
                                        print title, '(', year, ')'
                                        print imgurl

                                        title = ' '.join(title).strip()
                                        title = remove_all_special_chars(title)

                                        if not content_rating:
                                            content_rating = ['R']

                                        if "TV Series" in year[0]:
                                           seriesscrap(i,globalmovieid,title,datelist,' '.join(genre),content_rating[0],ratings,rating_value[0],''.join(plot).strip(),link,poster[0].strip())
                                           if review_link:
                                               scrap_user_reviews(globalmovieid,review_link[0].strip())
                                        else:
                                           moviedb(i,globalmovieid,title,datelist,' '.join(genre),content_rating[0],ratings,rating_value[0],''.join(plot).strip(),link,poster[0].strip())
                                           if review_link:
                                               scrap_user_reviews(globalmovieid,review_link[0].strip())

                                        for actor in xrange(len(casts)):
                                            if len(casts) == len(castusername):
                                               scrapActor(i,globalmovieid,casts[actor],castslink[actor],castusername[actor])
                                            else:
                                               scrapActor(i,globalmovieid,casts[actor],castslink[actor]," ")


                                        if poster:
                                            if moviephotosurl:
                                               photoscrap(i,globalmovieid,moviephotosurl[0].strip())
                                            else:
                                               photoscrap(i,globalmovieid,[])

                                        globalmovieid += 1


    #
    except BaseException, e:
      #insert into error table the exception
      #db = getCursor()
      #cur = db.cursor()

      print e
      #fix this. insert specific errors

      #sql = "insert into Errors(movieid,info,level) values('%s','%s','%s')" % \
      #      (globalmovieid,i,"movie")

      #try:
      #  cur.execute(sql)
      #  db.commit()

      #except MySQLdb.Error, e:
      #    print "error",e
      #    db.rollback()

      #db.close()



