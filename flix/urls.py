from django.urls import path

from .views import random_browse

urlpatterns = [
    path('random/', random_browse, name='random_browse')
]