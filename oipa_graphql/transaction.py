import graphene
from django.db.models import Sum
from graphene import relay, String, List
from graphene_django import DjangoObjectType
from django_filters import FilterSet
from oipa_db.iati.transaction.models import Transaction
from oipa_graphql.utils import (
    OrderedDjangoFilterConnectionField,
    list_string_comma
)


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
    recipientCountryCode = graphene.String()
    recipientCountryName = graphene.String()

    FIELDS_MAPPING = {
        'recipientCountryCode': 'activity__recipient_country__code',
        'recipientCountryName': 'activity__recipient_country__name'
    }

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
        mapping = TransactionSummaryNode.FIELDS_MAPPING
        groups = [mapping.get(
            value) for value in list_string_comma(kwargs['groupBy'])
        ]
        orders = [mapping.get(
            value) for value in list_string_comma(kwargs['orderBy'])
        ]

        results = Transaction.objects.values(*groups).\
            annotate(value=Sum('value')).order_by(*orders)

        return [TransactionSummaryNode(
            recipientCountryCode=result[
                'activity__recipient_country__name'],
            recipientCountryName=result[
                'activity__recipient_country__code'],
            value=result['value']) for result in results
        ]
