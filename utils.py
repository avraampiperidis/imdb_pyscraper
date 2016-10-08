# -*- coding: utf-8 -*-
__author__ = 'abraham'
from datetime import datetime
import sys
from db import *
reload(sys)
sys.setdefaultencoding('utf-8')
import time

def month_to_int(month):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return months.index(month) + 1

#this method can be replaced with regex
def remove_all_special_chars(text):
    text = text.replace("'","")
    text = text.replace("/","//")
    text = text.replace("\\","/")
    text = text.replace(";",".")
    text = text.replace(":",".")
    text = text.replace("*",".")
    text = text.replace("%",".")
    text = text.replace("$",".")
    text = text.replace("^",".")
    text = text.replace("`",".")
    text = text.replace("\"","")

    return text



def is_date_older_2months(date):

    month_in_secs = 2678400

    day = date[0]
    if day == "0":
        day = "1"
    month = date[1]
    year = date[2]

    asd = int(year)
    if asd < 1971:
        year = "1971"

    monthint = int(month_to_int(month))

    datenow = time.strftime("%d/%m/%Y")
    moviedate = str(day)+"/"+str(monthint)+"/"+str(year)

    dnow = datetime.strptime(datenow, "%d/%m/%Y")
    dmovie = datetime.strptime(moviedate, "%d/%m/%Y")
    inow = int(time.mktime(dnow.timetuple()) )
    imovie = int(time.mktime(dmovie.timetuple()))

    dif = inow - imovie

    if dif > month_in_secs:
        return False
    else:
        return True

def getMaxMovieid():

    db = getCursor()
    cur = db.cursor()

    sql = "SELECT max(Movie.movieid) FROM Movie"

    cur.execute(sql)

    result = cur.fetchall()

    for row in result:
        movieid = row[0]
        if movieid == None:
            return 0
        else:
            return row[0]
