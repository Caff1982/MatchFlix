from django.urls import path

from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('random/', random_browse, name='random_browse'),
    path('recommendations/', recommender_view, name='recommender_view'),
    path('recommendations-friends/', recommender_friends, name='recommender_friends'),
    path('recommender_listing/', RecommenderListing.as_view(), name='recommender_listing'),
    path('ajax/friends/', get_friends, name='get_friends'),
]
