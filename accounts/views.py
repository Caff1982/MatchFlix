from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, JsonResponse

from .models import Account
from .forms import UserCreationForm, RegistrationForm


class RegistrationView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)

        return reverse('login')

class ProfileView(UpdateView):
    model = Account
    fields = ['name', 'date_of_birth']
    template_name = 'accounts/profile.html'

    def get_success_url(self):
        return '/'

    def get_object(self):
        return self.request.user


def friend_search(request):
    q = request.GET.get('q')
    if q is not None:
        user_list = Account.objects.filter(name__icontains=q)
        return render(request, 'accounts/friend_search.html', {'user_list': user_list})
    else:
        return render(request, 'accounts/friend_search.html')

def profile_view(request, pk):
    account = Account.objects.filter(id=pk).first()
    context = {
        'account': account,
    }
    return render(request, 'accounts/profile_view.html', context)

def add_friend(request):
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        friend_id = request.POST.get('friend_id')
        friend_acc = Account.objects.get(id=friend_id)
        user.friends.add(friend_acc)
        user.save()
        return HttpResponse(status=200)
    else:
        print('add friend error')
        return HttpResponse(status=500)

def remove_friend(request):
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        friend_id = request.POST.get('friend_id')
        friend_acc = Account.objects.get(id=friend_id)
        user.friends.remove(friend_acc)
        user.save()
        return HttpResponse(status=200)
    else:
        print('remove friend error')
        return HttpResponse(status=500)