from django.urls import path

from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('random/', random_browse, name='random_browse'),
    # Detail view for movie/tv show
    path('detail/<pk>/', detail_view, name='detail_view'),
    path('profile/<pk>/', profile_view, name='profile_view'),
    path('friends-search/', friend_search, name='friend_search'),
    path('show-search/', show_search, name='show_search'),
    path('recommendations/', recommender_view, name='recommender_view')
]
