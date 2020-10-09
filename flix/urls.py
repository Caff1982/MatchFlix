from django.urls import path

from .views import random_browse, detail_view, profile_view, dashboard


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('random/', random_browse, name='random_browse'),
    # Detail view for movie/tv show
    path('detail/<pk>/', detail_view, name='detail_view'),
    path('profile/<pk>/', profile_view, name='profile_view')
]