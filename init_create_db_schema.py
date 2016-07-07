__author__ = 'abraham'
from conf import db_host
from conf import db_name
from conf import db_passwd
from conf import db_username
#---------------
#the basic mysql_database schema
#without indexes ,references,foreign keys!
#
#good option if there is a lot of data to be inserted
#-----------------------------
import MySQLdb


def getCursor():
   db = MySQLdb.connect(host=db_host,
                     user=db_username,
                     passwd=db_passwd,
                     )
   return db


cursor = getCursor().cursor()

#imdb database create
#cursor.execute('drop database imdb')
cursor.execute('create database if not exists imdb')
cursor.execute('use imdb')

#tables create
sql_create_table_movie = """
CREATE TABLE `movie` (
  `movieid` int(11) NOT NULL,
  `imdbid` varchar(8) CHARACTER SET latin1 NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `plot` text,
  `altplot` text,
  `date` text,
  `year` int(11) DEFAULT NULL,
  `month` int(11) DEFAULT NULL,
  `day` int(11) DEFAULT NULL,
  `genre` varchar(50) DEFAULT NULL,
  `ratings` int(11) DEFAULT NULL,
  `ratingvalue` float DEFAULT NULL,
  `contentrating` varchar(45) DEFAULT NULL,
  `poster` text,
  PRIMARY KEY (`movieid`,`imdbid`),
  UNIQUE KEY `id_UNIQUE` (`movieid`),
  UNIQUE KEY `imdbid_UNIQUE` (`imdbid`),
  KEY `index_year` (`year`) USING BTREE,
  KEY `index_ratings` (`ratings`) USING BTREE,
  KEY `index_genres` (`genre`) USING BTREE,
  KEY `index_title` (`title`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


sql_create_table_casts = """
CREATE TABLE `casts` (
  `name` varchar(80) DEFAULT NULL,
  `lastname` varchar(80) DEFAULT NULL,
  `personid` int(11) NOT NULL DEFAULT '0',
  `imdbid` int(11) NOT NULL DEFAULT '0',
  `moviename` varchar(160) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


sql_create_table_persons = """
CREATE TABLE `persons` (
  `personid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `lastname` varchar(80) DEFAULT NULL,
  `birth` text,
  `age` int(11) DEFAULT NULL,
  PRIMARY KEY (`personid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
"""


sql_create_table_personinfo = """
CREATE TABLE `personinfo` (
  `personinfoid` int(11) NOT NULL AUTO_INCREMENT,
  `bio` longtext,
  `trivia` longtext,
  `personquotes` longtext,
  `personid` int(11) DEFAULT NULL,
  `profilepic` text,
  PRIMARY KEY (`personinfoid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
"""

sql_create_table_images = """
CREATE TABLE `images` (
  `imageid` int(11) NOT NULL AUTO_INCREMENT,
  `imageurl` varchar(250) NOT NULL,
  UNIQUE KEY `imageid_UNIQUE` (`imageid`),
  KEY `imageurl` (`imageurl`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
"""

sql_create_table_personimages = """
CREATE TABLE `personimages` (
  `personimageid` int(11) NOT NULL AUTO_INCREMENT,
  `personid` int(11) NOT NULL,
  `imageid` int(11) DEFAULT NULL,
  PRIMARY KEY (`personimageid`,`personid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
"""

sql_create_table_movieimages = """
CREATE TABLE `movieimages` (
  `movieimageid` int(11) NOT NULL AUTO_INCREMENT,
  `movieid` int(11) DEFAULT NULL,
  `imageid` int(11) DEFAULT NULL,
  PRIMARY KEY (`movieimageid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
"""

sql_create_table_series = """
CREATE TABLE `series` (
  `seriesid` int(11) NOT NULL AUTO_INCREMENT,
  `movieid` int(11) DEFAULT NULL,
  `imdbid` varchar(8) DEFAULT NULL,
  `poster` text,
  PRIMARY KEY (`seriesid`),
  UNIQUE KEY `seriesid_UNIQUE` (`seriesid`),
  KEY `movieid_idx` (`movieid`),
  CONSTRAINT `movieid` FOREIGN KEY (`movieid`) REFERENCES `movie` (`movieid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
"""

sql_create_table_season = """
CREATE TABLE `season` (
  `seasonid` int(11) NOT NULL AUTO_INCREMENT,
  `movieid` int(11) DEFAULT NULL,
  `season` int(11) DEFAULT '0',
  `link` text,
  PRIMARY KEY (`seasonid`),
  UNIQUE KEY `seasonid_UNIQUE` (`seasonid`),
  KEY `movieid_idx2` (`movieid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
"""

sql_create_table_episodes = """
CREATE TABLE `episodes` (
  `episodeid` int(11) NOT NULL AUTO_INCREMENT,
  `movieid` int(11) DEFAULT NULL,
  `title` text,
  `plot` text,
  `poster` text,
  `season` int(11) DEFAULT NULL,
  `episode` int(11) DEFAULT NULL,
  `imdb` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`episodeid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
"""

sql_create_table_comingsoon = """
CREATE TABLE `comingsoon` (
  `comingsoonid` int(11) NOT NULL,
  `movieid` int(11) NOT NULL,
  `title` text,
  `plot` text,
  `date` text,
  `year` int(11) DEFAULT NULL,
  `month` int(11) DEFAULT NULL,
  `day` int(11) DEFAULT NULL,
  `genre` text,
  `poster` text,
  PRIMARY KEY (`comingsoonid`,`movieid`),
  UNIQUE KEY `comingsoonid_UNIQUE` (`comingsoonid`),
  UNIQUE KEY `movieid_UNIQUE` (`movieid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

sql_create_table_reviews = """
CREATE TABLE `reviews` (
  `movieid` int(11) DEFAULT NULL,
  `title` text,
  `review` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SELECT * FROM moviecloud.reviews;
"""

print('creating table movie...')
cursor.execute(sql_create_table_movie)

print('creating table casts...')
cursor.execute(sql_create_table_casts)

print('creating table persons...')
cursor.execute(sql_create_table_persons)

print('creating table personinfo...')
cursor.execute(sql_create_table_personinfo)

print('creating table images...')
cursor.execute(sql_create_table_images)

print('creating table movieimages...')
cursor.execute(sql_create_table_movieimages)

print('creating table personimages...')
cursor.execute(sql_create_table_personimages)

print('creating table series...')
cursor.execute(sql_create_table_series)

print('creating table season...')
cursor.execute(sql_create_table_season)

print('creating table episodes...')
cursor.execute(sql_create_table_episodes)

print('creating table comingsoon...')
cursor.execute(sql_create_table_comingsoon)

print('creating table reviews...')
cursor.execute(sql_create_table_reviews)


print('Done..All tables created')

