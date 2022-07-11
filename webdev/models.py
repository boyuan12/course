from django.db import models
from django.conf import settings

# Create your models here.
class Attempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = models.JSONField()
    pset = models.IntegerField()
    time = models.DateTimeField(auto_created=True, auto_now=True)