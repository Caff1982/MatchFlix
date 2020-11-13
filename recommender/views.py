from django.shortcuts import render
from django.db.models import Max, Min
from rest_framework.generics import ListAPIView
from django.http import JsonResponse

import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from accounts.models import Account
from shows.models import Show
from .pagination import StandardResultsSetPagination
from .serializers import RecommenderSerealizers

def dashboard(request):
    return render(request, 'recommender/dashboard.html')

def get_random_show():
    """
    Helper function. Returns a randomly selected
    row from Show database table
    """
    max_id = Show.objects.all().aggregate(max_id=Max('id'))['max_id']
    min_id = Show.objects.all().aggregate(min_id=Min('id'))['min_id']
    pk = np.random.randint(min_id, max_id)
    return Show.objects.get(pk=pk)

def recommender_view(request):
    """
    Returns the recommendations template
    """
    return render(request, 'recommender/recommender_view.html')

class RecommenderListing(ListAPIView):
    model = Show
    # set the pagination and serializer class
    pagination_class = StandardResultsSetPagination
    serializer_class = RecommenderSerealizers

    def get_queryset(self):
        queryset = Show.objects.all()
        # Select type of recommendations
        rec_type = self.request.query_params.get('type', None)

        if rec_type == 'self':
            print('Self recs')
            queryset = self.get_self_recs()
        elif rec_type == 'friend':
            friend = self.request.query_params.get('friend', None)
            if friend:
                query_set = self.get_friend_recs(friend)
        elif rec_type == 'random':
            queryset = Show.objects.order_by('?')

        return queryset

    def get_self_recs(self):
        """
        Gets recommendations for one profile
        """
        likes = self.request.user.likes.all()
        if len(likes) == 0:
            # User must have likes to get recommendations
            pass
        
        show_titles = [show.title for show in likes]
        df = pd.read_csv('item_profiles.csv')
        # User Profile is the mean of all user likes
        user_profile = df[df['title'].isin(show_titles)].mean().values.reshape(1, -1)
        # recs are the recommendations, ie labels/targets
        recs = pd.DataFrame(data=df['title'], columns=['title'])
        # df.drop(['title'], axis=1, inplace=True)
        # Add cos theta as column to labels
        recs['similarity'] = cosine_similarity(df.drop(['title'], axis=1), user_profile)
        recs.sort_values(by=['similarity'], ascending=False, inplace=True)
        # Use recs DataFrame to get list of Show objects
        queryset = [Show.objects.filter(title=title)[0] for title in recs['title'].values[:100]]
        print('Len queryset: ', len(queryset))
        return queryset

    def get_friend_recs(self, friend):
        """
        Gets recommendations for two user profiles
        """
        user_likes = self.request.user.likes.all()
        friend_likes = Account.objects.get(name=friend).likes.all()
        if (len(user_likes) | len(friend_likes)) == 0:
            # Must have likes to get recommendations
            pass
        print('Friend: ', friend)
        print('Len friend likes: ', len(friend_likes))
        # Add the two querysets together
        likes = user_likes | friend_likes
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
        return rec_shows


def get_friends(request):
    """
    Returns all the user's friends, to be used in dropdown menu
    """
    if request.method == 'GET' and request.is_ajax():
        friends_qs = request.user.friends.all()
        friends = [friend.name for friend in friends_qs]
        data = {
            'friends': friends,
        }
        return JsonResponse(data, status=200)

def recommender_friends(request):
    user = request.user
    user_likes = user.likes.all()
    user_friends = user.friends.all()

    friend_id = request.GET.get('friend')
    if friend_id:
        friend = Account.objects.filter(id=friend_id).first()
        friend_likes = friend.likes.all()
        # Add the two querysets together
        likes = user_likes | friend_likes

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
    else:
        rec_shows = []

    context = {
        'user_friends': user_friends,
        'queryset': rec_shows
    }
    return render(request, 'recommender/recommender_friends.html', context)



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
    return render(request, 'recommender/random_browse.html', context)

def recommender_view(request):
    user = request.user
    likes = user.likes.all()
    if len(likes) == 0:
        ### TODO: User myst have likes to get recommendations ###
        pass
    else:
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
    return render(request, 'recommender/recommender_view.html', context)






