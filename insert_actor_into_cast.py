# -*- coding: utf-8 -*-
__author__ = 'abraham'
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from utils import *
from db import getCursor


def insert_actor_to_casts(globalmovieid,name,lastname,username):

    db = getCursor()
    cur = db.cursor()

    #check if is in this movie casts
    sql = "select personid from Persons where name = %s and lastname = %s "

    try:
           cur.execute(sql, [name,lastname])

           result = cur.fetchall()

           for row in result:
               personid = row[0]


               sql = "select count(1) from Casts where imdbid = %s and personid = %s "
               cur.execute(sql, [globalmovieid,personid])

               if cur.fetchone()[0]:
                   print "Actor is in this movie cast"
                   #done nothing to update
                   #if its not insert to casts
               else:

                   sql = "insert into Casts(name,lastname,personid,imdbid,moviename) values(%s,%s,%s,%s,%s)"

                   try:
                      cur.execute(sql,[name,lastname,personid,globalmovieid,username])
                      db.commit()
                   except MySQLdb.Error, e:
                       db.rollback()
                       print e

           cur.close()

    except:
        print 'Error...'
        db.rollback()


def getPersonsId(name,lastname):
    db = getCursor()
    cur = db.cursor()

    #check if is in this movie casts
    sql = "select personid from Persons where name = %s and lastname = %s "

    try:
        cur.execute(sql,[name,lastname])
        result = cur.fetchall()

        for row in result:
            personid = row[0]
            return personid

    except MySQLdb.Error, e:
        print e