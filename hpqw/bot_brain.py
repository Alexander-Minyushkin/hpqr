# coding: utf-8
import telepot
from django.utils import timezone
from django.utils.translation import ugettext_lazy 
def _(x): return unicode(ugettext_lazy(x))
from django.utils import translation
#def _(x): return ugettext_lazy(x)
#def _(x): return x
from datetime import timedelta
from random import randint
from hpqw.models import Connection, Language
from hpqr.settings import bot as real_bot
from hpqr.settings import LANGUAGES_SET


msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': u'/ls'}

#msg = bot.getUpdates()[-1]['message']

def get_print_link(con, host_name):
    return host_name + "/print/" + str(con.id) + "." + str(con.pin)

test_lang_ru_to_en_msg = _(u"Тест с Русского на Английский")
test_lang_ru_to_ru_msg = _(u"Тест с Русского на Русский")
test_lang_en_to_en_msg = _(u"Test from English to English")
test_lang_en_to_ru_msg = _(u"Test from English to Russian")

help_text=(_('Hello! I am Hot Parking Bot. I understand commands:\n\n') +
           _('/make - create QR-code for your car.\n') +
           _('/make xxx - create QR code with car plate number (incomplete is OK). It is convenient if you have several cars.\n') +
           _('/ls - list all active QR-codes.\n') +
           _('/del id=XXX - delete code with id=XXX.\n') 
           )
           
def get_user_lang(chat_id):
    x = Language.objects.filter(telegram_id=chat_id)
    if (len(x) == 1):
        return x[0].prefix        
    return 'ru'
    
def set_user_lang(chat_id, lang):
    obj, created = Language.objects.update_or_create(telegram_id=chat_id, prefix = lang)
    pass

def read_msg(msg = msg, bot = real_bot, host_name = "http://127.0.0.1:8000", _ = _):

    content_type, chat_type, chat_id = telepot.glance(msg)
    print "read_msg, " + str(chat_id) + ", " + str(content_type)
    
    translation.activate(get_user_lang(chat_id))
    
    if content_type != 'text':
        bot.sendMessage(chat_id, _('Sorry, I understand only text.'))
        return
    text = msg['text']  
    if text.startswith("/lang_"):
        lang = text[6:]
        if lang not in LANGUAGES_SET:
            bot.sendMessage(chat_id, _("Sorry, we don't support this language."))
            return
        
        set_user_lang(chat_id, lang)
        translation.activate(get_user_lang(chat_id))
        bot.sendMessage(chat_id, _("Now it's better."))
        return
    
    if text == '/make':                 # Create new code
        if Connection.objects.filter(telegram_id=chat_id).count() >=10:
            bot.sendMessage(chat_id, _('Sorry, you have too many registred codes.'))
            return
        new_connection = Connection(pin=randint(1000, 9999), telegram_id=chat_id, wait_till = timezone.now())
        new_connection.save()
        link = get_print_link( new_connection, host_name)
        bot.sendMessage(chat_id, _("Print your QR-code: ") + link)
        return
    if text == '/ls':                   # List all 
        out_msg = _("Active QR-codes:\n")
        end_of_msg = _("no codes.")
        for x in Connection.objects.filter(telegram_id=chat_id):
            end_of_msg = _(" ")
            link = get_print_link( x, host_name)
            out_msg = out_msg + "id = " + str(x.id) + " [" + str(x.car_id) + "] " + link +"\n"
        bot.sendMessage(chat_id, out_msg + end_of_msg)
        return  
    if text == '/del_all':              # Delete all codes
        num, full_list = Connection.objects.filter(telegram_id=chat_id).delete()        
        bot.sendMessage(chat_id, 
                        "Removed %d codes. You will have no more messages from them.\nYou can /make new code. It is free." % num)
        return               
    st = text.split()
    if len(st) > 1 and st[0] == '/make': # Make QR-code with car_id
        car_id = text[len(text.split()[0]):].strip()
        if len(car_id) > 20: car_id = car_id[:20]
        new_connection = Connection(pin=randint(1000, 9999), telegram_id=chat_id, wait_till = timezone.now(), car_id=car_id)
        new_connection.save()
        link = get_print_link( new_connection, host_name)
        bot.sendMessage(chat_id, _("Print your QR-code: ") + link)
        return 
    if len(st) > 1 and st[0] == '/del':
        try: 
            id_ = int(st[1].split('=')[1]) 
            all_con = Connection.objects.filter(id = id_).filter(telegram_id=chat_id)
            if all_con.count() != 1:
                bot.sendMessage(chat_id, _('Sorry, I can not find this id.'))
                return
            else:
                num, full_list = all_con.delete()
                bot.sendMessage(chat_id, 
                               "Removed code with id=%d. There will be no more messages from it. \nYou can /make new code. It is free." % id_)
            return
        except ValueError:
            bot.sendMessage(chat_id, _('Sorry, I did not understand what you said.'))
            pass
    if len(st) > 1 and st[1] == 'minute': # Answer, when user is going to come back to the car.  
        try:        
            num = int(st[0])
            all_con = Connection.objects.filter(telegram_id=chat_id)            
            if all_con.count() == 1:
                con = all_con[0]                
            elif len(st) ==2 :
                bot.sendMessage(chat_id, _('Sorry, you have many codes. Provide particular id.'))
                return
            else: 
                id_ = int(st[2].split('=')[1])
                con = all_con.filter(id = id_)[0]            
            con.message = _("Will come back soon.")            
            con.wait_till = timezone.now() + timedelta(minutes = num)            
            con.save()            
            #bot.sendMessage(chat_id, _('I am hiding keyboard'), reply_markup={'hide_keyboard': True})
            return
        except ValueError:
            bot.sendMessage(chat_id, _('Sorry, I did not understand what you said.'))
            pass

    
    bot.sendMessage(chat_id, help_text + _('\nYou can read more here: ' + host_name))

