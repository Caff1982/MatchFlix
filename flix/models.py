from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Country(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Countries'


class Show(models.Model):
    """
    Data relates to netflix_data.csv

    ### TODO: Cast, country, listed_in should be one-to-many field ###

    show_id: The netflix id, also the url slug
    is_movie: TV shows are False, movies True
    title
    """
    show_id = models.CharField(max_length=10)
    is_movie = models.BooleanField(default=False)
    title = models.CharField(max_length=120)
    director = models.CharField(max_length=120)
    # cast, country, listed_int = TODO
    release_year = models.IntegerField()
    rating = models.CharField(max_length=50, null=True, blank=True)
    duration = models.CharField(max_length=20)
    description = models.CharField(max_length=250)
    image_url = models.CharField(max_length=50, default='default_image.jpg')

    category = models.ManyToManyField(Category)
    country = models.ManyToManyField(Country)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Shows'
        ordering = ['title']