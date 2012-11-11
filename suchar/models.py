import base64
import hashlib
import random
from django.db import models

# Create your models here.
class Organisation(models.Model):
    name = models.CharField(max_length=128,db_index=True)
    api_key = models.CharField(max_length=128,db_index=True)
    creator_email = models.EmailField(db_index=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = base64.b64encode(hashlib.sha256( str(random.getrandbits(256)) ).digest(), random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('==')
        super(Organisation, self).save(*args, **kwargs)

class Participants(models.Model):
    organisation = models.ForeignKey(Organisation)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    gravatar = models.URLField()
    points = models.IntegerField(default=0)