from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def signal_post_save(sender, instance=None, created=False, **kwargs):
    pass
    # print('post ----')
    # print(instance.first_name)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def signal_re_save(sender, instance=None, created=False, **kwargs):
    pass