import base64
import hashlib
import hmac

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_text
from django.views.generic import View

from wagtail_references import get_reference_model


def generate_signature(reference_id, filter_spec, key=None):
    if key is None:
        key = settings.SECRET_KEY

    # Key must be a bytes object
    if isinstance(key, str):
        key = key.encode()

    # Based on libthumbor hmac generation
    # https://github.com/thumbor/libthumbor/blob/b19dc58cf84787e08c8e397ab322e86268bb4345/libthumbor/crypto.py#L50
    url = '{}/{}/'.format(reference_id, filter_spec)
    return force_text(base64.urlsafe_b64encode(hmac.new(key, url.encode(), hashlib.sha1).digest()))


def verify_signature(signature, reference_id, filter_spec, key=None):
    return force_text(signature) == generate_signature(reference_id, filter_spec, key=key)


def generate_reference_url(reference, filter_spec, viewname='wagtailreferences_serve', key=None):
    signature = generate_signature(reference.id, filter_spec, key)
    url = reverse(viewname, args=(signature, reference.id, filter_spec))
    url += reference.file.name[len('original_references/'):]
    return url


class ServeView(View):
    model = get_reference_model()
    key = None

    def get(self, request, reference_id):

        reference = get_object_or_404(self.model, id=reference_id)

        return HttpResponse(reference.bibtex, content_type='text/plain')


serve = ServeView.as_view()
