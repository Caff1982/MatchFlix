from django.contrib import admin

from .models import Show, Category, Country


# class ShowAdmin(admin.ModelAdmin):
#     list_display = ('show_id', 'is_movie', 'title', 'director',
#                     'release_year', 'rating', 'duration', 'description')
#     list_filter = ('is_movie',)

admin.site.register(Show)
admin.site.register(Category)
admin.site.register(Country)
