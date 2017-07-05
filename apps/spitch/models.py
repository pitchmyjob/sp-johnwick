from django.db import models
from apps.authentication.models import User
from apps.ask.models import Ask

from apps.core.fields import FileField, ImageField



class Spitch(models.Model):

    COLOR_SPITCH = (
        (1, 'Violet'),
        (2, 'Orange'),
        (3, 'Rouge'),
        (4, 'Vert'),
        (5, 'Rose'),
        (6, 'Bleu')
    )

    user = models.ForeignKey(User, related_name="spitchs")
    ask = models.ForeignKey(Ask, related_name="spitchs")
    color = models.IntegerField(choices=COLOR_SPITCH, default=1)

    video = FileField(null=True)
    spitch = FileField(null=True)
    photo = ImageField(null=True)
    thumb = ImageField(null=True)

    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']



class Like(models.Model):
    spitch = models.ForeignKey(Spitch, related_name="likes")
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('spitch', 'user')