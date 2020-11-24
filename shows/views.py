from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView

from .models import Show, Category, Country
from .serealizers import ShowSerealizers
from .pagination import StandardResultsSetPagination

from .forms import SearchForm


# def show_search(request):
#     """
#     Returns the show search template
#     """
#     form = SearchForm(request.GET)
#     if form.is_valid():
#         title_search = form.cleaned_data['title_search']
#         category_search = form.cleaned_data['category_search']
#         country_search = form.cleaned_data['country_search']
#         year_search = form.cleaned_data['year_search']
#         print('Title search: ', title_search)
#         print('Category search: ', category_search)
#         print('Country search: ', country_search)
#         print('Year search: ', year_search)

#     else:
#         print('Invalid form')
    
#     return render(request, 'shows/show_search.html', {'form': form})

class ShowSearch(ListView):
    """
    Class-based view for controlling show search
    """
    model = Show
    template_name = 'shows/show_search.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = Show.objects.all()
        title_search = self.request.GET.get('title')
        category_search = self.request.GET.get('category')
        country_search = self.request.GET.get('country')
        year_search = self.request.GET.get('year')

        print('title_search: ', title_search)
        print('category_search: ', category_search)
        print('category_search type: ', type(category_search))
        print('country_search:', country_search)
        print('year_search: ', year_search)

        if title_search is not None:
            if title_search != '':
                print('title')
                queryset = queryset.filter(title__icontains=title_search)
        if category_search is not None:
            if category_search != '':
                print('category')
                queryset = queryset.filter(category__name=category_search)
        if country_search is not None:
            if country_search != '':
                print('country')
                queryset = queryset.filter(country__name=country_search)
        if year_search is not None:
            print('year search ttype: ', type(year_search))
            if year_search != '0':
                print('year_search')
                queryset = queryset.filter(release_year=year_search)


        print('len queryset: ', len(queryset))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = SearchForm()
        return context



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


class ShowListing(ListView):
    """
    Uses DRF ListAPIView to provide an API for show search
    """
    model = Show
    # set the pagination and serializer class
    pagination_class = StandardResultsSetPagination
    serializer_class = ShowSerealizers

    def get_queryset(self):
        """
        Filters queryset based on search params
        """
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

def add_like(request):
    """
    Ajax call to add like
    """
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        show_id = request.POST.get('show_id')
        show = Show.objects.get(show_id=show_id)
        user.likes.add(show)
        user.save()
        return HttpResponse(status=200)

def remove_like(request):
    """
    Ajax call to remove like
    """
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        show_id = request.POST.get('show_id')
        show = Show.objects.get(show_id=show_id)
        user.likes.remove(show)
        user.save()
        return HttpResponse(status=200)
