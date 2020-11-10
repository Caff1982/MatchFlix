from django.urls import path

from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('random/', random_browse, name='random_browse'),
    path('recommendations/', recommender_view, name='recommender_view'),
    path('recommendations-friends/', recommender_friends, name='recommender_friends'),
]
