import graphene

# DjangoObjectType is a class that references our custom models in Django
from graphene_django.types import DjangoObjectType

from .models import *

# Creation of MovieType class, that is a type of data of our Movie model. The declaration is very similar to the DRF Serializers
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

    # New attribute created for the MovieType class. This is not an attribute of our Movie model. It can be used only in graphql query
    movie_age = graphene.String()

    # Resolving the movie_age attribute. It can be queried as "movieAge" in graphql url. Any logic can be added inside this method
    def resolve_movie_age(self, info):
        return "Old movie" if self.year < 2000 else "New movie"

# GraphQL only recognizes data types in its interface, not objects. So, if we try to query the director foreign key in the Movie class, an error will occur. To fix this, we need to create a DirectorType, as shown below
# Just writing the director foreign key in the graphql is not enough. We ha ve to tell which attibutes we want to query. In our case, we will query both name and surname
class DirectorType(DjangoObjectType):
    class Meta:
        model = Director

# Custom Query class specific to this Movie model. It will be passed as argument to the generic parent Query class, in movies.schema
class Query(graphene.ObjectType):

    # Setting all our movies object to a list of MovieType data. In the graphql interface, it will read "all_movies" as "allMovies"
    all_movies = graphene.List(MovieType)

    # Setting all our directors type in a list
    all_directors = graphene.List(DirectorType)

    # Setting an attribute to query a single object by its id. It is necessary to create a specific resolve method to it too
    # It is possible to pass another parameters, like the title in the exmaple below
    movie = graphene.Field(MovieType, id=graphene.Int(), title=graphene.String())

    # Method to query our objects the same way we do in our views
    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()

     # Method to query our objects the same way we do in our views
    def resolve_all_directors(self, info, **kwargs):
        return Director.objects.all()

    # Method to query a single object by its id
    def resolve_movie(self, info, **kwargs):

        # Getting the id from the kwargs. The id needs to be passed as argument in the query in graphql interface
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Movie.objects.get(pk=id)

        if title is not None:
            return Movie.objects.get(title=title)

        return None



# ================= Aliases and Fragments ====================

# Aliases: used when we want to query the same data two times, just changing the parameters of search
# Fragments: it's a way to save the same query in a single statement, like saving a value in a variable
# 
# Example:
# 
# query {
#   firstMovie: movie(id 1){
#       ...movieData
#   }
#   secondMovie: movie(id 2){
#       ...movieData
#   }
# }
#
# fragment movieData on MovieType {
#   id
#   title
# }