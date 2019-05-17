from django.conf.urls import include, url
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from wagtail.admin.menu import MenuItem
from wagtail.admin.search import SearchArea
from wagtail.admin.site_summary import SummaryItem
from wagtail.core import hooks

from wagtail_references import admin_urls, get_reference_model
from wagtail_references.forms import GroupReferencePermissionFormSet
from wagtail_references.permissions import permission_policy


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^references/', include(admin_urls, namespace='wagtailreferences')),
    ]


class ReferencesMenuItem(MenuItem):
    def is_shown(self, request):
        return permission_policy.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )


@hooks.register('register_admin_menu_item')
def register_images_menu_item():
    return ReferencesMenuItem(
        _('References'), reverse('wagtail_references:index'),
        name='references', classnames='icon icon-list-ol', order=300
    )


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
        <script>
            window.chooserUrls.referenceChooser = '{0}';
        </script>
        """,
        reverse('wagtail_references:chooser')
    )


class ReferencesSummaryItem(SummaryItem):
    order = 200
    template = 'wagtail_references/homepage/site_summary_references.html'

    def get_context(self):
        return {
            'total_references': get_reference_model().objects.count(),
        }

    def is_shown(self):
        return permission_policy.user_has_any_permission(
            self.request.user, ['add', 'change', 'delete']
        )


@hooks.register('construct_homepage_summary_items')
def add_references_summary_item(request, items):
    items.append(ReferencesSummaryItem(request))


class ReferencesSearchArea(SearchArea):
    def is_shown(self, request):
        return permission_policy.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )


@hooks.register('register_admin_search_area')
def register_references_search_area():
    return ReferencesSearchArea(
        _('References'), reverse('wagtail_references:index'),
        name='references',
        classnames='icon icon-list-ol',
        order=200)


@hooks.register('register_group_permission_panel')
def register_reference_permissions_panel():
    return GroupReferencePermissionFormSet


@hooks.register('describe_collection_contents')
def describe_collection_docs(collection):
    references_count = get_reference_model().objects.filter(collection=collection).count()
    if references_count:
        url = reverse('wagtail_references:index') + ('?collection_id=%d' % collection.id)
        return {
            'count': references_count,
            'count_text': ungettext(
                "%(count)s reference",
                "%(count)s references",
                references_count
            ) % {'count': references_count},
            'url': url,
        }
