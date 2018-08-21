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
    recipient_country_code = graphene.String()
    recipient_country_name = graphene.String()

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
        field_group_by = TransactionSummaryNode.FIELDS_MAPPING.get(
            kwargs['groupBy'])
        field_order_by = TransactionSummaryNode.FIELDS_MAPPING.get(
            kwargs['orderBy'])

        results = Transaction.objects.\
            values(field_group_by).\
            annotate(value=Sum('value')).\
            order_by(field_order_by)

        return [TransactionSummaryNode(
            recipient_country_code=result[
                'activity__recipient_country__code'],
            value=result['value']) for result in results
        ]
