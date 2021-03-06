# coding: utf-8
from django.shortcuts import render

from django.shortcuts import render
from django.utils.translation import ugettext, ugettext_lazy 
def _(x): return unicode(ugettext(x))
#def _(x): return unicode(x)
from django.utils import translation
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.gzip import gzip_page
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from datetime import timedelta
import json

from hpqw.models import Connection
from hpqr.settings import bot
from hpqr.settings import HPQR_HOST
from hpqr.settings import HPQR_YANDEX_METRIKA
import hpqw.bot_brain as brain

# Create your views here.


@csrf_exempt
@require_http_methods(["POST"])
def telegram_hook(request):     
    try:
        brain.read_msg(json.loads(request.body)['message'], bot, HPQR_HOST)
    finally:
        pass
    return HttpResponse('hook')
    
@gzip_page
def index(request):   
    return render(request, 'index.html', {'bot_getMe':bot.getMe(),
                                          'HPQR_HOST':HPQR_HOST,
                                          'HPQR_YANDEX_METRIKA' : HPQR_YANDEX_METRIKA})

def robots(request):   
    return render(request, 'robots.txt')

@gzip_page    
def register(request):   
    return render(request, 'register.html', 
                  {'bot_getMe':bot.getMe(),
                   'HPQR_HOST':HPQR_HOST,
                   'HPQR_YANDEX_METRIKA' : HPQR_YANDEX_METRIKA})
 
@gzip_page 
def credits(request):   
    return render(request, 'credits.html', {'HPQR_HOST':HPQR_HOST, 'HPQR_YANDEX_METRIKA' : HPQR_YANDEX_METRIKA})

@gzip_page    
def contact(request):   
    return render(request, 'contact.html', {'HPQR_HOST':HPQR_HOST, 'HPQR_YANDEX_METRIKA' : HPQR_YANDEX_METRIKA})
    
def check_inputs(id, pin):
    try:
        obj = Connection.objects.get( id = int(id) )
    except ObjectDoesNotExist:
        #return HttpResponse("DoesNotExist id " + id)
        raise Http404(_("ID does not exist"))
    
    if int(pin) != obj.pin:
        #return HttpResponse("Wrong pin " + pin)
        raise Http404(_("Wrong pin"))

        
def print_page(request, id, pin): 
    check_inputs(id, pin)
    
    con = Connection.objects.get(id=id)
    translation.activate(brain.get_user_lang(con.telegram_id)) # Optimization is possible using join
    
    message_link = HPQR_HOST +"/" + id + "." + pin    
    return render(request, 'print.html', {'message_link':message_link, 'HPQR_YANDEX_METRIKA' : HPQR_YANDEX_METRIKA})
 
@gzip_page 
def connection(request, id, pin):  
    check_inputs(id, pin)
    con = Connection.objects.get(id=id)
        
    if timezone.now() > con.wait_till: # This is small spam protection
        cur_language = translation.get_language()
        try:
            translation.activate(brain.get_user_lang(con.telegram_id)) # Optimization is possible using join
    
            con.message = ""
            con.wait_till = timezone.now() + timedelta(minutes = 1)  
            con.save()
        
            car_id = u""
            if con.car_id != u"":
                car_id = u" [%s]." % con.car_id
            
            specific = u" id=" + unicode(str(con.id)) + car_id 
            show_keyboard = {'keyboard': [[u'2 minute'+specific,u'5 minute'+specific], [u'10 minute'+specific,u'60 minute'+specific + u' (block spam)']]}
            bot.sendMessage(con.telegram_id, 
                        _(u"Кто-то ожидает вас у машины ") + specific + _(u". Когда вы подойдёте?") , 
                        reply_markup=show_keyboard)
        finally:
            translation.activate(cur_language)    
    
    reply_message = _(con.message)           
    reply_time = (con.wait_till - timezone.now()).seconds
    #return HttpResponse("Good!: " + id + " -> " + pin)
    return render(request, 'connection.html', 
                  {'id':id, 'pin':pin, 'reply_message':reply_message, 'reply_time':reply_time, 'HPQR_HOST':HPQR_HOST, 'HPQR_YANDEX_METRIKA' : HPQR_YANDEX_METRIKA})
  
def bad_request(request): 
    response = render(request, '404.html', {'HPQR_HOST':HPQR_HOST, 'HPQR_YANDEX_METRIKA' : HPQR_YANDEX_METRIKA})
    response.status_code = 404
    return response

