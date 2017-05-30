from django.db import models
from apps.authentication.models import User
from apps.ask.models import Ask

from apps.core.fields import FileField


class Spitch(models.Model):
    user = models.ForeignKey(User, related_name="spitchs")
    ask = models.ForeignKey(Ask, related_name="spitchs")
    spitch = FileField(null=True)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)