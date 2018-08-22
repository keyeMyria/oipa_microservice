import graphene

import oipa_graphql.activity
import oipa_graphql.transaction


class Query(oipa_graphql.activity.Query, oipa_graphql.transaction.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
