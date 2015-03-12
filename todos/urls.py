from django.conf.urls import patterns, url

from views import todos

urlpatterns = patterns('',
    url(r'^$', todos, name='todos'),
)
