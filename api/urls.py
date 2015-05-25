from django.conf.urls import patterns, url

from views import ZufangItems, ZufangAccessCount

urlpatterns = patterns('',
    url(r'^zufang-items/$', ZufangItems.as_view()),
    url(r'^zufang-access-count/$', ZufangAccessCount.as_view()),
)
