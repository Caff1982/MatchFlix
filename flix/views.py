from django.shortcuts import render
from django.db.models import Max

import random

from .models import Show


def get_random_show():
    """
    Randomly selects a row from Show database table
    """
    max_id = Show.objects.all().aggregate(max_id=Max('id'))['max_id']
    pk = random.randint(1, max_id)
    return Show.objects.get(pk=pk)

def random_browse(request):
    if request.method == 'POST':
        print('Request.user: ', request.user)
        print('request POST: ', request.POST)
    show = get_random_show()
    context = {
        'show': show
    }
    return render(request, 'flix/random_browse.html', context)
    
