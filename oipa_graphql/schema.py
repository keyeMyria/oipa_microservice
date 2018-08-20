import graphene
from django_filters import FilterSet, CharFilter
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


class ActivityFilter(FilterSet):
    reporting_organisation = CharFilter(
        method='filter_reporting_organisation')

    class Meta:
        model = Activity
        fields = ['iati_identifier', 'reporting_organisation', ]

    def filter_reporting_organisation(self, queryset, name, value):
        name = 'reporting_organisations__organisation__organisation_identifier'
        return queryset.filter(**{name: value})


class Query(ObjectType):
    activity = relay.Node.Field(ActivityNode)
    activities = DjangoFilterConnectionField(
        ActivityNode, filterset_class=ActivityFilter)


schema = graphene.Schema(query=Query)
