from __future__ import division
import pandas as pd
from datetime import datetime
from math import log
from operator import itemgetter
import sys

current_time = datetime.now()
tags = pd.read_csv('../phase1_dataset/mltags.csv')
movie_genre = pd.read_csv('../phase1_dataset/mlmovies.csv')
tags_details = pd.read_csv('../phase1_dataset/genome-tags.csv')

for i,row in tags.iterrows():
	tags.set_value(i,'timestamp', 1/(current_time-datetime.strptime(row['timestamp'],'%Y-%m-%d %H:%M:%S')).total_seconds())

# Get input arguments
genre1 = sys.argv[1]#'Thriller'
genre2 = sys.argv[2]#'Comedy'
model = sys.argv[3]#'P-DIFF1'

f = open('../Output/output_differentiate_'+model+'.txt','w') 

# Get movie ids for given genre and calculate the count
movie_genre = pd.DataFrame(movie_genre.genres.str.split('|').tolist(), index = movie_genre.movieid).stack()
movie_genre = movie_genre.reset_index()[[0,'movieid']]
movie_genre.columns = ['genres','movieid']

movieids_genre1 = movie_genre.where(movie_genre['genres']==genre1).dropna().loc[:,'movieid']
movieids_genre2 = movie_genre.where(movie_genre['genres']==genre2).dropna().loc[:,'movieid']

count_g1 = movieids_genre1.count()
count_g2 = movieids_genre2.count()
movieids_genre12 = pd.concat([movieids_genre1,movieids_genre2]).unique()
total_count = len(movieids_genre12)


genres_12 = []
for movie in movieids_genre1:
	genres_12.append(movie_genre.where(movie_genre['movieid']==movie).dropna())
for movie in movieids_genre2:
	genres_12.append(movie_genre.where(movie_genre['movieid']==movie).dropna())
genres_total_df = pd.concat(genres_12)
total_genres = len(genres_total_df.genres.unique())

# find differentiating tag vector based on tf-idf diff model
def tf_idf(genre):
	tag_vector = []
	movieids = movie_genre.where(movie_genre['genres']==genre).dropna().loc[:,'movieid']
	movietags = tags.where(tags['movieid'].isin(movieids)).dropna()

	distinct_tags = movietags.tagid.unique()
	total_tag_weight = movietags['timestamp'].sum()

	for tag in distinct_tags:
		movieid_with_tag = movietags.where(movietags['tagid']==tag).movieid.unique()
		genres_dfs = []
		for movie in movieid_with_tag:
			genres_dfs.append(movie_genre.where(movie_genre['movieid']==movie).dropna())
		genres_df = pd.concat(genres_dfs)
		genres = len(genres_df.genres.unique())
		
		tag_weight = movietags.loc[movietags['tagid']==tag]['timestamp'].sum()
		tag_vector.append([tags_details.where(tags_details['tagId']==tag).dropna().iloc[0,1], (tag_weight/total_tag_weight)*log(total_genres/genres)])
		
		tag_vector= sorted(tag_vector, key=itemgetter(1), reverse=True)
	for vector in tag_vector:
		print >> f, vector
		print vector
	return tag_vector

# find differentiating tag vector based on pdiff1 model
def pdiff1():
	tag_vector_genre1 = []
	tag_vector_genre2 = []

	movietags_genre1 = tags.where(tags['movieid'].isin(movieids_genre1)).dropna()
	movietags_genre2 = tags.where(tags['movieid'].isin(movieids_genre2)).dropna()
	movietags_genre12 = tags.where(tags['movieid'].isin(movieids_genre12)).dropna()
	distinct_tags_genre1 = movietags_genre1.tagid.unique()

	for tag in distinct_tags_genre1:
		movieid_with_tag_genre1 = movietags_genre1.where(movietags_genre1['tagid']==tag).movieid.unique()
		r1 = len(movieid_with_tag_genre1)
		movieid_with_tag_genre12 = movietags_genre12.where(movietags_genre12['tagid']==tag).movieid.unique()
		m1 = len(movieid_with_tag_genre12)

		tag_weight = log(((r1+ (m1/total_count))/(count_g1-r1 + 1))/(((m1-r1)+(m1/total_count))/(total_count - m1 - count_g1 + r1 + 1))) * abs(((r1 + (m1/total_count))/(count_g1 + 1))-(((m1-r1)+ (m1/total_count))/(total_count - count_g1 + 1)))
		tag_vector_genre1.append([tags_details.where(tags_details['tagId']==tag).dropna().iloc[0,1], tag_weight])

	
	tag_vector_genre1= sorted(tag_vector_genre1, key=itemgetter(1), reverse=True)
	for vector in tag_vector_genre1:
		print >> f, vector
		print vector

# find differentiating tag vector based on pdiff2 model
def pdiff2():
	tag_vector_genre1 = []
	tag_vector_genre2 = []

	movietags_genre1 = tags.where(tags['movieid'].isin(movieids_genre1)).dropna()
	movietags_genre2 = tags.where(tags['movieid'].isin(movieids_genre2)).dropna()
	movietags_genre12 = tags.where(tags['movieid'].isin(movieids_genre12)).dropna()
	distinct_tags_genre1 = movietags_genre1.tagid.unique()

	for tag in distinct_tags_genre1:
		movieid_without_tag_genre1 = movietags_genre1.where(movietags_genre1['tagid']!=tag).movieid.unique()
		r1 = len(movieid_without_tag_genre1)
		movieid_without_tag_genre12 = movietags_genre12.where(movietags_genre12['tagid']!=tag).movieid.unique()
		m1 = len(movieid_without_tag_genre12)



		tag_weight = log(((r1+ (m1/total_count))/(count_g1-r1 + 1))/(((m1-r1)+(m1/total_count))/(total_count - m1 - count_g1 + r1 + 1))) * abs(((r1 + (m1/total_count))/(count_g1 + 1))-(((m1-r1)+ (m1/total_count))/(total_count - count_g1 + 1)))
		tag_vector_genre1.append([tags_details.where(tags_details['tagId']==tag).dropna().iloc[0,1], tag_weight])

	tag_vector_genre1= sorted(tag_vector_genre2, key=itemgetter(1), reverse=True)

	for vector in tag_vector_genre1:
		print >> f, vector
		print vector



def main():
	
	f.write('Genre 1 is: '+ genre1+'\n')
	f.write('Genre 2 is: '+ genre2+'\n')
	f.write('Model is: '+ model+'\n')
	if(model == 'TF-IDF-DIFF'):
		tag_vector_genre1 = tf_idf(genre1)

	if(model == 'P-DIFF1'):
		pdiff1()
	if(model == 'P-DIFF2'):
		pdiff2()
	f.close()



	
if __name__ == '__main__':
	main()