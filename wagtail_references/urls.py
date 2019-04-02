
from django.conf.urls import url

from references.views.serve import serve

urlpatterns = [
    url(r'^([^/]*)/(\d*)/([^/]*)/[^/]*$', serve, name='wagtailreferences_serve'),
]
