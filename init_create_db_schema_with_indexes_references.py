__author__ = 'abraham'

#---------------
#the extended mysql_database create schema
#this create script builds the database
#with indexes , references,foreign keys
#!!-->NOTE if there is to be inserted a lot of records
#-->  It will become very Slow at insert's because of the indexes
#-->  And will getting even slower as the data increases!
#-----------------------------
import MySQLdb


def getCursor():
   db = MySQLdb.connect(host="127.0.0.1",
                     user="root",
                     passwd="1zeronerone",
                     )
   return db


cursor = getCursor().cursor()

#imdb database create
#cursor.execute('drop database imdb')
cursor.execute('create database if not exists imdb')
cursor.execute('use imdb')

#tables create
sql_create_table_movie = """
CREATE TABLE IF NOT EXISTS `Movie` (
  `movieid` INT(11) NOT NULL,
  `imdbid` VARCHAR(8) CHARACTER SET 'latin1' NOT NULL,
  `title` VARCHAR(50) NULL DEFAULT NULL,
  `plot` TEXT NULL DEFAULT NULL,
  `altplot` TEXT NULL DEFAULT NULL,
  `date` TEXT NULL DEFAULT NULL,
  `year` INT(11) NULL DEFAULT NULL,
  `month` INT(11) NULL DEFAULT NULL,
  `day` INT(11) NULL DEFAULT NULL,
  `genre` VARCHAR(50) NULL DEFAULT NULL,
  `ratings` INT(11) NULL DEFAULT NULL,
  `ratingvalue` FLOAT NULL DEFAULT NULL,
  `contentrating` VARCHAR(45) NULL DEFAULT NULL,
  `poster` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`movieid`, `imdbid`),
  UNIQUE INDEX `id_UNIQUE` (`movieid` ASC),
  UNIQUE INDEX `imdbid_UNIQUE` (`imdbid` ASC),
  INDEX `title_index` (`title` ASC),
  INDEX `year_index` (`year` ASC),
  INDEX `genre_index` (`genre` ASC),
  INDEX `ratings_index` (`ratings` ASC),
  INDEX `genre_rating_index` (`genre` ASC, `ratings` ASC),
  INDEX `genre_title_index` (`genre` ASC, `title` ASC),
  INDEX `year_ratings_index` (`year` ASC, `ratings` ASC),
  INDEX `year_ratingvalue_index` USING BTREE (`year` ASC, `ratingvalue` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
"""


sql_create_table_casts = """
CREATE TABLE IF NOT EXISTS `Casts` (
  `name` VARCHAR(80) NULL DEFAULT NULL,
  `lastname` VARCHAR(80) NULL DEFAULT NULL,
  `personid` INT(11) NOT NULL DEFAULT '0',
  `imdbid` INT(11) NOT NULL DEFAULT '0',
  `moviename` VARCHAR(160) NULL DEFAULT NULL,
  PRIMARY KEY (`personid`, `imdbid`),
  INDEX `imdbid` (`imdbid` ASC),
  INDEX `name_index` (`name` ASC),
  INDEX `lastname_index` USING BTREE (`lastname` ASC),
  CONSTRAINT `Casts_ibfk_1`
    FOREIGN KEY (`personid`)
    REFERENCES `Persons` (`personid`),
  CONSTRAINT `Casts_ibfk_2`
    FOREIGN KEY (`imdbid`)
    REFERENCES `Movie` (`movieid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
"""


sql_create_table_persons = """
CREATE TABLE IF NOT EXISTS `Persons` (
  `personid` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) NULL DEFAULT NULL,
  `lastname` VARCHAR(80) NULL DEFAULT NULL,
  `birth` TEXT NULL DEFAULT NULL,
  `age` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`personid`),
  UNIQUE INDEX `id_UNIQUE` (`personid` ASC),
  INDEX `name_index` (`name` ASC),
  INDEX `lastname_index` USING BTREE (`lastname` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
"""


sql_create_table_personinfo = """
CREATE TABLE IF NOT EXISTS `PersonInfo` (
  `personinfoid` INT(11) NOT NULL AUTO_INCREMENT,
  `bio` LONGTEXT NULL DEFAULT NULL,
  `trivia` LONGTEXT NULL DEFAULT NULL,
  `personquotes` LONGTEXT NULL DEFAULT NULL,
  `personid` INT(11) NULL DEFAULT NULL,
  `profilepic` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`personinfoid`),
  UNIQUE INDEX `id_UNIQUE` (`personinfoid` ASC),
  INDEX `id_idx` (`personid` ASC),
  CONSTRAINT `personidpersoninfo`
    FOREIGN KEY (`personid`)
    REFERENCES `Persons` (`personid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
"""

sql_create_table_images = """
CREATE TABLE IF NOT EXISTS `Images` (
  `imageid` INT(11) NOT NULL AUTO_INCREMENT,
  `imageurl` TEXT NOT NULL,
  PRIMARY KEY (`imageid`),
  UNIQUE INDEX `id_UNIQUE` (`imageid` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
"""

sql_create_table_personimages = """
CREATE TABLE IF NOT EXISTS `PersonImages` (
  `personimageid` INT(11) NOT NULL AUTO_INCREMENT,
  `personid` INT(11) NULL DEFAULT NULL,
  `imageid` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`personimageid`),
  UNIQUE INDEX `personimageid_UNIQUE` (`personimageid` ASC),
  INDEX `imageid_idx` (`imageid` ASC),
  INDEX `personidpersonimg` (`personid` ASC),
  CONSTRAINT `imageidpersonimg`
    FOREIGN KEY (`imageid`)
    REFERENCES `Images` (`imageid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `personidpersonimg`
    FOREIGN KEY (`personid`)
    REFERENCES `Persons` (`personid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
"""

sql_create_table_movieimages = """
CREATE TABLE IF NOT EXISTS `MovieImages` (
  `movieimageid` INT(11) NOT NULL AUTO_INCREMENT,
  `movieid` INT(11) NULL DEFAULT NULL,
  `imageid` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`movieimageid`),
  INDEX `imageid_idx` (`imageid` ASC),
  INDEX `movieidmovieimg` (`movieid` ASC),
  CONSTRAINT `imageidmovieimg`
    FOREIGN KEY (`imageid`)
    REFERENCES `Images` (`imageid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `movieidmovieimg`
    FOREIGN KEY (`movieid`)
    REFERENCES `Movie` (`movieid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
"""

sql_create_table_series = """
CREATE TABLE IF NOT EXISTS `Series` (
  `seriesid` INT(11) NOT NULL AUTO_INCREMENT,
  `movieid` INT(11) NULL DEFAULT NULL,
  `imdbid` VARCHAR(8) NULL DEFAULT NULL,
  `poster` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`seriesid`),
  UNIQUE INDEX `seriesid_UNIQUE` (`seriesid` ASC),
  INDEX `movieid_idx` (`movieid` ASC),
  CONSTRAINT `movieid`
    FOREIGN KEY (`movieid`)
    REFERENCES `Movie` (`movieid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
"""

sql_create_table_season = """
CREATE TABLE IF NOT EXISTS `Season` (
  `seasonid` INT(11) NOT NULL AUTO_INCREMENT,
  `movieid` INT(11) NULL DEFAULT NULL,
  `season` INT(11) NULL DEFAULT '0',
  `link` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`seasonid`),
  UNIQUE INDEX `seasonid_UNIQUE` (`seasonid` ASC),
  INDEX `movieid_idx` (`movieid` ASC),
  INDEX `season_index` USING BTREE (`season` ASC),
  CONSTRAINT `movieidseason`
    FOREIGN KEY (`movieid`)
    REFERENCES `Series` (`movieid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
"""

sql_create_table_episodes = """
CREATE TABLE IF NOT EXISTS `Episodes` (
  `episodeid` INT(11) NOT NULL AUTO_INCREMENT,
  `movieid` INT(11) NULL DEFAULT NULL,
  `title` TEXT NULL DEFAULT NULL,
  `plot` TEXT NULL DEFAULT NULL,
  `poster` TEXT NULL DEFAULT NULL,
  `season` INT(11) NULL DEFAULT NULL,
  `episode` INT(11) NULL DEFAULT NULL,
  `imdb` VARCHAR(10) NULL DEFAULT NULL,
  PRIMARY KEY (`episodeid`),
  UNIQUE INDEX `episodeid_UNIQUE` (`episodeid` ASC),
  INDEX `movieid_idx3` (`movieid` ASC),
  CONSTRAINT `movieidepisode`
    FOREIGN KEY (`movieid`)
    REFERENCES `Season` (`movieid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
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

print('creating table movie...')
cursor.execute(sql_create_table_movie)

print('creating table images...')
cursor.execute(sql_create_table_images)

print('creating table persons...')
cursor.execute(sql_create_table_persons)

print('creating table casts...')
cursor.execute(sql_create_table_casts)

print('creating table personinfo...')
cursor.execute(sql_create_table_personinfo)

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


print('Done..All tables created')

