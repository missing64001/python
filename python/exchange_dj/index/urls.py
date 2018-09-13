from django.conf.urls import url
from .views import *

urlpatterns = [
    # url(r'^01_parent/$', parent_views),
    # url(r'^02_child/$', child_views),
    url(r'^market/$', market_views),
    url(r'^$', depth_views),
    url(r'^depth/$', depth_views),
    url(r'^depth/([_a-zA-Z]+)/$', depth_views),
]