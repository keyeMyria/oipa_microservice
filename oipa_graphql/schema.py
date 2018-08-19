import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from oipa_db.iati.models import Activity as ActivityModel, Title as TitleModel


class Title(DjangoObjectType):

    class Meta:
        model = TitleModel
        interfaces = (relay.Node, )


class Activity(DjangoObjectType):
    title = graphene.String()

    class Meta:
        model = ActivityModel
        filter_fields = ['iati_identifier', ]
        interfaces = (relay.Node, )

    def resolve_title(self, args, context, info):
        try:
            narratives = TitleModel.objects.get(
                activity_id=self.id).narratives.all()

            if narratives:
                return narratives[0].content

        except TitleModel.DoesNotExist:
            pass

        return ''


class Query(ObjectType):
    activity = relay.Node.Field(Activity)
    activities = DjangoFilterConnectionField(Activity)


schema = graphene.Schema(query=Query)
