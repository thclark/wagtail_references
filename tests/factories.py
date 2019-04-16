import factory
from wagtail_factories import PageFactory

from wagtail_references.models import Reference


class ReferenceFactory(PageFactory):
    """
    Factory for wagtail_references.models.Reference
    """
    title = factory.Sequence('Reference {}'.format)

    class Meta(object):
        model = Reference
