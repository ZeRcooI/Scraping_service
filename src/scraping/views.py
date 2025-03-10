from django.shortcuts import render

from scraping.forms import FindForm
from scraping.models import Vacancy


def home_view(request):
    form = FindForm()

    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    queryset = []

    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        queryset = Vacancy.objects.filter(**_filter)
    return render(request, 'scraping/list.html', {'object_list': queryset, 'form': form})
