# from datetime import timedelta
# from django.core.exceptions import ValidationError
# from django.core.paginator import Page as PaginatorPage
# from django.core.paginator import Paginator
from django.test import TestCase
# from django.utils import timezone
# from mock import patch, Mock
# from modelcluster.fields import ParentalKey
# from wagtail.core.fields import StreamField
# from wagtail.core.models import Page
# from wagtail_factories import SiteFactory


# from tests import factories
# from wagtail_references.models import Reference


class TestReference(TestCase):

    def setUp(self):
        pass

    def test_broken_bibtex(self):
        """
        Tests what happens when broken or incomplete bibtex is supplied
        """
        pass

    def test_multiple_entries(self):
        """
        Tests that multiple bibtex entries are ignored favouring only the first one
        :return:
        """
        pass
