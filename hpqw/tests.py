# coding: utf-8
from django.test import TestCase
import hpqw.bot_brain as brain
from hpqw.models import Connection, Language
from hpqr.settings import LANGUAGES_SET
from django.utils.translation import ugettext_lazy
def _(x): return unicode(ugettext_lazy(x))
from django.utils import translation

# Create your tests here.

class BotStab:
    chat_id = 0
    message = ""
    def sendMessage(self, id, m):
        self.chat_id = id
        self.message = m
        
    def result(self):
        return (self.chat_id, self.message)

class BotBrainTests(TestCase):

    def test_test_bot(self):
        """
        Verify empty test_bot
        """
        
        test_bot = BotStab()
        chat_id, msg = test_bot.result()
        
        self.assertEqual(chat_id, 0)
        self.assertEqual(msg, "")
        
    def test_answer_to_unrecoginzed_text(self):
        """
        Answer to unrecognizable message should contain 'Hello' - beginning of help message.
        No changes in Connection table should be made.
        """
        cur_language = translation.get_language()
        translation.activate('en')  
        
        test_bot = BotStab()
        test_host = 'test.host'
        
        size_before = Connection.objects.all().count()
        
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': u'Some_strange_text'}
                    
        brain.set_user_lang(200490867, 'en')
        
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        
        chat_id, msg = test_bot.result()
                
        self.assertEqual('hello' in msg.lower(), True)
        self.assertEqual(size_before, Connection.objects.all().count())
        
        translation.activate(cur_language) 
        
    def test_make_one(self):
        """
        Make one QR ID.
        Connection size should increase by one
        """
        test_bot = BotStab()
        test_host = 'test.host'
        
        size_before = Connection.objects.all().count()
        
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': u'/make'}
        
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        
        chat_id, msg = test_bot.result()
        
        self.assertEqual('print' in msg.lower(), True)
        self.assertEqual(size_before+1, Connection.objects.all().count())
        
        
    def test_make_two(self):
        """
        Make two QR ID.
        Connection size should increase by two
        """
        test_bot = BotStab()
        test_host = 'test.host'
        
        size_before = Connection.objects.all().count()
        
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': u'/make'}
        
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        chat_id, msg = test_bot.result()        
        self.assertEqual('print' in msg.lower(), True)
        self.assertEqual(size_before+1, Connection.objects.all().count())
        
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)        
        chat_id, msg = test_bot.result()        
        self.assertEqual('print' in msg.lower(), True)
        self.assertEqual(size_before+2, Connection.objects.all().count())
        
    def test_make_11(self):
        """
        Try to make 11 QR ID.
        Only 10 should be created
        """
        test_bot = BotStab()
        test_host = 'test.host'
        
        size_before = Connection.objects.all().count()
        
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': u'/make'}
        
        for i in range(10):
            brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
            chat_id, msg = test_bot.result()        
            self.assertEqual('print' in msg.lower(), True)
            self.assertEqual(size_before+1+i, Connection.objects.all().count())
            
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        chat_id, msg = test_bot.result()        
        self.assertEqual('sorry' in msg.lower(), True)
        self.assertEqual(size_before+10, Connection.objects.all().count())
            
    def test_wrong_content(self):
        """
        Non-text content should be answered with 'Sorry'
        Connection size should increase by one
        """
        test_bot = BotStab()
        test_host = 'test.host'
        
        size_before = Connection.objects.all().count()
        
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'document': u''}
                    
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        chat_id, msg = test_bot.result()        
        self.assertEqual('sorry' in msg.lower(), True)
        self.assertEqual(size_before, Connection.objects.all().count())
  
    def test_make_5_del_all(self):
        """
        Try to make 11 QR ID.
        Only 10 should be created
        """
        test_bot = BotStab()
        test_host = 'test.host'
        
        size_before = Connection.objects.all().count()
        
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': u'/make'}
        
        for i in range(5):
            brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
            chat_id, msg = test_bot.result()        
            self.assertEqual('print' in msg.lower(), True)
            self.assertEqual(size_before+1+i, Connection.objects.all().count())
            
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': u'/del_all'}            
            
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        chat_id, msg = test_bot.result()        
        self.assertEqual('removed 5 codes' in msg.lower(), True)
        self.assertEqual(size_before, Connection.objects.all().count())

    def test_del_not_your_id(self):
        """
        User may try to delete id which is owned by somebody else
        He should fail
        """
        test_bot = BotStab()
        test_host = 'test.host'
        
        size_before = Connection.objects.all().count()
        
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': u'/make'}
        
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        chat_id, msg = test_bot.result()     
        del_command = u'/del id=' + msg.split('/')[2].split('.')[0]
                
        self.assertEqual('print' in msg.lower(), True)
        self.assertEqual(size_before+1, Connection.objects.all().count())
        
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490866,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490866,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': u'/make'}
        
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        chat_id, msg = test_bot.result()  
        
        self.assertEqual('print' in msg.lower(), True)
        self.assertEqual(size_before+2, Connection.objects.all().count())
        
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490866,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490866,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': del_command}
        
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        chat_id, msg = test_bot.result()  
        self.assertEqual('sorry' in msg.lower(), True)        
        
#        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)        
#        chat_id, msg = test_bot.result()        
#        self.assertEqual('print' in msg.lower(), True)
#        self.assertEqual(size_before+2, Connection.objects.all().count())
        
    def test_lang_list(self):
        """
        Verify that English and Russian are in supported languages
        """
        
        self.assertEqual('ru' in LANGUAGES_SET, True)
        self.assertEqual('en' in LANGUAGES_SET, True)
        
    def test_lang_ru_to_en(self):
        """
        Verify translation from Russian to English
        """  
        cur_language = translation.get_language()
        translation.activate('en')        
        self.assertEqual( _(brain.test_lang_ru_to_en_msg), u"Test from Russian to English")
        translation.activate(cur_language)
        
    def test_lang_ru_to_ru(self):
        """
        Verify translation from Russian to English
        """     
        cur_language = translation.get_language()
        translation.activate('ru')        
        self.assertEqual( _(brain.test_lang_ru_to_ru_msg), u"Тест с Русского на Русский")
        translation.activate(cur_language)
        
    def test_lang_en_to_en(self):
        """
        Verify translation from English to English
        """  
        cur_language = translation.get_language()
        translation.activate('en')        
        self.assertEqual( _(brain.test_lang_en_to_en_msg), u"Test from English to English")
        translation.activate(cur_language)
        
    def test_lang_en_to_ru(self):
        """
        Verify translation from English to Russian
        """     
        cur_language = translation.get_language()
        translation.activate('ru')        
        self.assertEqual( _(brain.test_lang_en_to_ru_msg), u"Тест с Английского на Русский")    
        translation.activate(cur_language)  

    def test_default_user_lang(self):
        """
        Verify that default language is Russian
        """          
        self.assertEqual(brain.get_user_lang(1), 'ru')

    def test_updated_user_lang(self):
        """
        Verify that default language can be changed
        """          
        self.assertEqual(brain.get_user_lang(1), 'ru')
        brain.set_user_lang(1, 'en')
        self.assertEqual(brain.get_user_lang(1), 'en')

    def test_updated_1_user_lang(self):
        """
        Verify that language changed only for one user
        """          
        self.assertEqual(brain.get_user_lang(1), 'ru')
        self.assertEqual(brain.get_user_lang(2), 'ru')
        brain.set_user_lang(1, 'en')
        brain.set_user_lang(2, 'en')
        self.assertEqual(brain.get_user_lang(1), 'en')
        self.assertEqual(brain.get_user_lang(2), 'en')
        
        brain.set_user_lang(2, 'ru') # Changed only for one
        
        self.assertEqual(brain.get_user_lang(1), 'en') # This one stay the same
        self.assertEqual(brain.get_user_lang(2), 'ru') # This one changed
    
    def test_set_lang_via_brain(self):
        """
        Change language
        Language size should increase by one
        """
        test_bot = BotStab()
        test_host = 'test.host'
        
        size_before = Language.objects.all().count()
        
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': u'/lang_en'}
        
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        
        chat_id, msg = test_bot.result()
        
        self.assertEqual('better' in msg.lower(), True)
        self.assertEqual(size_before+1, Language.objects.all().count())

    def test_set_unsupported_lang_via_brain(self):
        """
        Try to change language to unsupported.
        Language size should not change
        """
        test_bot = BotStab()
        test_host = 'test.host'
        
        size_before = Language.objects.all().count()
        
        test_msg = {u'chat': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee',
                         u'type': u'private'},
               u'date': 1444723969,
               u'from': {u'first_name': u'Nick',
                         u'id': 200490867,
                         u'last_name': u'Lee'},
               u'message_id': 4015,
               u'text': u'/lang_never_support'}
        
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        
        chat_id, msg = test_bot.result()
        
        self.assertEqual('sorry' in msg.lower(), True)
        self.assertEqual(size_before, Language.objects.all().count())    