import logging
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import homogenize_latex_encoding, convert_to_unicode
from django.conf import settings
from django.db.models.signals import pre_save
from wagtail_references import get_reference_model
from wagtail_references.bibjson import record_from_entry


logger = logging.getLogger(__name__)


def pre_save_reference_conversion(instance, **kwargs):
    """ Perform (optional) parsing and conversion of bibtex to ensure validity and force to a uniform type.

    Uses BibtexParser library. Your bibtex may contain accents and specific characters. They are sometimes coded like
    this \'{e} but this is not the correct way. {\'e} is preferred by latex... but for purposes other than using latex,
    you may wish to clean up such entries to unicode e.g. é.

    If WAGTAILREFERENCES_CONVERT_BIBTEX is True (default), clean and convert the input bibtex.
    If 'WAGTAILREFERENCES_ENABLE_UNICODE', is True (default False), convert to unicode, otherwise convert to homogenised LaTeX.

    The entry ID key is always forced to lower case to avoid confusing duplicates.

    :param instance:
    :param kwargs:
    :return:
    """
    parser = BibTexParser()
    if getattr(settings, 'WAGTAILREFERENCES_CONVERT_BIBTEX', True):
        if getattr(settings, 'WAGTAILREFERENCES_ENABLE_UNICODE', True):
            parser.customization = convert_to_unicode
        else:
            parser.customization = homogenize_latex_encoding

    bib_database = bibtexparser.loads(instance.bibtex, parser=parser)

    assert len(bib_database.entries) > 0
    if len(bib_database.entries) > 1:
        bib_database.entries = [bib_database.entries[0]]
        logger.warning('More than one entry in submitted bibtex string. Removing all but the first.')

    bib_database.entries[0]['ID'] = bib_database.entries[0]['ID'].lower()

    writer = BibTexWriter()
    writer.indent = '    '

    instance.slug = bib_database.entries[0]['ID']
    instance.bibtype = bib_database.entries[0]['ENTRYTYPE']
    instance.bibtex = bibtexparser.dumps(bib_database, writer=writer)
    instance.bibjson_record = record_from_entry(
        bib_database.entries[0]['ID'],
        bib_database.entries[0],
        getattr(settings, 'WAGTAILREFERENCES_COLLECTION_NAME', None)
    )


def register_signal_handlers():
    pre_save.connect(pre_save_reference_conversion, sender=get_reference_model())
