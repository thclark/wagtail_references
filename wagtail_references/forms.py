from django import forms
from django.forms.models import modelform_factory
from django.utils.translation import ugettext as _
from wagtail.admin.forms.collections import (BaseCollectionMemberForm, collection_member_permission_formset_factory)
from wagtail_references.models import Reference
from wagtail_references.permissions import permission_policy as references_permission_policy


def formfield_for_dbfield(db_field, **kwargs):
    return db_field.formfield(**kwargs)


class BaseReferenceForm(BaseCollectionMemberForm):
    permission_policy = references_permission_policy


def get_reference_form(model, include_slug=False):
    fields = model.admin_form_fields
    if 'collection' not in fields:
        # force addition of the 'collection' field, because leaving it out can
        # cause dubious results when multiple collections exist (e.g adding the
        # document to the root collection where the user may not have permission) -
        # and when only one collection exists, it will get hidden anyway.
        fields = list(fields) + ['collection']

    if include_slug and 'slug' not in fields:
        # we want to include slug in edit forms, but not in addition form
        fields = list(fields) + ['slug']

    return modelform_factory(
        model,
        form=BaseReferenceForm,
        fields=fields,
        formfield_callback=formfield_for_dbfield
    )


class ReferenceInsertionForm(forms.Form):
    """
    Form for selecting parameters of the reference (e.g. format) prior to insertion
    """
    # format = forms.ChoiceField(
    #     choices=[(format.slug, format.label) for format in get_image_formats()],
    #     widget=forms.RadioSelect
    # )
    bibtex = forms.CharField()


GroupReferencePermissionFormSet = collection_member_permission_formset_factory(
    Reference,
    [
        ('add_reference', _("Add"), _("Add/edit references you own")),
        ('change_reference', _("Edit"), _("Edit any reference")),
    ],
    'wagtail_references/permissions/includes/reference_permissions_formset.html'
)
