from data import *
import sys
import time
import math
import re
import pickle
import numpy as np
from sklearn.cluster import KMeans
import os.path
from sklearn.metrics import mean_squared_error

user = []
item = []
rating = []

d = Dataset()
d.load_items("allmovies.txt", item)
d.load_users("users.txt", user)
d.load_ratings("ratings.txt", rating)


n_users = len(user)
n_items = len(item)

# The utility matrix stores the rating for each user-item pair in the
# matrix form.
utility = np.zeros((n_users, n_items))
for r in rating:
    utility[r.user_id - 1][r.item_id - 1] = r.rating

# print(utility)
# A matrix of users vs movies flled with respective rating as cells

# test = np.zeros((n_users, n_items))
# for r in rating_test:
#     test[r.user_id - 1][r.item_id - 1] = r.rating

# # Perform clustering on items
movie_genre = []
for movie in item:
    movie_genre.append([movie.action, movie.adventure, movie.animation, movie.comedy,
                        movie.crime, movie.documentary, movie.drama, movie.family,
                        movie.fantasy, movie.history, movie.horror, movie.musical, 
                        movie.mystery, movie.romance, movie.sci_fi, movie.tv_movie, 
                        movie.thriller, movie.war, movie.western])

movie_genre = np.array(movie_genre)
cluster = KMeans(n_clusters=19)
cluster.fit_predict(movie_genre)

# size=n_items ____ array([ 1,  4,  8, ..., 14, 11,  2], dtype=int32)
# assigned each movie to a cluster

utility_clustered = []
for i in range(0, n_users):
    average = np.zeros(19)
    # average = [[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0]]
    tmp = []
    for m in range(0, 19):
        tmp.append([])
        # tmp = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for j in range(0, n_items):
        if utility[i][j] != 0:
            tmp[cluster.labels_[j] - 1].append(utility[i][j])
        # tmp = [[rate of movies belonging to cluster 0], [rate of movies belonging to cluster 1], ... [rate of movies belonging to cluster 18]]
    for m in range(0, 19):
        if len(tmp[m]) != 0:
            average[m] = np.mean(tmp[m])
        else:
            average[m] = 0
    utility_clustered.append(average)

utility_clustered = np.array(utility_clustered)

# utility_clustered is the array of average ratings given to each cluster by the user

# array([[ 0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
#          0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
#          0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
#          0.        ,  0.        ,  0.        ,  0.        ],
# this is the useless admin user

#        [ 0.        ,  7.25      ,  7.        ,  2.        ,  0.        ,
#          4.        ,  0.        ,  1.        ,  0.        ,  8.        ,
#          8.        ,  0.        ,  0.        ,  6.        ,  6.        ,
#          0.        ,  0.        ,  2.        ,  0.        ],
# this user gave higher rating to horror, thriller, comedy etc and lower to romance,musical etc

#        [ 0.        ,  7.85714286,  0.        ,  0.        ,  8.        ,
#          0.        ,  9.        ,  3.2       ,  9.5       ,  8.        ,
#          0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
#          0.        ,  0.        ,  3.        ,  8.        ],
# this user also gave higher rating to horror, thriller, comedy etc and lower to romance,musical etc

#        [ 0.        ,  3.        ,  0.        ,  8.        ,  9.        ,
#          0.        ,  0.        ,  8.        ,  0.        ,  0.        ,
#          0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
#          0.        ,  0.        ,  9.        ,  0.        ]])
# this user gave higher rating to romance and lower to horror



# Find the average rating for each user and stores it in the user's object

for i in range(0, n_users):
    x = utility_clustered[i]
    num = sum(a for a in x if a > 0)
    den = sum(a > 0 for a in x)
    if den == 0:
    	user[i].avg_r = 0
    else:
	    user[i].avg_r = num/den 

# user1 avg_rating : 5.125
# user2 avg_rating : 7.06964285714
# user3 avg_rating : 7.4

# Find the Pearson Correlation Similarity Measure between two users
def pcs(x, y):
    num = 0
    den1 = 0
    den2 = 0
    A = utility_clustered[x - 1]
    B = utility_clustered[y - 1]
    num = sum((a - user[x - 1].avg_r) * (b - user[y - 1].avg_r) for a, b in zip(A, B) if a > 0 and b > 0)
    den1 = sum((a - user[x - 1].avg_r) ** 2 for a in A if a > 0)
    den2 = sum((b - user[y - 1].avg_r) ** 2 for b in B if b > 0)
    den = (den1 ** 0.5) * (den2 ** 0.5)
    if den == 0:
        return 0
    else:
        return num / den

# r =       SUM[(x-x_avg).(y-y_avg)]
#	  --------------------------------------- 
#		_______________      __________________
#      /	   			    /
#     / SUM[(x-x_avg)^2] . / SUM[(y-y_avg)^2]
#
#

pcs_matrix = np.zeros((n_users, n_users))
for i in range(0, n_users):
    for j in range(0, n_users):
        if i!=j:
            pcs_matrix[i][j] = pcs(i + 1, j + 1)
 
# finds the pearsons coefficient between all user pairs

# array([[ 0.        ,  0.        ,  0.        ,  0.        ],
#        [ 0.        ,  0.        ,  0.62014004, -0.46598257],
#        [ 0.        ,  0.62014004,  0.        , -0.32321283],
#        [ 0.        , -0.46598257, -0.32321283,  0.        ]])
#
# high correlation between user 1 and user 2 (+ve)
# low correlation between user 1 and user 3 (-ve)
# low correlation between user 2 and user 3 (-ve)
# makes sense

# Guesses the ratings that user with id, user_id, might give to item with id, i_id.
# We will consider the top_n similar users to do this.
def norm():
    normalize = np.zeros((n_users, 19))
    for i in range(0, n_users):
        for j in range(0, 19):
            if utility_clustered[i][j] != 0:
                normalize[i][j] = utility_clustered[i][j] - user[i].avg_r
            else:
                normalize[i][j] = float('Inf')
    return normalize

def guess(user_id, i_id, top_n):
    similarity = []
    for i in range(0, n_users):
        if i+1 != user_id:
            similarity.append(pcs_matrix[user_id-1][i])
            # a list of pearsons correlation of that user to other users

    temp = norm()
    temp = np.delete(temp, user_id-1, 0)
	# the whole normalized matrix without the user row whose id = user_id-1
    	# temp = [
	# 	[inf,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf],
	# 	[inf,0.7875,inf,inf,0.93035714,inf,1.93035714,-3.86964286,2.43035714,0.93035714,inf,inf,inf,inf,inf,inf,inf,-4.06964286,0.93035714],
	# 	[inf,-4.4,inf,0.6,1.6,inf,inf,0.6,inf,inf,inf,inf,inf,inf,inf,inf,inf,1.6,inf]
	# ]
	# similarity = [0.0, 0.62014003913348725, -0.46598256662291143]
    combine = zip(similarity,temp)
    sorted_by_similarity = sorted(combine, key=lambda pair:pair[0], reverse=True)
    top = [x for (y,x) in sorted_by_similarity]
    # top =  [ [inf, 0.7875, inf, inf, 0.93035714, inf, 1.93035714, -3.86964286, 2.43035714, 0.93035714, inf, inf, inf, inf, inf, inf, inf, -4.06964286, 0.93035714], 
	# 		 [inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf], 
	#		 [inf, -4.4, inf, 0.6, 1.6, inf, inf, 0.6, inf, inf, inf, inf, inf, inf, inf, inf, inf, 1.6, inf]
	# 		 ]
	# in the ith cluster, what is the average rate
    s = 0
    c = 0
    for i in range(0, top_n):
        if top[i][i_id-1] != float('Inf'):
            s += top[i][i_id-1]
            c += 1
    if c ==0:
        g = user[user_id-1].avg_r
    else:
        g = s/float(c) + user[user_id-1].avg_r
    return g
# utility_matrix = 
# [ 
# 	[	 0.          0.          0.          0.          0.          0.          0.
#   	 0.          0.          0.          0.          0.          0.          0.
#   	 0.          0.          0.          0.          0.        
#	]
#  	[	0.          7.25        7.          2.          0.          4.          0.
#    	1.          0.          8.          8.          0.          0.          6.
#    	6.          0.          0.          2.          0.        ]
#   [ 	0.          7.85714286  0.          0.          8.          0.          9.
#    	3.2         9.5         8.          0.          0.          0.          0.
#    	0.          0.          0.          3.          8.        
#   ]
#   [ 	0.          3.          0.          8.          9.          0.          0.
#    	8.          0.          0.          0.          0.          0.          0.
#    	0.          0.          0.          9.          0.        
#   ]
# ]

utility_copy = np.copy(utility_clustered)
for i in range(0, n_users):
    for j in range(0, 19):
        if utility_copy[i][j] == 0:
            t = guess(i+1, j+1, 1)
            if t < 1:
                utility_copy[i][j] = 1
            elif t > 10:
                utility_copy[i][j] = 10
            else:
                utility_copy[i][j] = t 

# utility_copy = 
# [
#	 	 [ 0.        ,  2.125     ,  1.875     , -3.125     ,  1.26517857,
#         -1.125     ,  1.93035714, -4.125     ,  2.43035714,  2.875     ,
#          2.875     ,  0.        ,  0.        ,  0.875     ,  0.875     ,
#          0.        ,  0.        , -3.125     ,  0.93035714],

#        [ 5.125     ,  7.25      ,  7.        ,  2.        ,  6.05535714,
#          4.        ,  7.05535714,  1.        ,  7.55535714,  8.        ,
#          8.        ,  5.125     ,  5.125     ,  6.        ,  6.        ,
#          5.125     ,  5.125     ,  2.        ,  6.05535714],

#        [ 7.06964286,  7.85714286,  8.94464286,  3.94464286,  8.        ,
#          5.94464286,  9.        ,  3.2       ,  9.5       ,  8.        ,
#          9.94464286,  7.06964286,  7.06964286,  7.94464286,  7.94464286,
#          7.06964286,  7.06964286,  3.        ,  8.        ],

#        [ 7.4       ,  3.        ,  7.4       ,  8.        ,  9.        ,
#          7.4       ,  7.4       ,  8.        ,  7.4       ,  7.4       ,
#          7.4       ,  7.4       ,  7.4       ,  7.4       ,  7.4       ,
#          7.4       ,  7.4       ,  9.        ,  7.4       ]]
# print(utility_copy)
pickle.dump( utility_copy, open(os.path.expanduser(os.path.join('~/Desktop/Movie/main/utility_matrix.pkl')), "wb"))
