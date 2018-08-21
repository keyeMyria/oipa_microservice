import graphene
from django.db.models import Sum
from graphene import relay, String, List
from graphene_django import DjangoObjectType
from django_filters import FilterSet
from oipa_db.iati.transaction.models import Transaction
from oipa_graphql.utils import OrderedDjangoFilterConnectionField


class TransactionListNode(DjangoObjectType):

    class Meta:
        model = Transaction
        interfaces = (relay.Node, )


class TransactionListFilter(FilterSet):

    class Meta:
        model = Transaction
        fields = {
            'ref': ['exact', ],
        }


class TransactionSummaryNode(graphene.ObjectType):
    value = graphene.Float()
    activity__recipient_country__code = graphene.String()

    class Meta:
        interfaces = (relay.Node, )


class Query(object):
    transaction = relay.Node.Field(TransactionListNode)
    transactions = OrderedDjangoFilterConnectionField(
        TransactionListNode,
        filterset_class=TransactionListFilter,
        orderBy=List(of_type=String)
    )

    transaction_summaries = graphene.List(
        TransactionSummaryNode,
        groupBy=String(),
        orderBy=String()
    )

    def resolve_transaction_summaries(self, context, **kwargs):
        results = Transaction.objects.\
            values(kwargs['groupBy']).\
            annotate(value=Sum('value')).\
            order_by(kwargs['orderBy'])

        return [TransactionSummaryNode(
            activity__recipient_country__code=result[
                'activity__recipient_country__code'],
            value=result['value']) for result in results
        ]
