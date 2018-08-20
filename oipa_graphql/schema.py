import graphene
import django_filters
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from oipa_db.iati.models import Activity, Title
from oipa_db.iati.transaction.models import Transaction


class TransactionNode(DjangoObjectType):

    class Meta:
        model = Transaction


class ActivityNode(DjangoObjectType):
    title = graphene.String()
    transactions = graphene.List(TransactionNode)

    class Meta:
        model = Activity
        filter_fields = ['iati_identifier', ]
        interfaces = (relay.Node, )

    def resolve_title(self, args, context, info):
        try:
            narrative = Title.objects.get(
                activity_id=self.id).narratives.first()

            return narrative.content if narrative else ''

        except Title.DoesNotExist:
            pass

        return ''

    def resolve_transactions(self, args, context, info):
        return Transaction.objects.filter(activity_id=self.id)


class ActivityFilter(django_filters.FilterSet):
    reporting_organisation = django_filters.CharFilter(
        method='filter_reporting_organisation')

    class Meta:
        model = Activity
        fields = ['reporting_organisation', ]

    def filter_reporting_organisation(self, queryset, name, value):
        return queryset.filter(
            reporting_organisations__organisation__organisation_identifier
            =value)


class Query(ObjectType):
    activity = relay.Node.Field(ActivityNode)
    activities = DjangoFilterConnectionField(
        ActivityNode, filterset_class=ActivityFilter)


schema = graphene.Schema(query=Query)
