from django.conf.urls import url

from clients.views import CreateView
from clients.views import DashboardView
from clients.views import edit_password
from clients.views import EditSocialClass
from clients.views import LoginView
from clients.views import logout
from clients.views import ShowView
from clients.views import edit
from clients.views import user_filter

#es un identificador por si en otros modulos nombramos las url de forma igual
app_name = 'client'

urlpatterns = [
    #url(r'^show/(?P<pk>\d+)/$', views.ShowView.as_view(), name = 'show'),
    url(r'^show/(?P<username_url>\w+)/$', ShowView.as_view(), name = 'show'),
    url(r'^login/$', LoginView.as_view(), name = 'login'),
    url(r'^logout/$', logout, name = 'logout'),
    url(r'^dashboard/$', DashboardView.as_view(), name = 'dashboard'),
    url(r'^create/$', CreateView.as_view(), name = 'create'),

    url(r'^edit/$', edit, name = 'edit'),
    url(r'^edit/password/$', edit_password, name = 'edit_password'),
    url(r'^edit/social/$', EditSocialClass.as_view(), name = 'edit_social'),

    url(r'^filter$', user_filter, name = 'filter')
]
