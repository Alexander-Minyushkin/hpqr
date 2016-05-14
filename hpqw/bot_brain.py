# coding: utf-8
import telepot
from django.utils import timezone
from django.utils.translation import ugettext_lazy 
#def ugettext_lazy(x): return x
from datetime import timedelta
from random import randint
from hpqw.models import Connection
from hpqr.settings import bot as real_bot


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


def read_msg(msg = msg, bot = real_bot, host_name = "http://127.0.0.1:8000", ugettext_lazy = ugettext_lazy):
    help_text = (ugettext_lazy('Hello! I am Hot Parking Bot. I can understand commands:') + '\n\n' +
                ugettext_lazy('/make - create QR code for your car') + '\n' +
                ugettext_lazy('/make xxx - create QR code with car plate number (incomplete is OK). It is convenient if you have several cars.') +'\n' +
                ugettext_lazy('/ls   - list all active QR-codes') +'\n' +
                ugettext_lazy('/del_all - delete all codes.')+'\n' +
                ugettext_lazy('/del id=XXX - delete code with id=XXX.')+'\n'
                )
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        bot.sendMessage(chat_id, ugettext_lazy('Sorry, I understand only text'))
        return
    text = msg['text']    
    if text == '/make':                 # Create new code
        if Connection.objects.filter(telegram_id=chat_id).count() >=10:
            bot.sendMessage(chat_id, ugettext_lazy('Sorry, you have too many registred codes.'))
            return
        new_connection = Connection(pin=randint(1000, 9999), telegram_id=chat_id, wait_till = timezone.now())
        new_connection.save()
        link = get_print_link( new_connection, host_name)
        bot.sendMessage(chat_id, ugettext_lazy("Print your QR-code: ") + link)
        return
    if text == '/ls':                   # List all 
        out_msg = ugettext_lazy("Active QR-codes:") + "\n"
        for x in Connection.objects.filter(telegram_id=chat_id):
            link = get_print_link( x, host_name)
            out_msg = out_msg + "id = " + str(x.id) + " [" + str(x.car_id) + "] " + link +"\n"
        bot.sendMessage(chat_id, out_msg)
        return  
    if text == '/del_all':              # Delete all codes
        num, full_list = Connection.objects.filter(telegram_id=chat_id).delete()        
        bot.sendMessage(chat_id, "Removed %d codes. There will be no more messages from them. You can /make new code." % num)
        return               
    st = text.split()
    if len(st) > 1 and st[0] == '/make': # Make QR-code with car_id
        car_id = text[len(text.split()[0]):].strip()
        if len(car_id) > 20: car_id = car_id[:20]
        new_connection = Connection(pin=randint(1000, 9999), telegram_id=chat_id, wait_till = timezone.now(), car_id=car_id)
        new_connection.save()
        link = get_print_link( new_connection, host_name)
        bot.sendMessage(chat_id, ugettext_lazy("Print your QR-code: ") + link)
        return 
    if len(st) > 1 and st[0] == '/del':
        try: 
            id_ = int(st[1].split('=')[1]) 
            all_con = Connection.objects.filter(id = id_).filter(telegram_id=chat_id)
            if all_con.count() != 1:
                bot.sendMessage(chat_id, ugettext_lazy('Sorry, I can not find this id.'))
                return
            else:
                num, full_list = all_con.delete()
                bot.sendMessage(chat_id, "Removed code with id=%d. There will be no more messages from it. You can /make new code." % id_)
            return
        except ValueError:
            bot.sendMessage(chat_id, ugettext_lazy('Sorry, I did not understand what you said.'))
            pass
    if len(st) > 1 and st[1] == 'minute': # Answer, when user is going to come back to the car.  
        try:        
            num = int(st[0])
            all_con = Connection.objects.filter(telegram_id=chat_id)            
            if all_con.count() == 1:
                con = all_con[0]                
            elif len(st) ==2 :
                bot.sendMessage(chat_id, ugettext_lazy('Sorry, you have many codes. Provide particular id.'))
                return
            else: 
                id_ = int(st[2].split('=')[1])
                con = all_con.filter(id = id_)[0]            
            con.message = ugettext_lazy("Will come back soon")            
            con.wait_till = timezone.now() + timedelta(minutes = num)            
            con.save()            
            #bot.sendMessage(chat_id, ugettext_lazy('I am hiding keyboard'), reply_markup={'hide_keyboard': True})
            return
        except ValueError:
            bot.sendMessage(chat_id, ugettext_lazy('Sorry, I did not understand what you said.'))
            pass
    bot.sendMessage(chat_id, help_text)
