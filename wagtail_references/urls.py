
from django.conf.urls import url

from wagtail_references.views.serve import serve

urlpatterns = [
    url(r'^([^/]*)/(\d*)/([^/]*)/[^/]*$', serve, name='wagtailreferences_serve'),
]
