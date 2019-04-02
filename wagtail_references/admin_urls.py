from django.conf.urls import url

from wagtail_references.views import references, chooser


app_name = 'wagtail_references'


urlpatterns = [
    url(r'^$', references.index, name='index'),
    url(r'^(\d+)/$', references.edit, name='edit'),
    url(r'^(\d+)/delete/$', references.delete, name='delete'),
    url(r'^(\d+)/preview/(.*)/$', references.preview, name='preview'),
    url(r'^add/$', references.add, name='add'),
    url(r'^usage/(\d+)/$', references.usage, name='reference_usage'),
    url(r'^chooser/$', chooser.chooser, name='chooser'),
    url(r'^chooser/(\d+)/$', chooser.reference_chosen, name='reference_chosen'),
]
