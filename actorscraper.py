# -*- coding: utf-8 -*-
__author__ = 'abraham'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from lxml import html
import MySQLdb
from utils import *
from db import getCursor
from actorphotoscrap import actorphoto
from insert_actor_into_cast import *

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    "Accept-Language": "en-US,en;q=0.5"}


def scrapActor(i,globalmovieid,actor,link,username):
    print 'actor scraping start...'
    print actor,link
    db = getCursor()
    cur = db.cursor()
    #first check if actor already in database
    actor = remove_all_special_chars(actor)
    actor = actor.split(" ")
    username = remove_all_special_chars(username)
    name = ""
    lastname = ""
    if len(actor) == 1:
       name = actor[0]
    else:
        name = actor[0]
        lastname = actor[1]

    cur.execute("select count(1) from Persons where name = %s and lastname = %s ", [name,lastname])
    if cur.fetchone()[0]:
        print 'Actor exits'
        #check if is in this movie casts
        insert_actor_to_casts(globalmovieid,name,lastname,username)
    else:
        print 'new Actor'
        #1first Persons
        #bio info
        #Born date
        page = requests.get(link, headers=headers);
        tree = html.fromstring(page.content);
        tree.make_links_absolute(link)

        shortbio = tree.xpath('//div[@class="name-trivia-bio-text"]/div[@class="inline"]/text()')
        fullbiolink = tree.xpath('//div[@class="name-trivia-bio-text"]/div[@class="inline"]/span/a/@href')
        borndate = tree.xpath('//div[@id="name-born-info"]/time/@datetime')
        profilepic = tree.xpath('//td[@id="img_primary"]/div[@class="image"]/a/img/@src')
        photosurl = tree.xpath('//div[@class="see-more"]/a[1]/@href')

        #insert into persons
        if shortbio:
            if profilepic:
                if not borndate:
                    borndate = [" "]

                db = getCursor()
                cur = db.cursor()

                sql = "insert into Persons(name,lastname,birth) values(%s,%s,%s)"
                try:
                    cur.execute(sql,[name,lastname,' '.join(borndate)])
                    db.commit()
                except MySQLdb.Error, e:
                    print e
                    db.rollback()
                    actorinfo = []
                    actorinfo.append("Actor")
                    actorinfo.append(name)
                    actorinfo.append(lastname)
                    sql = "insert into Errors(movieid,info,level) values('%s','%s','%s')" % \
                    (globalmovieid,i,' '.join(actorinfo))
                    try:
                      cur.execute(sql)
                      db.commit()
                    except MySQLdb.Error, e:
                      print "error",e
                      db.rollback()
                    db.close()


                #2then casts
                insert_actor_to_casts(globalmovieid,name,lastname,username)
                #3then personsInfo
                if fullbiolink:
                    page = requests.get(fullbiolink[0], headers=headers);
                    tree = html.fromstring(page.content);
                    tree.make_links_absolute(fullbiolink[0])

                    minibio = tree.xpath('//div[@id="bio_content"]/div[@class="soda odd"]/p[1]/text()')
                    minibio = remove_all_special_chars(''.join(minibio))
                    #if any exists from below
                    #mini bio
                    #trivia
                    #Personal Quotes
                    #insert extra info link bio trivia personal quotes to personinfo
                    personid = getPersonsId(name,lastname)
                    db = getCursor()
                    cur = db.cursor()
                    sql = "insert into PersonInfo(bio,personid,profilepic) values(%s,%s,%s)"
                    try:
                        cur.execute(sql,[minibio.strip(),personid,''.join(profilepic).strip()])
                        db.commit()
                    except MySQLdb.Error, e:
                        print e
                    #4Last photos from photo page
                    if photosurl:
                        actorphoto(personid,''.join(photosurl[0]))
                else:
                    print ''



