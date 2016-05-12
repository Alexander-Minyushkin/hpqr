from django.conf.urls import include, url
from django.contrib import admin
from hpqw import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'hpqr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index),
    url(r'^([0-9]+)\.([0-9]{4})', views.connection),        
    url(r'^print/([0-9]+)\.([0-9]{4})', views.print_page),
    url(r'^register$', views.register),
    url(r'^credits$', views.credits),
    url(r'^contact$', views.contact),
    url(r'^admin/', include(admin.site.urls)),
]
