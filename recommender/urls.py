from django.urls import path

from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('recommendations/<str:type>/', RecommenderListing.as_view(), name='recommender_view'),
    # path('recommender_listing/', RecommenderListing.as_view(), name='recommender_listing'),
    path('ajax/friends/', get_friends, name='get_friends'),
]
