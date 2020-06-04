from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_resized import ResizedImageField

from .managers import CustomUserManager


# Create your models here.

class CustomUser(AbstractUser):
    """
    Custom user model.
    """
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    image = ResizedImageField(size=[45, 45], quality=100, force_format='PNG', upload_to='avatars/', blank=True,
                              null=True, default='default-avatar.png')
    blocked = models.ManyToManyField('accounts.CustomUser')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username}'
