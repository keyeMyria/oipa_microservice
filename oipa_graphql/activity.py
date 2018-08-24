import graphene
from django_filters import FilterSet, CharFilter
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from oipa_db.iati.models import Activity, Title, ActivityRecipientCountry
from oipa_db.iati.transaction.models import Transaction
from oipa_db.geodata.models import Country


class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction


class CountryNode(DjangoObjectType):
    polygon = graphene.JSONString()
    center_longlat = graphene.JSONString()

    class Meta:
        model = Country
        exclude_fields = (
            'center_longlat',
        )

    def resolve_polygon(self, context, **kwargs):
        return self.polygon

    def resolve_center_longlat(self, context, **kwargs):
        return self.center_longlat.json


class ActivityRecipientCountryNode(DjangoObjectType):
    country = graphene.List(CountryNode)

    class Meta:
        model = ActivityRecipientCountry

    def resolve_country(self, context, **kwargs):
        return Country.objects.filter(code=self.country_id)


class ActivityNode(DjangoObjectType):
    title = graphene.String()
    transactions = graphene.List(TransactionNode)
    recipient_country = graphene.List(ActivityRecipientCountryNode)

    class Meta:
        model = Activity
        interfaces = (relay.Node, )

    def resolve_title(self, context, **kwargs):
        try:
            narrative = Title.objects.get(
                activity_id=self.id).narratives.first()

            return narrative.content if narrative else ''

        except Title.DoesNotExist:
            pass

        return ''

    def resolve_transactions(self, context, **kwargs):
        return Transaction.objects.filter(activity_id=self.id)

    def resolve_recipient_country(self, context, **kwargs):
        return ActivityRecipientCountry.objects.filter(activity_id=self.id)


class ActivityFilter(FilterSet):
    reporting_organisation = CharFilter(
        method='filter_reporting_organisation')

    class Meta:
        model = Activity
        fields = {
            'iati_identifier': ['exact', ],
            'reporting_organisation': ['exact', ],
            'end_date': ['exact', 'gte', 'lte'],
            'start_date': ['exact', 'gte', 'lte'], }

    def filter_reporting_organisation(self, queryset, name, value):
        name = 'reporting_organisations__organisation__organisation_identifier'
        return queryset.filter(**{name: value})


class Query(object):
    activity = relay.Node.Field(ActivityNode)
    activities = DjangoFilterConnectionField(
        ActivityNode, filterset_class=ActivityFilter)
