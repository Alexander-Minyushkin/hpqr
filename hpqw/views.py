# coding: utf-8
from django.shortcuts import render

from django.shortcuts import render
#from django.utils.translation import ugettext_lazy as _
def _(x): return x
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta

from hpqw.models import Connection
from hpqr.settings import bot
import hpqw.bot_brain as brain

# Create your views here.
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST"])
def telegram_hook(request):
    brain.read_msg(request.POST, bot, request.META['HTTP_HOST'])
    return HttpResponse('hook' + str(request.POST))

def index(request):   
    return render(request, 'index.html')
    
def register(request):   
    return render(request, 'register.html')
    
def credits(request):   
    return render(request, 'credits.html')
    
def contact(request):   
    return render(request, 'contact.html')
    
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
    
    message_link = request.META['HTTP_HOST'] +"/" + id + "." + pin
    return render(request, 'print.html', {'message_link':message_link})
    
def connection(request, id, pin):  
    check_inputs(id, pin)
    con = Connection.objects.get(id=id)
    
    if timezone.now() > con.wait_till: # This is small spam protection
        con.message = ""
        con.wait_till = timezone.now() + timedelta(minutes = 1)  
        con.save()
        
        car_id = ""
        if con.car_id != "":
            car_id = " [%s]." % con.car_id
            
        specific = " id=" + str(con.id) + car_id 
        show_keyboard = {'keyboard': [['1 minute'+specific,'2 minute'+specific], ['5 minute'+specific,'60 minute'+specific + ' (block spam)']]}
        bot.sendMessage(con.telegram_id, _("Somebody calling you to your car") + car_id , reply_markup=show_keyboard)
    
    reply_message = con.message       
    reply_time = (con.wait_till - timezone.now()).seconds     
    #return HttpResponse("Good!: " + id + " -> " + pin)
    return render(request, 'connection.html', {'id':id, 'pin':pin, 'reply_message':reply_message, 'reply_time':reply_time})
  

