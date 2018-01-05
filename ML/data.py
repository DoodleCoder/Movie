import re

class User:
    def __init__(self, id, username, first_name):
        self.id = int(id)
        self.username = username
        self.first_name = first_name
        self.avg_r = 0.0

class Item:
    def __init__(self, id, movie_id, title, action, adventure, animation, comedy, crime, documentary, \
    drama, family, fantasy, history, horror, musical, mystery ,romance, sci_fi, tv_movie, \
    thriller, war, western):
        self.id = int(id)
        self.movie_id = int(movie_id)
        self.title = title
        self.action = int(action)
        self.adventure = int(adventure)
        self.animation = int(animation)
        self.comedy = int(comedy)
        self.crime = int(crime)
        self.documentary = int(documentary)
        self.drama = int(drama)
        self.family = int(family)
        self.fantasy = int(fantasy)
        self.history = int(history)
        self.horror = int(horror)
        self.musical = int(musical)
        self.mystery = int(mystery)
        self.romance = int(romance)
        self.sci_fi = int(sci_fi)
        self.tv_movie = int(tv_movie)
        self.thriller = int(thriller)
        self.war = int(war)
        self.western = int(western)

class Rating:
    def __init__(self, user_id, id, item_id, rating):
        self.user_id = int(user_id)
        self.item_id = int(id)
        self.id = int(item_id)
        self.rating = int(rating)

class Dataset:
    def load_users(self, file, u):
        f = open(file, "r")
        text = f.read()
        entries = re.split("\n+", text)
        for entry in entries:
            e = entry.split('|', 3)
            if len(e) == 3:
                u.append(User(e[0], e[1], e[2]))
        f.close()

    def load_items(self, file, i):
        f = open(file, "r")
        text = f.read()
        entries = re.split("\n+", text)
        for entry in entries:
            e = entry.split('|', 23)
            if len(e) == 23:
                i.append(Item(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8], e[9], e[10], \
                e[11], e[12], e[13], e[14], e[15], e[16], e[17], e[18], e[19], e[20], e[21]))
        f.close()

    def load_ratings(self, file, r):
        f = open(file, "r")
        text = f.read()
        entries = re.split("\n+", text)
        for entry in entries:
            e = entry.split('|', 4)
            if len(e) == 4:
                r.append(Rating(e[0], e[1], e[2], e[3]))
        f.close()
