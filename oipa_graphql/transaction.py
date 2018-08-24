import graphene
from django.db.models import Sum
from graphene import relay, String, List, Scalar
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
            'ref': ['exact', ], }


class TransactionSummaryNode(graphene.ObjectType):
    value = graphene.Float()
    recipientCountryCode = graphene.String()
    recipientCountryName = graphene.String()

    FIELDS_MAPPING = {
        'recipientCountryCode': 'activity__recipient_country__code',
        'recipientCountryName': 'activity__recipient_country__name'}

    FIELDS_FILTER_MAPPING = {
        'recipientCountryCodeIn': 'activity__recipient_country__code__in', }

    class Meta:
        interfaces = (relay.Node, )

    def get_group_by(self, context, **kwargs):
        return [self.FIELDS_MAPPING.get(field) for field in kwargs['groupBy']]

    def get_order_by(self, context, **kwargs):
        return [('-' if '-' == field[0] else '') + self.FIELDS_MAPPING
                .get(field.replace('-', '')) for field in kwargs['orderBy']]

    def get_filters(self, context, **kwargs):
        filters = {}
        for field, filter_field in self.FIELDS_FILTER_MAPPING.items():
            value = kwargs.get(field)
            if field:
                filters[filter_field] = value

        return filters

    def get_results(self, context, **kwargs):
        filters = self.get_filters(context, **kwargs)
        groups = self.get_group_by(context, **kwargs)
        orders = self.get_order_by(context, **kwargs)
        aggregation = kwargs['aggregation']
        return Transaction.objects.values(*groups).annotate(
            **{field: Sum(field) for field in aggregation}
        ).order_by(*orders).filter(**filters)

    def get_node_summaries(self, context, **kwargs):
        results = self.get_results(context, **kwargs)
        nodes = []
        aggregation = kwargs['aggregation']
        for result in results:
            node = TransactionSummaryNode(**{field: result[
                self.FIELDS_MAPPING.get(
                    field)] for field in kwargs['groupBy']})

            for field in aggregation:
                setattr(node, field, result[field])

            nodes.append(node)

        return nodes


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
        return TransactionSummaryNode().get_node_summaries(context, **kwargs)
