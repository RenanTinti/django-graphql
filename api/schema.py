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
        # We can use kwargs or the parameter itself (id and title). There are two ways to do this
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Movie.objects.get(pk=id)

        if title is not None:
            return Movie.objects.get(title=title)

        return None

# Class to create a movie. When we create or update some entity in our system with GraphQL, we call this a mutation
class MovieCreateMutation(graphene.Mutation):

    # The required arguments to create a new movie (it's not mandatory to be required, we just defined here)
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)

    # Creating a new field with the MovieType, and defining it as movie
    movie = graphene.Field(MovieType)

    # The method will create a new movie object ir our database, like we do in views
    def mutate(self, info, title, year):
        movie = Movie.objects.create(title=title, year=year)

        return MovieCreateMutation(movie=movie)

# Update class
class MovieUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        year = graphene.Int()

    movie = graphene.Field(MovieType)

    def mutate(self, info, id, title, year):
        movie = Movie.objects.get(pk=id)

        if movie.title is not None:
            movie.title = title
        if movie.year is not None:
            movie.year = year

        # Method save to update an object
        movie.save()

        return MovieUpdateMutation(movie=movie)

# Delete class
class MovieDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, id):
        movie = Movie.objects.get(pk=id)
        movie.delete()

        # Since the movie will be removed, we have to return its value as None
        return MovieDeleteMutation(movie=None)

# The method create_movie of this generic class will call the class above, creating the movie when we pass the command and arguments in graphql
class Mutation:
    create_movie = MovieCreateMutation.Field()
    update_movie = MovieUpdateMutation.Field()
    delete_movie = MovieDeleteMutation.Field()



# ================= Aliases and Fragments ====================

# Aliases: used when we want to query the same data two times, just changing the parameters of search. It's basically a name for the query
# Fragments: it's a way to save the same query in a single statement, like saving a value in a variable

# Example:

'''
query {
  firstMovie: movie(id: 1){
      ...movieData
  }
  secondMovie: movie(id: 2){
      ...movieData
  }
}

fragment movieData on MovieType {
  id
  title
}
'''


# ================ Names, Variables and Directives =============

# Names: every query is an anonymous function in graphql. We can name these functions to make our code more readable
# Variables: we can also pass variables directly in the graphql function as parameters, and test some values as arguments in the "Query Variables" window below
# Directive: it's a conditional to check if some data in our query will be shown

# Example:

'''
query MovieAndDirector($id Int, $showDirector: Boolean = true){
    movie(id: $id){
        id
        title
        year
        director @include(if: $showDirector){
            surname
        }
    }
}
'''

# =================== Mutation ====================

# Mutation: used when we want to create or update some object in our system

'''
mutation CreateMovie{
  createMovie(title: "Test", year: 1999){
    movie {
      id
      title
      year
    }
  }
}

mutation UpdateMovie{
    updateMovie(id: 5, title: "Test 2", year: 1980){
        movie {
            id
        }
    }
}

mutation DeleteMovie{
    deleteMovie(id: 5){
        id
    }
}

query QueryMovies{
  allMovies {
    id
    title
    year
  }
}
'''