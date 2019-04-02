from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


default_app_config = 'wagtail_references.apps.ReferencesAppConfig'


def get_reference_model_string():
    """
    Get the dotted ``app.Model`` name for the reference model as a string.
    Useful for developers making Wagtail plugins that need to refer to the
    reference model, such as in foreign keys, but the model itself is not required.
    """
    return getattr(settings, 'WAGTAILREFERENCES_REFERENCE_MODEL', 'wagtail_references.Reference')


def get_reference_model():
    """
    Get the reference model from the ``WAGTAILREFERENCES_REFERENCE_MODEL`` setting.
    Useful for developers making Wagtail plugins that need the reference model.
    Defaults to the standard :class:`~wagtail.references.models.Reference` model
    if no custom model is defined.
    """
    from django.apps import apps
    model_string = get_reference_model_string()
    try:
        return apps.get_model(model_string)
    except ValueError:
        raise ImproperlyConfigured("WAGTAILREFERENCES_REFERENCE_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "WAGTAILREFERENCES_REFERENCE_MODEL refers to model '%s' that has not been installed" % model_string
        )
