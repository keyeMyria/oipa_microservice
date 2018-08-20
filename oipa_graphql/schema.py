import graphene
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


class Query(ObjectType):
    activity = relay.Node.Field(ActivityNode)
    activities = DjangoFilterConnectionField(ActivityNode)


schema = graphene.Schema(query=Query)
