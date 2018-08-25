import graphene
from graphene import relay, String, List
from graphene_django import DjangoObjectType
from django_filters import FilterSet
from oipa_db.iati.models import Transaction
from oipa_graphql.utils import OrderedDjangoFilterConnectionField, SummaryNode


class TransactionListNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces = (relay.Node, )


class TransactionListFilter(FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'ref': ['exact', ], }


class TransactionSummaryNode(SummaryNode):
    value = graphene.Float()
    recipientCountryCode = graphene.String()
    recipientCountryName = graphene.String()

    Model = Transaction
    FIELDS_MAPPING = {
        'recipientCountryCode': 'activity__recipient_country__code',
        'recipientCountryName': 'activity__recipient_country__name'}
    FIELDS_FILTER_MAPPING = {
        'recipientCountryCodeIn': 'activity__recipient_country__code__in', }


class Query(object):
    transaction = relay.Node.Field(TransactionListNode)
    transactions = OrderedDjangoFilterConnectionField(
        TransactionListNode,
        filterset_class=TransactionListFilter,
        orderBy=List(of_type=String))

    transaction_summaries = graphene.List(
        TransactionSummaryNode,
        groupBy=List(of_type=String),
        orderBy=List(of_type=String),
        aggregation=List(of_type=String),
        recipientCountryCodeIn=List(of_type=String))

    def resolve_transaction_summaries(self, context, **kwargs):
        return TransactionSummaryNode().get_nodes(context, **kwargs)
