from django.core.management.base import BaseCommand, CommandError
from flix.models import Show, Country, Category

import csv


class Command(BaseCommand):
    help = 'Updates database from csv file'

    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
        """
        Iterates through rows in csv and creates Show objects.
        """
        with open(options['filepath'], 'r') as f:
            reader = csv.DictReader(f)
            for line in reader:
                if line['type'] == 'Movie':
                    is_movie = True
                else:
                    is_movie = False

                show, _ = Show.objects.get_or_create(
                    show_id=line['show_id'], is_movie=is_movie,
                    title=line['title'], director=line['director'],
                    release_year=line['release_year'], rating=line['rating'],
                    duration=line['duration'], description=line['description'])

                # Add category & country as many_to_many field
                categories = line['listed_in'].split(',')
                for category in categories:
                    cat_obj, _ = Category.objects.get_or_create(name=category)
                    show.category.add(cat_obj)

                countries = line['country'].split(',')
                for country in countries:
                    country_obj, _ = Country.objects.get_or_create(name=country)
                    show.country.add(country_obj)

      