import graphene
from graphene_django import DjangoObjectType
from .models import Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('id', 'title', 'excerpt')

class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    
    def resolve_all_books(root, info):
        return Book.objects.filter(title="Title 01")


schema = graphene.Schema(query=Query)