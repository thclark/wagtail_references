from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.vary import vary_on_headers
from wagtail.admin import messages
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.utils import PermissionPolicyChecker, permission_denied
from wagtail.core.models import Collection
from wagtail.search import index as search_index
from wagtail.utils.pagination import paginate

from wagtail_references import get_reference_model
from wagtail_references.forms import get_reference_form
from wagtail_references.permissions import permission_policy


permission_checker = PermissionPolicyChecker(permission_policy)


@permission_checker.require_any('add', 'change', 'delete')
@vary_on_headers('X-Requested-With')
def index(request):

    # Get references (filtered by user permission)
    references = permission_policy.instances_user_has_any_permission_for(
        request.user, ['change', 'delete']
    ).order_by('-created_at')

    # Search
    query_string = None
    if 'q' in request.GET:
        form = SearchForm(request.GET, placeholder=_("Search references"))
        if form.is_valid():
            query_string = form.cleaned_data['q']

            references = references.search(query_string)
    else:
        form = SearchForm(placeholder=_("Search references"))

    # Filter by collection
    current_collection = None
    collection_id = request.GET.get('collection_id')
    if collection_id:
        try:
            current_collection = Collection.objects.get(id=collection_id)
            references = references.filter(collection=current_collection)
        except (ValueError, Collection.DoesNotExist):
            pass

    paginator, references = paginate(request, references)

    collections = permission_policy.collections_user_has_any_permission_for(
        request.user, ['add', 'change']
    )
    if len(collections) < 2:
        collections = None

    # Create response
    if request.is_ajax():
        return render(request, 'wagtail_references/references/results.html', {
            'references': references,
            'query_string': query_string,
            'is_searching': bool(query_string),
        })
    else:
        return render(request, 'wagtail_references/references/index.html', {
            'references': references,
            'query_string': query_string,
            'is_searching': bool(query_string),
            'search_form': form,
            'collections': collections,
            'current_collection': current_collection,
            'user_can_add': permission_policy.user_has_permission(request.user, 'add'),
        })


@permission_checker.require('change')
def edit(request, reference_id):
    Reference = get_reference_model()
    ReferenceForm = get_reference_form(Reference, include_slug=True)

    reference = get_object_or_404(Reference, id=reference_id)

    if not permission_policy.user_has_permission_for_instance(request.user, 'change', reference):
        return permission_denied(request)

    if request.method == 'POST':
        form = ReferenceForm(request.POST, instance=reference, user=request.user)
        if form.is_valid():
            form.save()

            # Reindex the reference
            search_index.insert_or_update_object(reference)

            messages.success(request, _("Reference '{0}' updated.").format(reference.slug), buttons=[
                messages.button(reverse('wagtailreferences:edit', args=(reference.id,)), _('Edit again'))
            ])
            return redirect('wagtailreferences:index')
        else:
            messages.error(request, _("The reference could not be saved due to errors."))
    else:
        form = ReferenceForm(instance=reference, user=request.user)

    return render(request, "wagtail_references/references/edit.html", {
        'reference': reference,
        'form': form,
        'url_generator_enabled': False,
        'user_can_delete': permission_policy.user_has_permission_for_instance(
            request.user, 'delete', reference
        ),
    })


def preview(request, reference_id):
    reference = get_object_or_404(get_reference_model(), id=reference_id)
    response = HttpResponse(reference.bibtex)
    response['Content-Type'] = 'text/plain'
    return response


@permission_checker.require('delete')
def delete(request, reference_id):
    reference = get_object_or_404(get_reference_model(), id=reference_id)

    if not permission_policy.user_has_permission_for_instance(request.user, 'delete', reference):
        return permission_denied(request)

    if request.method == 'POST':
        reference.delete()
        messages.success(request, _("Reference '{0}' deleted.").format(reference.slug))
        return redirect('wagtailreferences:index')

    return render(request, "wagtail_references/references/confirm_delete.html", {
        'reference': reference,
    })


@permission_checker.require('add')
def add(request):
    Reference = get_reference_model()
    ReferenceForm = get_reference_form(Reference)

    if request.method == 'POST':
        reference = Reference(created_by_user=request.user)
        form = ReferenceForm(request.POST, request.FILES, instance=reference, user=request.user)
        if form.is_valid():
            form.save()

            # Reindex the image to make sure all tags are indexed
            search_index.insert_or_update_object(reference)

            messages.success(request, _("Reference '{0}' added.").format(reference.slug), buttons=[
                messages.button(reverse('wagtailreferences:edit', args=(reference.id,)), _('Edit'))
            ])
            return redirect('wagtailreferences:index')
        else:
            messages.error(request, _("The reference could not be created due to errors."))
    else:
        form = ReferenceForm(user=request.user)

    return render(request, "wagtail_references/references/add.html", {
        'form': form,
    })


def usage(request, image_id):
    reference = get_object_or_404(get_reference_model(), id=image_id)

    paginator, used_by = paginate(request, reference.get_usage())

    return render(request, "wagtail_references/references/usage.html", {
        'reference': reference,
        'used_by': used_by
    })
