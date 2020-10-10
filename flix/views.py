from django.shortcuts import render, get_object_or_404
from django.db.models import Max, Min
from django.views.generic import ListView

import random
import os

from .models import Show
from accounts.models import Account


def friend_search(request):
    q = request.GET['q']
    user_list = Account.objects.filter(name__icontains=q)
    return render(request, 'flix/friend_search.html', {'user_list': user_list})

def show_search(request):
    q = request.GET['q']
    show_list = Show.objects.filter(title__icontains=q)
    print('Show list: ', show_list)
    return render(request, 'flix/show_search.html', {'show_list': show_list})

def get_random_show():
    """
    Helper function. Returns a randomly selected
    row from Show database table
    """
    max_id = Show.objects.all().aggregate(max_id=Max('id'))['max_id']
    min_id = Show.objects.all().aggregate(min_id=Min('id'))['min_id']
    pk = random.randint(min_id, max_id)
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
        user.likes.add(last_show)

    show = get_random_show()
    print('Show id: ', show.id)
    # Check if image for the show exists
    image_path = f'media/images/{show.show_id}.jpg'
    if os.path.exists(image_path):
        image_exists = True
    else:
        image_exists = False
    context = {
        'show': show,
        'image_exists': image_exists
    }
    return render(request, 'flix/random_browse.html', context)

def detail_view(request, pk):
    """
    Detail view for shows/movies
    """
    show = Show.objects.filter(id=pk).first()
    if request.method == 'POST':
        user = request.user
        user.likes.add(show)
    # Check if image for the show exists
    image_path = f'media/images/{show.show_id}.jpg'
    if os.path.exists(image_path):
        image_exists = True
    else:
        image_exists = False
    context = {
        'show': show,
        'image_exists': image_exists
    }

    return render(request, 'flix/detail_view.html', context)

def profile_view(request, pk):
    account = Account.objects.filter(id=pk).first()
    if request.method == 'POST':
        user = request.user
        user.friends.add(account)
    context = {
        'account': account,
    }
    return render(request, 'flix/profile_view.html', context)

