from django.shortcuts import render, get_object_or_404
from django.db.models import Max, Min
from django.views.generic import ListView

import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from .models import Show, Category, Country
from accounts.models import Account


def friend_search(request):
    q = request.GET.get('q')
    if q is not None:
        user_list = Account.objects.filter(name__icontains=q)
        return render(request, 'flix/friend_search.html', {'user_list': user_list})
    else:
        return render(request, 'flix/friend_search.html')

def show_search(request):
    queryset = Show.objects.all()
    name_query = request.GET.get('name')
    director_query = request.GET.get('director')
    year_query = request.GET.get('year')
    is_movie_query = request.GET.get('is_movie')
    category_query = request.GET.get('category')
    country_query = request.GET.get('country')

    if name_query:
        queryset = queryset.filter(title__icontains=name_query)
    if director_query:
        queryset = queryset.filter(director__icontains=director_query)
    if year_query:
        queryset = queryset.filter(release_year=year_query)
    if is_movie_query:
        if is_movie_query == 'movies':
            queryset = queryset.filter(is_movie=True)
        elif is_movie_query == 'tv':
            queryset = queryset.filter(is_movie=False)
    if category_query:
        if category_query != 'all':
            queryset = queryset.filter(category__name=category_query)
    if country_query:
        print('country_query: ', country_query)
        if country_query != 'all':
            queryset = queryset.filter(country__name=country_query)

    categories = Category.objects.all()
    countries = Country.objects.all()
    context = {
        'queryset': queryset,
        'categories': categories,
        'countries': countries
    }
    return render(request, 'flix/show_search.html', context)


def get_random_show():
    """
    Helper function. Returns a randomly selected
    row from Show database table
    """
    max_id = Show.objects.all().aggregate(max_id=Max('id'))['max_id']
    min_id = Show.objects.all().aggregate(min_id=Min('id'))['min_id']
    pk = np.random.randint(min_id, max_id)
    return Show.objects.get(pk=pk)

def dashboard(request):
    return render(request, 'flix/dashboard.html')

def random_browse(request):
    """
    Displays a random show which the user can like
    """
    if request.method == 'POST':
        user = request.user
        last_show = Show.objects.filter(id=request.POST['show_id']).first()
        if last_show in user.likes.all():
            user.likes.remove(last_show)
        else:
            user.likes.add(last_show)

    show = get_random_show()
    context = {
        'show': show,
    }
    return render(request, 'flix/random_browse.html', context)

def detail_view(request, pk):
    """
    Detail view for shows/movies
    """
    show = Show.objects.filter(id=pk).first()
    if request.method == 'POST':
        user = request.user
        if show in user.likes.all():
            user.likes.remove(show)
        else:
            user.likes.add(show)

    context = {
        'show': show,
    }
    return render(request, 'flix/detail_view.html', context)

def profile_view(request, pk):
    account = Account.objects.filter(id=pk).first()
    if request.method == 'POST':
        user = request.user
        if account in user.friends.all():
            user.friends.remove(account)
        else:
            user.friends.add(account)
    context = {
        'account': account,
    }
    return render(request, 'flix/profile_view.html', context)

def recommender_view(request):
    user = request.user
    likes = user.likes.all()
    df = pd.read_csv('item_profiles.csv')
    show_titles = [show.title for show in likes] 
    # User Profile is the mean of all user likes
    user_profile = df[df['title'].isin(show_titles)].mean().values.reshape(1, -1)
    # Keep titles for recommendations, drop from df
    recs = pd.DataFrame(data=df['title'], columns=['title'])
    df.drop(['title'], axis=1, inplace=True)
    # Add cos theta as column to labels
    recs['similarity'] = cosine_similarity(df, user_profile)
    recs.sort_values(by=['similarity'], ascending=False, inplace=True)
    # Use recs DataFrame to get list of Show objects
    rec_shows = [Show.objects.filter(title=title)[0] for title in recs['title'].values[:25]]

    context = {
        'queryset': rec_shows
    }
    return render(request, 'flix/recommender_view.html', context)


    

