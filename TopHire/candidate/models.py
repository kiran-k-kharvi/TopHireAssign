from django.db import models


# Create your models here.


class Resume(models.Model):
    name = models.CharField(max_length=256)
    text = models.CharField(max_length=2000)
