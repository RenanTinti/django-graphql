from django.contrib import admin
from django.urls import path, include

# GraphQL view to generate an url where we can see our data
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Graphql urls to show our data. The GraphQLView needs to be imported
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
