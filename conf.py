#configuration settings for mysql database
#and imdb scrap option

#mysql options
db_host = '127.0.0.1'
db_username = 'root'
db_passwd = 'password'
db_name = 'imdb'


#-------->imdb.com scrap options<--------------
#
#will not scrap if the movie number of ratings is bellow than this
#the higher the value the more famous the movie/series
#is not to be confused with rating value! this is just how many users have rated the movie
imdb_min_ratings_count = 1000



#the movie id to start
#!this must be bigger from imdb_id_stop_in
#DEFAULT VALUE imdb_id_start_from = 0, min value = 0
#EG: imdb_id_start_from = 1000
#will start from http://www.imdb.com/title/tt0001000/
imdb_id_start_from = 0

#the movie id to stop
#!This must be smaller from imdb_id_start_from
#DEFAULT VALUE imdb_id_stop_in = 9999999 , max value = 9999999
#will stop in http://www.imdb.com/title/tt9999999/
imdb_id_stop_in = 9999999



#this photo urls are small 100x100 px
#the number of photo urls to be scan per actor
#!i think the maximum is 50 setting higher than 50 wont change anything
photos_url_per_actor = 24

#this photo urls are small 100x100 px
photos_url_per_movie_series = 24
