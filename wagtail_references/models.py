from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.core.models import CollectionMember, Orderable
from wagtail.search import index
from wagtail.search.queryset import SearchableQuerySetMixin
from wagtail.snippets.models import register_snippet
import jsonfield
from modelcluster.models import ClusterableModel


class ReferenceQuerySet(SearchableQuerySetMixin, models.QuerySet):
    pass


class AbstractReference(ClusterableModel, CollectionMember, Orderable, index.Indexed, models.Model):
    slug = models.CharField(max_length=255, unique=True, verbose_name=_('slug'), help_text=_('A short key to cite the reference by. Determined from the BibTeX entry key. Must be unique.'))
    bibtex = models.TextField(help_text=_('The reference, in bibtex format.'))
    bibtype = models.CharField(max_length=255, verbose_name=_('Bibliography entry type'), default='article', help_text=_('The entry type, detected from the BibTeX entry.'))
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True, db_index=True)
    bibjson = jsonfield.JSONField()
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('created by user'),
        null=True, blank=True, editable=False, on_delete=models.SET_NULL
    )

    objects = ReferenceQuerySet.as_manager()

    search_fields = CollectionMember.search_fields + [
        index.SearchField('slug', partial_match=True, boost=10),
        index.SearchField('bibtex', partial_match=True, boost=10),
        index.AutocompleteField('slug'),
        index.FilterField('bibtype'),
        index.FilterField('created_by_user'),
    ]

    def __str__(self):
        return self.bibtex

    def is_editable_by_user(self, user):
        from wagtail.images.permissions import permission_policy
        return permission_policy.user_has_permission_for_instance(user, 'change', self)

    class Meta:
        abstract = True


@register_snippet
class Reference(AbstractReference):
    admin_form_fields = (
        'bibtex',
        'collection',
    )

    class Meta:
        verbose_name = _('BibTeX Reference')
        verbose_name_plural = _('BibTeX References')
