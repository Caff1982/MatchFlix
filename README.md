Inspired by tutorial from:
https://dev.to/joshwizzy/customizing-django-authentication-using-abstractbaseuser-llg

tmdb api used for images, give credit
tmdbv3api library used to get images
We have 5484 images out of 6234, ~88%


To get images run image_scraper.py. This must be done before populating the database.

To populate database run manage.py update_db filename.csv. File added as a command in flix/management/commands.