import graphene

from django.db.models import FloatField, Sum
from graphene import relay, String, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django_filters import FilterSet

from oipa_db.iati.transaction.models import Transaction


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


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):

    @classmethod
    def connection_resolver(
            cls, resolver, connection, default_manager, max_limit,
            enforce_first_or_last, filterset_class, filtering_args,
            root, info, **args):

        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = default_manager.get_queryset() \
            if hasattr(default_manager, 'get_queryset') else default_manager

        qs = filterset_class(data=filter_kwargs, queryset=qs).qs
        order = args.get('orderBy', None)

        if order:
            qs = qs.order_by(*order)

        return super(DjangoFilterConnectionField, cls).connection_resolver(
            resolver, connection, qs, max_limit,
            enforce_first_or_last, root, info, **args
        )


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
