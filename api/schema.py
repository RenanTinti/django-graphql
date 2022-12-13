import graphene

# DjangoObjectType is a class that references our custom models in Django
from graphene_django.types import DjangoObjectType

from .models import *

# Creation of MovieType class, that is a type of data of our Movie model. The declaration is very similar to the DRF Serializers
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

class DirectorType(DjangoObjectType):
    class Meta:
        model = Director

# Custom Query class specific to this Movie model. It will be passed as argument to the generic parent Query class, in movies.schema
class Query(graphene.ObjectType):

    # Setting all our movies object to a list of MovieType data. In the graphql interface, it will read "all_movies" as "allMovies"
    all_movies = graphene.List(MovieType)

    # Method to query our objects the same way we do in our views
    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()