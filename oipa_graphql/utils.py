import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from django.db import models
from django.db.models import Sum


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


class SummaryNode(graphene.ObjectType):
    FIELDS_MAPPING = {}
    FIELDS_FILTER_MAPPING = {}
    Model = models.Model

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
            if value:
                filters[filter_field] = value

        return filters

    def get_results(self, context, **kwargs):
        filters = self.get_filters(context, **kwargs)
        groups = self.get_group_by(context, **kwargs)
        orders = self.get_order_by(context, **kwargs)

        return self.Model.objects.values(*groups).annotate(
            **{field: Sum(field) for field in kwargs['aggregation']}
        ).order_by(*orders).filter(**filters)

    def get_nodes(self, context, **kwargs):
        results = self.get_results(context, **kwargs)
        nodes = []
        aggregation = kwargs['aggregation']
        for result in results:
            node = self.__class__(**{field: result[
                self.FIELDS_MAPPING.get(
                    field)] for field in kwargs['groupBy']})

            for field in aggregation:
                setattr(node, field, result[field])

            nodes.append(node)

        return nodes
