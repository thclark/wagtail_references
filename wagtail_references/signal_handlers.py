import logging
from django.db.models.signals import pre_save
from wagtail_references import get_reference_model


logger = logging.getLogger(__name__)


def update_from_bibtex(instance, *args, **kwargs):
    """ A signal to always update the reference from its bibtex prior to saving
    """
    instance.update_from_bibtex()


def register_signal_handlers():
    pre_save.connect(update_from_bibtex, sender=get_reference_model())
