from django.shortcuts import render, get_object_or_404
from django.db.models import Max

import random

from .models import Show
from accounts.models import Account


def get_random_show():
    """
    Randomly selects a row from Show database table
    """
    max_id = Show.objects.all().aggregate(max_id=Max('id'))['max_id']
    pk = random.randint(1, max_id)
    return Show.objects.get(pk=pk)

def random_browse(request):
    if request.method == 'POST':
        user = request.user

        last_show = Show.objects.filter(id=request.POST['show_id']).first()
        print(last_show)
        user.likes.add(last_show)
    show = get_random_show()
    context = {
        'show': show
    }
    return render(request, 'flix/random_browse.html', context)
    
