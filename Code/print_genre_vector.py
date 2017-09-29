from __future__ import division
import pandas as pd
from datetime import datetime
from math import log
from operator import itemgetter
import sys

current_time = datetime.now()
tags = pd.read_csv('../phase1_testdata/mltags.csv')
movie_genre = pd.read_csv('../phase1_testdata/mlmovies.csv')
tags_details = pd.read_csv('../phase1_testdata/genome-tags.csv')
tag_vector = []
for i,row in tags.iterrows():
	tags.set_value(i,'timestamp', 1/(current_time-datetime.strptime(row['timestamp'],'%Y-%m-%d %H:%M:%S')).total_seconds())

movie_genre = pd.DataFrame(movie_genre.genres.str.split('|').tolist(), index = movie_genre.movieid).stack()
movie_genre = movie_genre.reset_index()[[0,'movieid']]
movie_genre.columns = ['genres','movieid']

# Get input arguments
genre = sys.argv[1]#'War'
model = sys.argv[2]#'tfidf'

f = open('../Output/output_genre_'+model+'.txt','w')
f.write('Genre is: '+ genre+'\n')
f.write('Model is: '+ model+'\n')

genres = movie_genre.genres.unique()
total_genres = len(genres)
movieids = movie_genre.where(movie_genre['genres']==genre).dropna().loc[:,'movieid']
movietags = tags.where(tags['movieid'].isin(movieids)).dropna()

distinct_tags = movietags.tagid.unique()
total_tag_weight = movietags['timestamp'].sum()

# Find the tag weght for each distinct tag
for tag in distinct_tags:
	movieid_with_tag = movietags.where(movietags['tagid']==tag).movieid.unique()
	genres_dfs = []
	for movie in movieid_with_tag:
		genres_dfs.append(movie_genre.where(movie_genre['movieid']==movie).dropna())
	genres_df = pd.concat(genres_dfs)
	genres = len(genres_df.genres.unique())
	
	tag_weight = movietags.loc[movietags['tagid']==tag]['timestamp'].sum()
	if(model == 'tfidf'):
		tag_vector.append([tags_details.where(tags_details['tagId']==tag).dropna().iloc[0,1], (tag_weight/total_tag_weight)*log(total_genres/genres)])
	if(model == 'tf'):
		tag_vector.append([tags_details.where(tags_details['tagId']==tag).dropna().iloc[0,1], (tag_weight/total_tag_weight)])
	tag_vector= sorted(tag_vector, key=itemgetter(1), reverse=True)

	
for vector in tag_vector:
	print >> f, vector
	print vector
f.close()