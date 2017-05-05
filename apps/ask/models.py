from django.db import models
from apps.authentication.models import User



class Tag(models.Model):
    tag = models.CharField(max_length=250, blank=False, unique=True)

    def __str__(self):
        return self.tag


class Ask(models.Model):
    text = models.TextField(blank=False)
    user =  models.ForeignKey(User, related_name="asks", blank=False)
    tags = models.ManyToManyField(Tag, through='Asktag')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Asktag(models.Model):
    ask = models.ForeignKey(Ask, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
