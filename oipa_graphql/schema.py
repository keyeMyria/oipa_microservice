import graphene

import oipa_graphql.activity


class Query(oipa_graphql.activity.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
