from django import forms
from .models import Show, Category, Country
from django.db.models import Max, Min


# Get years
year_range = range(Show.objects.all().aggregate(Min('release_year'))['release_year__min'],
                   Show.objects.all().aggregate(Max('release_year'))['release_year__max'])
RELEASE_YEAR_RANGE = [(year, str(year)) for year in reversed(year_range)]
RELEASE_YEAR_RANGE.insert(0, (0, 'All'))

# Get Categories
categories = Category.objects.all().values_list('name', flat=True)
CATEGORY_CHOICES = [(c, c) for c in categories]
CATEGORY_CHOICES.insert(0, (None, 'All'))

# Get Countries
countries = Country.objects.all().values_list('name', flat=True)
COUNTRY_CHOICES = [(c, c) for c in countries]
COUNTRY_CHOICES.insert(0, (None, 'All'))
   
class SearchForm(forms.Form):
    title = forms.CharField(label='Title search', max_length=100, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.CharField(required=False,
                               widget=forms.Select(choices=CATEGORY_CHOICES,
                                                   attrs={'class': 'form-control'}))

    country = forms.CharField(label='Country search',
                              required=False,
                              widget=forms.Select(choices=COUNTRY_CHOICES,
                                                  attrs={'class': 'form-control'}))
    year = forms.IntegerField(required=False,
                              widget=forms.Select(choices=RELEASE_YEAR_RANGE,
                                                  attrs={'class': 'form-control'}))

    # def __init__(self, data, **kwargs):
    #     initial = kwargs.get('initial', {})
    #     print('initial: ', initial)
    #     data = (*initial, *data)
    #     super().__init__(data, **kwargs)