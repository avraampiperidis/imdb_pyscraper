# imdb_pyscraper
-------------

python program that scraps imdb.com and stores data into mysql db

Intro-Info
-----

All the movies/series in imdb.com are accessible from url <br>
http://www.imdb.com/title/tt[movie id]/<br>
witch starts from 0000001 and ends 9999999(!some of them are invalid,not taken yet)<br>
also a relationship between higher id and year of movie/series exists!
<br>
<br>
And all the actors are accessible from url:
http://www.imdb.com/name/nm[actor id]/
<br>
<br>
by incrementing movie id we get all movies,<br>
and from movies we get the actors, from every movie casts. <br>
<br>
Tv shows and series are also as movies.<br>
show it goes like this series->seasons->episodes.
<br>
<br>
plot,actors bio,photo urls,genres,episodes titles are included in the scraping proccess.
<br>
<br>
Mysql Db Setup
-----
Edit the conf.py for user mysql credentials.(be sure to have database creation privileges)<br>
Run init_create_db_schema.py OR init_create_db_schema_with_indexes_references.py.<br>
It will create the database and all its tables needed.<br>
The difference between this two is tha the init_create_db_schema_with_indexes_references.py,<br>
will create also indexes,references,keys,constraints,<br>
while the other create_db_schema.py will create only the databas+tables.<br>
Note for(init_create_db_schema_with_indexes_references.py) a lot amount of data the <br>
database will become slow for updates/new inserts ,and will geting slower as the program runs,<br>
and the data are geting even more.<br>
<br>
the mysql workbench schema -> https://github.com/avraampiperidis/imdb_pyscraper/blob/master/workbench_schema.mwb?raw=true

Run
-----
just run imdbmain.py


<br>
<br>
Configuration
-----
conf.py contains some user options.<br>
mysql connection credentials.<br>
imdb scrap options.



