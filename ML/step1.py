from data import *
import sys
import time
import math
import re
import pickle
import numpy as np
from sklearn.cluster import KMeans
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

for i in range(1, n_users):
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
    temp = norm()
    temp = np.delete(temp, user_id-1, 0)
    top = [x for (y,x) in sorted(zip(similarity,temp), key=lambda pair: pair[0], reverse=True)]
    s = 0
    c = 0
    for i in range(0, top_n):
        if top[i][i_id-1] != float('Inf'):
            s += top[i][i_id-1]
            c += 1
    g = user[user_id-1].avg_r if c == 0 else s/float(c) + user[user_id-1].avg_r
    if g < 1.0:
        return 1.0
    elif g > 5.0:
        return 5.0
    else:
        return g

# utility_copy = np.copy(utility_clustered)
# for i in range(0, n_users):
#     for j in range(0, 19):
#         if utility_copy[i][j] == 0:
#             sys.stdout.write("\rGuessing [User:Rating] = [%d:%d]" % (i, j))
#             sys.stdout.flush()
#             time.sleep(0.00005)
#             utility_copy[i][j] = guess(i+1, j+1, 150)
# print "\rGuessing [User:Rating] = [%d:%d]" % (i, j)

# print utility_copy

# pickle.dump( utility_copy, open("utility_matrix.pkl", "wb"))

# # Predict ratings for u.test and find the mean squared error
# y_true = []
# y_pred = []
# f = open('test.txt', 'w')
# for i in range(0, n_users):
#     for j in range(0, n_items):
#         if test[i][j] > 0:
#             f.write("%d, %d, %.4f\n" % (i+1, j+1, utility_copy[i][cluster.labels_[j]-1]))
#             y_true.append(test[i][j])
#             y_pred.append(utility_copy[i][cluster.labels_[j]-1])
# f.close()

# print "Mean Squared Error: %f" % mean_squared_error(y_true, y_pred)
