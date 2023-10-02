from django.conf.urls import url

from projects.views import add_contributor
from projects.views import CreateClass
from projects.views import delete_contributor
from projects.views import edit
from projects.views import ListClass
from projects.views import ListContributorsClass
from projects.views import ListMyProjectsClass
from projects.views import ShowClass
from projects.views import user_contributor

app_name = 'project'

urlpatterns = [
    url(r'^$', ListClass.as_view(), name = 'projects'),
    url(r'^mine/$', ListMyProjectsClass.as_view(), name = 'my_projects'),
    url(r'^create/$', CreateClass.as_view(), name = 'create'),
    url(r'^(?P<slug>[\w-]+)/$', ShowClass.as_view(), name = 'show'),
    url(r'^(?P<slug>[\w-]+)/edit/$', edit, name = 'edit'),
    url(r'^(?P<slug>[\w-]+)/contributors/$', ListContributorsClass.as_view(), name = 'contributors'),
    url(r'^(?P<slug>[\w-]+)/contributors/add/(?P<username>[\w-]+)/$', add_contributor, name = 'add_contributor'),
    url(r'^(?P<slug>[\w-]+)/contributors/(?P<username>[\w-]+)/$', user_contributor, name = 'user_contributor'),
    url(r'^(?P<slug>[\w-]+)/contributors/delete/(?P<username>[\w-]+)/$', delete_contributor, name = 'delete_contributor'),
]
