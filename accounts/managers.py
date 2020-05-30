from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create a user with specific properties.
        :param email:
        :param username:
        :param password:
        :return: user
        """
        if not email:
            raise ValueError(_('The email must be set!'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be a staff.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be an active.'))
        return self.create_user(email, password, **extra_fields)
