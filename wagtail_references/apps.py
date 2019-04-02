from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReferencesAppConfig(AppConfig):
    name = 'wagtail_references'
    label = 'wagtail_references'
    verbose_name = _('Wagtail References')

    def ready(self):
        from wagtail_references.signal_handlers import register_signal_handlers
        register_signal_handlers()
