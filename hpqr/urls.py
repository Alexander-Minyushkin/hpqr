from django.conf.urls import include, url
from django.contrib import admin
from hpqw import views

from hpqr.settings import bot_token

urlpatterns = [
    # Examples:
    # url(r'^$', 'hpqr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(bot_token, views.telegram_hook),
    url(r'^$', views.index),    
    url(r'^([0-9]+)\.([0-9]{4})', views.connection),        
    url(r'^print/([0-9]+)\.([0-9]{4})', views.print_page),
    url(r'^register$', views.register),
    url(r'^credits$', views.credits),
    url(r'^contact$', views.contact),
    url(r'^index$', views.index),
    url(r'^robots\.txt$', views.robots),
    #url(r'^admin/', include(admin.site.urls)),
]
