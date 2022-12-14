import graphene

# Import of child schema file, from our custom app
import api.schema

# Generic Query class, that will take as parameter the Query class of our api app
class Query(api.schema.Query, graphene.ObjectType):
    pass

# Generic Mutation class
class Mutation(api.schema.Mutation, graphene.ObjectType):
    pass

# This is the schema definition, that will query/mutate the data and send them to the graphql url
schema = graphene.Schema(query=Query, mutation=Mutation)