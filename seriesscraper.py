# -*- coding: utf-8 -*-
__author__ = 'abraham'

from lxml import html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
from seriesdbutils import *
from db import getCursor
import time
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    "Accept-Language": "en-US,en;q=0.5"}


def seriesscrap(imdb,globalmovieid,title,datelist,genre,content_rating,ratings,rating_value,plot,link,poster):
    print "Tv series scrap..."

    #check if series exists
    db = getCursor()
    cur = db.cursor()

    cur.execute("select count(1) from Series where movieid = %s", [globalmovieid])

    if cur.fetchone()[0]:
        #if exists check if new season exists or new episodes and update
        print ''

    else:
        #get num of seasons and for every season the episodes
        #every episode title ,image,mini plot
        page = requests.get(link, headers=headers);
        tree = html.fromstring(page.content);
        tree.make_links_absolute(link)

        seasonlinks = tree.xpath('//div[@class="seasons-and-year-nav"]//br[@class="clear"]/following-sibling::div[1]/a/@href')
        seasonsnum = tree.xpath('//div[@class="seasons-and-year-nav"]//br[@class="clear"]/following-sibling::div[1]/a/text()')

        print len(seasonlinks)
        print len(seasonsnum)

        if len(seasonlinks) > 0:

            #first insert into Movie
            insert_series_into_movie(imdb,globalmovieid,title,genre,content_rating,ratings,rating_value,plot,poster)

            #Then insert into series
            insert_series(globalmovieid,imdb,poster)

            link = ("http://www.imdb.com/title/tt",str(imdb),"/")

            base_link = ''.join(link)

            if "See all" in ' '.join(seasonsnum):
                print "See all"
                maxseason = int(seasonsnum[0])
                for i in xrange(maxseason):
                    seasonlink = [base_link,"episodes?season=",str((i + 1)),"&ref_=tt_eps_sn_",str((i+1))]
                    print ''.join(seasonlink)
                    insert_season(globalmovieid,imdb,''.join(seasonlink),(i+1))

            else:
                print 'Not See all'
                for i in xrange(len(seasonlinks)):
                    print seasonsnum[i],seasonlinks[i]
                    seasonlink = [base_link,"episodes?season=",str((i+1)),"&ref_=tt_eps_sn_",str((i+1))]
                    insert_season(globalmovieid,imdb,''.join(seasonlink).strip(),(i+1))





def test_series():
    seriesscrap("0944947",121,"game of thrones","datelist","Drama","R","10050","8.6","game of thrones plot ...summary...","http://www.imdb.com/name/nm0917467/mediaindex?ref_=nm_phs_md_sm","posterlink")
    seriesscrap("0460681",122,"supernatural","datelist","Action Drama","R","280000","8.1","supernatural plot","http://www.imdb.com/title/tt0460681/","poster link")
    seriesscrap("0423776",123,"the xfactor","","Drama","R","1000","5","xfactor plot","http://www.imdb.com/title/tt0423776/","")
    seriesscrap("2712516",124,"The thundermans","","","R","1000","1","","http://www.imdb.com/title/tt2712516/","")
    seriesscrap("0096697",125,"The simpsons","","","R","1500","8","plot","http://www.imdb.com/title/tt0096697/","")
    seriesscrap("2453016",126,"Marvin marvin","","","R","1500","5.5","","http://www.imdb.com/title/tt2453016/","")


