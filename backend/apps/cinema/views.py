from rest_framework import generics
from rest_framework import filters

from apps.cinema.models import *
from apps.cinema.serializers import *


class MoviesList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'buildings__building__name',
                     'buildings__building__city__name', ]


class MovieDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class HottestMoviesList(generics.ListCreateAPIView):
    queryset = Movie.objects.order_by('-clicked')[:3]
    serializer_class = MovieSerializer

class CitiesList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class BuildingsList(generics.ListAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class GenresList(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
