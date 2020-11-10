from django.urls import path

from .views import *

urlpatterns = [
    path('search/', show_search, name='show_search'),
    path('detail/<pk>/', detail_view, name='detail_view'),
    path('show-listing/', ShowListing.as_view(), name='show_listing'),
    path('ajax/categories/', get_categories, name='get_categories'),
    path('ajax/countries/', get_countries, name='get_countries'),
    path('ajax/years/', get_years, name='get_years'),
]
