from django.conf.urls import patterns, url

from views import zufang, zufang_jyjx

urlpatterns = patterns('',
    url(r'^$', zufang, name='zufang'),
    url(r'^jyjx/$', zufang_jyjx, name='zufang_jyjx'),
)
