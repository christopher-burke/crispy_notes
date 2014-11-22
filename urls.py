from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth.views import login
admin.autodiscover()

urlpatterns = patterns('crispy_notes.views',

    ### Home page URL
    url(r'^$','home',name='home'),

    ### Action on Notes
    url(r'action/$','action',name='action'),

    ### ADD Tag
    url(r'^add/tag/$','new_tag',name='new_tag'),

    ### ADD Note URLs
    url(r'^add/$','add',name='add'),

    ### Remove tag
    url(r'remove-tag/(?P<id>\d+)/$','remove_tags',name='remove_tags'),

    ### View URLs
    url(r'^(?P<id>\d+)/$', RedirectView.as_view(url='/view/%(id)s')),
    url(r'^view/tag/(?P<tag>\w+[-\w]*)/$','view_tag',name='view_tag'),
    url(r'^view/(?P<id>\w+)*$','view',name='view'),

    ### Edit Note URLs
    url(r'^edit/(?P<id>\w+)*$','edit_note',name='edit_note'),

    ### Tag URLs
    url(r'^tags/(?P<sortby>\d)$','tags',name='tags'),

    #LOGIN URLs
    url(r'^accounts/login/$', 'login_user'),
    url(r'^logout/$', 'logout_user'),


    #Reports
    url(r'^report/(\d{4})/$', 'report_year', name='report_year'),
    url(r'^report/(\d{4})/(\d{2})/$', 'report_month', name='report_month'),
    url(r'^report/(\d{4})/(\d{2})/(\d+)/$', 'report_day',name='report_day'),

    url(r'^root/','root'),

    #AJAX
    url(r'ajax/star/$', 'ajax.star'),
)


urlpatterns += patterns('',

    ### Search URLs
    url(r'^search/', include('haystack.urls')),

)
