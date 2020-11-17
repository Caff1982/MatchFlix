# MatchFlix

**This is still a work in progess.**

MatchFlix is a recommender site for Netflix. It allows users to add their friends and get recommendations based on two profiles. I made this to explore recommendation algorithms, in-particular for combining two profiles. 

The recommender system uses a content-based algorithm to match user-profiles with item-profiles. The user-profile is the mean of all the users likes represented as a vector. The similarities are then calculated using cosine-theta.

Going forward, I would like to implement a hybrid system combining content-based with collaborative-filtering. For now however I am happy that content-based is the correct approach due to the low number of users and the 'cold-start problem'.

### Usage

To get the images run 'utils/image_scraper.py'. To populate the database run ' python manage.py populate_db data.csv'. The project can then be run using 'python manage.py runserver'.

### Acknowledgements

I found [this](https://dev.to/joshwizzy/customizing-django-authentication-using-abstractbaseuser-llg) tutorial very helpful for authentication.

I used The Movie Database (TMDb) API to get images.

The Netflix data is from Kaggle and can be found [here](https://www.kaggle.com/shivamb/netflix-shows).