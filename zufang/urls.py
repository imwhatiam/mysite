from django.conf.urls import patterns, url

from views import zufang

urlpatterns = patterns('',
    url(r'^$', zufang, name='zufang'),
)
