from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Game(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    object = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Score(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    value = models.BigIntegerField()
    assisted_flag = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
