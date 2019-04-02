from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _


# TODO probably unused. Delete.


class ReferenceField(CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Help text
        self.help_text = _('A bibtex reference')

        # Error messages
        self.error_messages['invalid_reference'] = _('Not a valid bibtex reference.')

        self.error_messages['invalid_image_known_format'] = _(
            "Not a valid %s image."
        )
