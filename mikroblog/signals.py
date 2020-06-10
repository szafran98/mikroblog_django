from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse

from accounts.models import CustomUser
from mikroblog.models import Post, TalkAbout


@receiver(post_save, sender=Post)
def create_notifications(instance, created, **kwargs):
    for word in instance.content_post.split():
        if '@' in word:
            try:
                if created:
                    user_to_notificate = CustomUser.objects.get(username=word[1:])
                    TalkAbout(where=instance, _from=instance.author, to=user_to_notificate).save()
            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse('index'))
