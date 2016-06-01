from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Connection(models.Model):
    pin	= models.IntegerField()
    telegram_id	= models.IntegerField(db_index=True)
    telegram_status = models.IntegerField(default=0)
    wait_till = models.DateTimeField()
    car_id = models.CharField(max_length=20)
    message = models.CharField(max_length=200)

    def __unicode__(self):              # __unicode__ on Python 2
        return str(self.id) + " pin=" + str(self.pin) +" telegram_id=" + str(self.telegram_id )

        
class Language(models.Model):
    telegram_id	= models.IntegerField(db_index=True)
    prefix = models.CharField(max_length=10, default='ru')