from __future__ import division
import pandas as pd
from datetime import datetime
from math import log
from operator import itemgetter
import sys

current_time = datetime.now()
tags = pd.read_csv('../phase1_dataset/mltags.csv')
movie_ratings = pd.read_csv('../phase1_dataset/mlratings.csv')
tags_details = pd.read_csv('../phase1_dataset/genome-tags.csv')
users = pd.read_csv('../phase1_dataset/mlusers.csv')


tag_vector = []
for i,row in tags.iterrows():
	tags.set_value(i,'timestamp', 1/(current_time-datetime.strptime(row['timestamp'],'%Y-%m-%d %H:%M:%S')).total_seconds())

# Get input arguments
user_id = int(sys.argv[1])#30167
model = sys.argv[2]#'tf'

f = open('../Output/output_user_'+model+'.txt','w')
f.write('User id is: '+ str(user_id)+'\n')
f.write('Model is: '+ model+'\n')

total_users = users.count()



movieids_dfs = []
movieids_dfs.append(movie_ratings.where(movie_ratings['userid']==user_id).dropna().loc[:,'movieid'])
movieids_dfs.append(tags.where(tags['userid']==user_id).dropna().loc[:,'movieid'])
movieids = pd.concat(movieids_dfs)
movietags = tags.where(tags['movieid'].isin(movieids)).dropna()
distinct_tags = movietags.tagid.unique()
total_tag_weight = movietags['timestamp'].sum()

# Find the tag weght for each distinct tag
for tag in distinct_tags:
	movieid_with_tag = movietags.where(movietags['tagid']==tag).movieid.unique()
	
	
	tag_weight = movietags.loc[movietags['tagid']==tag]['timestamp'].sum()
	if(model == 'tfidf'):
		users_dfs = []
		for movie in movieid_with_tag:
			users_dfs.append(movie_ratings.where(movie_ratings['movieid']==movie).dropna())
			users_dfs.append(tags.where(tags['movieid']==movie).dropna())
		users_df = pd.concat(users_dfs)
		users = len(users_df.userid.unique())
		tag_vector.append([tags_details.where(tags_details['tagId']==tag).dropna().iloc[0,1], (tag_weight/total_tag_weight)*log(total_users/users)])
	if(model == 'tf'):
		tag_vector.append([tags_details.where(tags_details['tagId']==tag).dropna().iloc[0,1], (tag_weight/total_tag_weight)])
	tag_vector= sorted(tag_vector, key=itemgetter(1), reverse=True)


for vector in tag_vector:
	print >> f, vector
	print vector
f.close()
