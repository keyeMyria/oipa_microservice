from django.core.management.base import BaseCommand

from oipa_db.iati.activity_search_indexes import (
    reindex_activity, reindex_activity_by_source, reindex_all_activities
)
from oipa_db.iati.models import Activity


class Command(BaseCommand):
    """
        Reindex full text search values for all activities
    """

    def add_arguments(self, parser):
        parser.add_argument('--activity',
                            action='store',
                            dest='activity',
                            default=None,
                            help='Reindex only this activity')

        parser.add_argument('--source',
                            action='store',
                            dest='source',
                            default=None,
                            help='Reindex only activities with this dataset_id'
                            )

    def handle(self, *args, **options):
        if options['activity']:
            activity = Activity.objects.get(
                iati_identifier=options['activity'])
            reindex_activity(activity)
        elif options['source']:
            reindex_activity_by_source(options['source'])
        else:
            reindex_all_activities()
