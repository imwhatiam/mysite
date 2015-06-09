from django.conf.urls import patterns, url

from views import ZufangItems, ZufangItem, ZufangAccessCount, \
    ZufangSearchContent

urlpatterns = patterns('',
    url(r'^zufang-items/$', ZufangItems.as_view()),
    url(r'^zufang-items/(?P<topic_id>\d+)/$', ZufangItem.as_view()),
    url(r'^zufang-access-count/$', ZufangAccessCount.as_view()),
    url(r'^zufang-search-content/$', ZufangSearchContent.as_view()),
)
