from django.test import TestCase
from django.urls import reverse
from wagtail.tests.utils import WagtailTestUtils

from wagtail_references.models import Reference
from wagtail_references.serializers import ReferenceSerializer
from wagtail_references import examples


class TestReferenceAdminViews(TestCase, WagtailTestUtils):

    def setUp(self):
        self.login()

    def test_index(self):
        """ Test that the index page renders with the correct template
        """
        response = self.client.get(reverse('wagtail_references:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtail_references/references/index.html')
        self.assertContains(response, "Add a reference")

    def test_add(self):
        """ Test the ability to post a new reference
        """
        response = self.client.post(
            reverse('wagtail_references:add'),
            data={'bibtex': examples.article1},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reference.objects.count(), 1)

    def test_get_edit_view(self):
        """ Test the ability to load the edit page for a reference
        """
        self.client.post(
            reverse('wagtail_references:add'),
            data={'bibtex': examples.article1},
        )
        response = self.client.get('/admin/references/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtail_references/references/edit.html')

    def test_get_edit_with_same_slug(self):
        """ Test the ability to edit a reference whilst retaining the same slug
        """
        self.client.post(
            reverse('wagtail_references:add'),
            data={'bibtex': examples.article1},
        )
        ref = Reference.objects.first()
        ref.bibtex = examples.article1_edited,
        response = self.client.post(
            reverse('wagtail_references:edit', args=(ref.id,)),
            data={
                'bibtex': examples.article1_edited,
                'slug': ref.slug,
            },
            follow=False,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reference.objects.count(), 1)
        ref_updated = Reference.objects.first()
        self.assertEqual('Fewer, AuthorsAfterEditing', ref_updated.bibjson['author'][0]['name'])

    def test_get_edit_with_new_slug(self):
        """ Test the ability to edit a reference whilst retaining the same slug
        """
        self.client.post(
            reverse('wagtail_references:add'),
            data={'bibtex': examples.article1},
        )
        ref = Reference.objects.first()
        ref.bibtex = examples.article1_edited,
        response = self.client.post(
            reverse('wagtail_references:edit', args=(ref.id,)),
            data={
                'bibtex': examples.article1,
                'slug': 'some-new-slug',
            },
            follow=False,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reference.objects.count(), 1)
        ref_updated = Reference.objects.first()
        self.assertEqual('some-new-slug', ref_updated.bibjson['citekey'])

    def test_broken_bibtex(self):
        """ Test what happens when broken or incomplete bibtex is supplied
        """
        pass

    def test_multiple_entries(self):
        """ Test that multiple bibtex entries are ignored favouring only the first one
        :return:
        """
        pass

    def test_duplicate_slug_handled(self):
        """ Tests that autoslugging correctly handles duplicate slugs.
        For versions <= 0.2.0 the slug of the snippet was automatically extracted from the bibtex. This caused a server
        error on duplicate slugs if you re-entered the same reference (or another one with the same reference string)
        """
        response = self.client.post(
            reverse('wagtail_references:add'),
            data={'bibtex': examples.article1},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reference.objects.count(), 1)

        # Post the same one again
        response2 = self.client.post(
            reverse('wagtail_references:add'),
            data={'bibtex': examples.article1},
        )
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(Reference.objects.count(), 2)

        # Ensure the slug is the same but autoincremented
        ref1 = Reference.objects.first()
        ref2 = Reference.objects.last()
        self.assertEqual(ref2.slug, '{}-2'.format(ref1.slug))

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
