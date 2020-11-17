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
    """
    Returns the dashboard/home template
    """
    return render(request, 'recommender/dashboard.html')

def recommender_view(request):
    """
    Returns the recommendations template
    """
    return render(request, 'recommender/recommender_view.html')

class RecommenderListing(ListAPIView):
    """
    Class-based view for recommendations.
    """
    model = Show
    # set the pagination and serializer class
    pagination_class = StandardResultsSetPagination
    serializer_class = RecommenderSerealizers

    def get_queryset(self):
        queryset = Show.objects.all()
        # Select type of recommendations
        rec_type = self.request.query_params.get('type', None)

        if rec_type == 'self': # Recommendations for one profile
            queryset = self.get_self_recs()
        elif rec_type == 'friend': # Recommendations for two profiles
            friend = self.request.query_params.get('friend', None)
            if friend:
                queryset = self.get_friend_recs(friend)
        elif rec_type == 'random': # Returns random recommendations
            queryset = Show.objects.order_by('?')
        return queryset

    def get_self_recs(self):
        """
        Gets recommendations for one profile
        """
        likes = self.request.user.likes.all()
        if len(likes) == 0:
            # User must have likes to get recommendations
            return []
        
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
        return queryset

    def get_friend_recs(self, friend):
        """
        Gets recommendations for two user profiles
        """
        user_likes = self.request.user.likes.all()
        friend_likes = Account.objects.get(name=friend).likes.all()
        if (len(user_likes) | len(friend_likes)) == 0:
            # Must have likes to get recommendations
            return []
        # Combine the two querysets together
        likes = user_likes | friend_likes
        df = pd.read_csv('item_profiles.csv')
        show_titles = [show.title for show in likes] 
        # User Profile is the mean of all user likes
        user_profile = df[df['title'].isin(show_titles)].mean().values.reshape(1, -1)
        # recs will be recommendations, keep title for labelling
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
