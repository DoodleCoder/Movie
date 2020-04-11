# Movie
A Django-powered web platform that predicts the ratings of upcoming movies and recommends movies to users. **[The Movie Database (TMDB)](https://www.themoviedb.org/?language=en-US)** used to collect movie data.  

## Prerequisites
```
pip install -r requirements.txt
```

## Running 
```
python manage.py runserver
```

## Working
### Movie Rating Prediction 
Uses features such as movie director, writer, acting team, genre, comments, release date, budget, tweets, prequel/sequel data to generate a rating for a given movie.
Generated results had an accuracy of 81% as tested against the accumulated dataset.

### Movie Recommender
A hybrid recommending engine developed using K-means algorithm to cluster movies into 19 groups based on genre and Nearest Neighbour + Correlation Matrix Factorization algorithms for Collaborative Filtering. 
This generated recommendations for similar users and found similar movies.

## Technologies Used
* HTML
* CSS
* Javascript
* Django
* Twitter API
* NLTK
* Scikit
* Pickle
