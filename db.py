__author__ = 'abraham'

import MySQLdb
from conf import db_host
from conf import db_name
from conf import db_passwd
from conf import db_username


def getCursor():
   db = MySQLdb.connect(host=db_host,
                     user=db_username,
                     passwd=db_passwd,
                     db=db_name
                     )
   return db

