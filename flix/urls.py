from django.urls import path

from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('random/', random_browse, name='random_browse'),
    # Detail view for movie/tv show
    path('detail/<pk>/', detail_view, name='detail_view'),
    path('profile/<pk>/', profile_view, name='profile_view'),
    path('friends-search/', friend_search, name='friend_search'),
    path('recommendations/', recommender_view, name='recommender_view'),
    path('recommendations-friends/', recommender_friends, name='recommender_friends'),
    path('show-search/', show_search, name='show_search'),
    path('show-listing/', ShowListing.as_view(), name='show_listing'),
    path('ajax/categories/', get_categories, name='get_categories'),
    path('ajax/countries/', get_countries, name='get_countries'),
    path('ajax/years/', get_years, name='get_years'),
]
