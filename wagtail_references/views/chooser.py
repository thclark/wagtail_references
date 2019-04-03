from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.utils import PermissionPolicyChecker
from wagtail.core import hooks
from wagtail.core.models import Collection
from wagtail.utils.pagination import paginate

from wagtail_references import get_reference_model
from wagtail_references.forms import ReferenceInsertionForm, get_reference_form
from wagtail_references.permissions import permission_policy


permission_checker = PermissionPolicyChecker(permission_policy)


def get_chooser_js_data():
    """construct context variables needed by the chooser JS"""
    return {
        'step': 'chooser',
        'error_label': _("Server Error"),
        'error_message': _("Report this error to your webmaster with the following information:"),
    }


def get_reference_result_data(reference):
    """
    helper function: given a reference, return the json data to pass back to the
    reference chooser panel
    """
    return {
        'id': reference.id,
        'edit_link': reverse('wagtailreferences:edit', args=(reference.id,)),
        'slug': reference.slug,
        'preview': {
            'bibtex': reference.bibtex
        }
    }


def get_chooser_context(request):
    """Helper function to return common template context variables for the main chooser view"""

    collections = Collection.objects.all()
    if len(collections) < 2:
        collections = None
    else:
        collections = Collection.order_for_display(collections)

    return {
        'searchform': SearchForm(),
        'is_searching': False,
        'query_string': None,
        'will_select_format': request.GET.get('select_format'),
        'collections': collections,
    }


def chooser(request):
    Reference = get_reference_model()

    if permission_policy.user_has_permission(request.user, 'add'):
        ReferenceForm = get_reference_form(Reference)
        uploadform = ReferenceForm(user=request.user)
    else:
        uploadform = None

    # TODO add an author field and order by that
    references = Reference.objects.order_by('-created_at')

    # allow hooks to modify the queryset
    for hook in hooks.get_hooks('construct_reference_chooser_queryset'):
        references = hook(references, request)

    if (
        'q' in request.GET or 'p' in request.GET or 'tag' in request.GET
        or 'collection_id' in request.GET
    ):
        # this request is triggered from search, pagination or 'popular tags';
        # we will just render the results.html fragment
        collection_id = request.GET.get('collection_id')
        if collection_id:
            references = references.filter(collection=collection_id)

        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']

            references = references.search(q)
            is_searching = True
        else:
            is_searching = False
            q = None

        paginator, images = paginate(request, references, per_page=50)
        return render(request, "wagtail_references/chooser/results.html", {
            'references': references,
            'is_searching': is_searching,
            'query_string': q,
            'will_select_format': request.GET.get('select_format')
        })
    else:
        paginator, images = paginate(request, references, per_page=50)
        context = get_chooser_context(request)
        context.update({
            'references': references,
            'uploadform': uploadform,
        })
        return render_modal_workflow(
            request, 'wagtail_references/chooser/chooser.html', None, context
        )


def reference_chosen(request, reference_id):
    reference = get_object_or_404(get_reference_model(), id=reference_id)

    return render_modal_workflow(
        request, None, None,
        None, json_data={'step': 'reference_chosen', 'result': get_reference_result_data(reference)}
    )


def chooser_select_format(request, reference_id):
    reference = get_object_or_404(get_reference_model(), id=reference_id)

    if request.method == 'POST':
        form = ReferenceInsertionForm(request.POST)
        if form.is_valid():
            reference_data = {
                'id': reference.id,
                'slug': reference.slug,
                'edit_link': reverse('wagtailreferences:edit', args=(reference.id,)),
                'bibtex': reference.bibtex
            }

            return render_modal_workflow(
                request, None, None,
                None, json_data={'step': 'reference_chosen', 'result': reference_data}
            )
    else:
        initial = {}
        initial.update(request.GET.dict())
        form = ReferenceInsertionForm(initial=initial)

    return render_modal_workflow(
        request, 'wagtail_references/chooser/select_format.html', None,
        {'reference': reference, 'form': form}, json_data={'step': 'select_format'}
    )
