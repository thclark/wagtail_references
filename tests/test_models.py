from django.test import TestCase

from wagtail_references.models import Reference
from wagtail_references.serializers import ReferenceSerializer
from wagtail_references import examples


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

    def test_duplicate_slug_handled(self):
        """ Tests that autoslugging correctly handles duplicate slugs.
        For versions <= 0.2.0 the slug of the snippet was automatically extracted from the bibtex. This caused a server
        error on duplicate slugs if you re-entered the same reference (or anotehr one with the same reference string)
        """
        ref1 = Reference.objects.create(bibtex=examples.article1)
        ref1.save()
        ref2 = Reference.objects.create(bibtex=examples.article1)
        ref2.save()

    def test_serializer(self):
        ref = Reference.objects.create(bibtex=examples.article1)
        ref.save()
        ser = ReferenceSerializer()
        rep = ser.to_representation(ref)
        self.assertIn('bibjson', rep.keys())
        bibjson = rep['bibjson']
        self.assertIn('journal', bibjson.keys())
        self.assertIn('title', bibjson.keys())
        self.assertIn('author', bibjson.keys())
        self.assertEqual(6, len(bibjson['author']))
