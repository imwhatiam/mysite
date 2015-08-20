from django.conf.urls import patterns, url

from views import zufang, export_excel

urlpatterns = patterns('',
    url(r'^$', zufang, name='zufang'),
    url(r'^export-excel/$', export_excel, name='export_excel'),
)
