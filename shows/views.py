from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import ListAPIView

from .models import Show, Category, Country
from .serealizers import ShowSerealizers
from .pagination import StandardResultsSetPagination


def show_search(request):
    """
    Returns the show search template
    """
    return render(request, 'shows/show_search.html', {})


class ShowListing(ListAPIView):
    """
    Uses DRF ListAPIView to provide an API for show search
    """
    model = Show
    # set the pagination and serializer class
    pagination_class = StandardResultsSetPagination
    serializer_class = ShowSerealizers

    def get_queryset(self):
        queryset = Show.objects.all()
        title_query = self.request.query_params.get('title', None)
        category_query = self.request.query_params.get('category', None)
        country_query = self.request.query_params.get('country', None)
        year_query = self.request.query_params.get('year', None)

        if title_query:
            queryset = queryset.filter(title__icontains=title_query)
        if category_query:
            if category_query != 'all':
                queryset = queryset.filter(category__name=category_query)
        if country_query:
            if country_query != 'all':
                queryset = queryset.filter(country__name=country_query)
        if year_query:
            if year_query != 'all':
                queryset = queryset.filter(release_year=year_query)
        return queryset

def get_categories(request):
    """
    Returns all categories, to be used in dropdown menu
    """
    if request.method == 'GET' and request.is_ajax():
        categories = Category.objects.all().values_list('name')
        categories = [i[0] for i in list(categories)]
        data = {
            'categories': categories,
        }
        return JsonResponse(data, status=200)

def get_countries(request):
    """
    Returns all countries, to be used in dropdown menu
    """
    if request.method == 'GET' and request.is_ajax():
        countries = Country.objects.all().values_list('name')
        countries = [i[0] for i in list(countries)]
        data = {
            'countries': countries,
        }
        return JsonResponse(data, status=200)

def get_years(request):
    """
    Returns all valid years, to be used in dropdown menu
    """
    if request.method == 'GET' and request.is_ajax():
        years_qs = Show.objects.order_by('-release_year').values_list('release_year', flat=True).distinct()    
        data = {
            'years': list(years_qs),
        }
        return JsonResponse(data, status=200)


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
    return render(request, 'shows/detail_view.html', context)
