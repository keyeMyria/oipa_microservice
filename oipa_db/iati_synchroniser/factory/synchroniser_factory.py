from datetime import datetime

from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from oipa_db.iati.factory.iati_factory import OrganisationFactory
from oipa_db.iati_synchroniser.models import Dataset, Publisher


class NoDatabaseFactory(DjangoModelFactory):
    @classmethod
    def _setup_next_sequence(cls):
        return 0


class PublisherFactory(NoDatabaseFactory):
    class Meta:
        model = Publisher
        django_get_or_create = ['publisher_iati_id']

    organisation = SubFactory(OrganisationFactory)
    iati_id = 'random-string'
    publisher_iati_id = 'NL-KVK-123456'
    name = 'dutchorg'
    display_name = 'Dutch organisation'


class DatasetFactory(NoDatabaseFactory):
    class Meta:
        model = Dataset

    iati_id = Sequence(
        lambda n: '{0}{0}{0}{0}{0}-{0}{0}{0}{0}{0}-{0}{0}{0}{0}{0}-{0}{0}{0}{0}{0}-'.format(n)  # NOQA: E501
    )
    name = 'nl-1'
    title = '1998-2008 Activities'
    filetype = 1
    publisher = SubFactory(PublisherFactory)
    source_url = 'http://nourl.com/NL-1.xml'
    date_created = datetime(2016, 1, 1)
    date_updated = datetime(2016, 1, 2)
    last_found_in_registry = datetime(2016, 1, 3)
    iati_version = '2.02'
    is_parsed = True
    added_manually = False
