# coding: utf-8
import telepot
from django.utils import timezone
from django.utils.translation import ugettext_lazy 
#def _(x): return unicode(ugettext_lazy(x))
def _(x): return x
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

help_text=(_('Привет! Я Парковочный Бот. Я понимаю такие команды:\n\n') +
           _('/make - создать QR-код для вашей машины.\n') +
           _('/make xxx - создать QR-код, указав номер машины (можно не полностью). Это удобно, если у вас несколько машин.\n') +
           _('/ls - показать все QR-коды.\n') +
           _('/del id=XXX - удалить код id=XXX.\n') 
           )

def read_msg(msg = msg, bot = real_bot, host_name = "http://127.0.0.1:8000", _ = _):

    help_text = help_text + _('\nВы можете узнать больше на странице: ' + host_name)

    content_type, chat_type, chat_id = telepot.glance(msg)
    print "read_msg, " + str(chat_id) + ", " + str(content_type)
    if content_type != 'text':
        bot.sendMessage(chat_id, _('Извините, я понимаю только текст.'))
        return
    text = msg['text']    
    if text == '/make':                 # Create new code
        if Connection.objects.filter(telegram_id=chat_id).count() >=10:
            bot.sendMessage(chat_id, _('Извините, у вас зарегистрировано слишком много кодов.'))
            return
        new_connection = Connection(pin=randint(1000, 9999), telegram_id=chat_id, wait_till = timezone.now())
        new_connection.save()
        link = get_print_link( new_connection, host_name)
        bot.sendMessage(chat_id, _("Распечатайте свой QR-код: ") + link)
        return
    if text == '/ls':                   # List all 
        out_msg = _("Действующие QR-коды:\n")
        end_of_msg = _(" нет кодов.")
        for x in Connection.objects.filter(telegram_id=chat_id):
            end_of_msg = _(".")
            link = get_print_link( x, host_name)
            out_msg = out_msg + "id = " + str(x.id) + " [" + str(x.car_id) + "] " + link +"\n"
        bot.sendMessage(chat_id, out_msg + end_of_msg)
        return  
    if text == '/del_all':              # Delete all codes
        num, full_list = Connection.objects.filter(telegram_id=chat_id).delete()        
        bot.sendMessage(chat_id, 
                        "Удалено %d кодов. Вы больше не будете получать сообщения от них.\n/make - создаст новый код, это бесплатно." % num)
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
                bot.sendMessage(chat_id, _('Извините, я не могу найти этот id.'))
                return
            else:
                num, full_list = all_con.delete()
                bot.sendMessage(chat_id, 
                               "Удалён код id=%d. Вы больше не будете получать сообщения от него.\n/make - создаст новый код, это бесплатно." % id_)
            return
        except ValueError:
            bot.sendMessage(chat_id, _('Извините, я не понял, что вы сказали.'))
            pass
    if len(st) > 1 and st[1] == 'minute': # Answer, when user is going to come back to the car.  
        try:        
            num = int(st[0])
            all_con = Connection.objects.filter(telegram_id=chat_id)            
            if all_con.count() == 1:
                con = all_con[0]                
            elif len(st) ==2 :
                bot.sendMessage(chat_id, _('Извините, у вас несколько кодов, укажите конкретный id.'))
                return
            else: 
                id_ = int(st[2].split('=')[1])
                con = all_con.filter(id = id_)[0]            
            con.message = _("Скоро приду.")            
            con.wait_till = timezone.now() + timedelta(minutes = num)            
            con.save()            
            #bot.sendMessage(chat_id, _('I am hiding keyboard'), reply_markup={'hide_keyboard': True})
            return
        except ValueError:
            bot.sendMessage(chat_id, _('Извините, я не понял, что вы сказали.'))
            pass
    bot.sendMessage(chat_id, help_text)
