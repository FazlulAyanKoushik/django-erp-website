from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from autoslug import AutoSlugField


# Create your models here.

class UserIncome(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ['-date']


class Source(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name
