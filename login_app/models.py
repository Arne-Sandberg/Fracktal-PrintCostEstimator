from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone_no = models.IntegerField(default=0)
    user_website = models.URLField(default='')