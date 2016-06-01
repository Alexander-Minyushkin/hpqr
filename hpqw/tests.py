from django.test import TestCase
import hpqw.bot_brain as brain
from hpqw.models import Connection
from hpqr.settings import LANGUAGES_SET
from django.utils.translation import ugettext_lazy
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
        
        brain.read_msg(test_msg, test_bot, test_host, lambda x: x)
        
        chat_id, msg = test_bot.result()
        
        self.assertEqual('hello' in msg.lower(), True)
        self.assertEqual(size_before, Connection.objects.all().count())
        
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
        self.assertEqual( brain.test_lang_ru_to_en_msg = , "Test from Russian to English")
        translation.activate(cur_language)
        
    def test_lang_ru_to_ru(self):
        """
        Verify translation from Russian to English
        """     
        cur_language = translation.get_language()
        translation.activate('ru')        
        self.assertEqual( brain.test_lang_ru_to_ru_msg = , "Тест с Русского на Русский")
        translation.activate(cur_language)
        
    def test_lang_en_to_en(self):
        """
        Verify translation from English to English
        """  
        cur_language = translation.get_language()
        translation.activate('en')        
        self.assertEqual( brain.test_lang_en_to_en_msg = , "Test from English to English")
        translation.activate(cur_language)
        
    def test_lang_en_to_ru(self):
        """
        Verify translation from English to Russian
        """     
        cur_language = translation.get_language()
        translation.activate('ru')        
        self.assertEqual( brain.test_lang_en_to_ru_msg = , "Тест с Английского на Русский")    
        translation.activate(cur_language)        