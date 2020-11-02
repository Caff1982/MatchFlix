import django_filters

from .models import Show


class ShowFilter(django_filters.FilterSet):
    class Meta:
        model = Show
        fields = ['title', 'category', 'country']