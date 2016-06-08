from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from hpqw import views
from django.conf.urls import handler400

from hpqr.settings import bot_token

urlpatterns = [
    url(bot_token, views.telegram_hook),
    url(r'^robots\.txt$', views.robots),
    #url(r'^admin/', include(admin.site.urls)),
    ]

urlpatterns += i18n_patterns( 
    url(r'^$', views.index),  
    url(r'^/$', views.index),   
    url(r'^([0-9]+)\.([0-9]{4})', views.connection),        
    url(r'^print/([0-9]+)\.([0-9]{4})', views.print_page),
    url(r'^register$', views.register),
    url(r'^credits$', views.credits),
    url(r'^contact$', views.contact),
    url(r'^index$', views.index)
    )
    


handler400 = 'hpqw.views.bad_request'
