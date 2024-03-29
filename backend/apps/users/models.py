from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from apps.cinema.models import Genre, Building


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(('Users must have an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a Superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email',
                              unique=True, max_length=255)

    # define user model fields here
    password_reset_token = models.CharField(
        verbose_name='Password reset token', max_length=255, blank=True, null=True)
    favourite_genres = models.ManyToManyField(
        Genre, verbose_name='Favourite genres', blank=True)
    favourite_cinemas = models.ManyToManyField(
        Building, verbose_name='Favourite Cinemas', blank=True)

    is_admin = models.BooleanField(verbose_name='Admin', default=False)
    is_staff = models.BooleanField(verbose_name='Staff', default=False)
    is_active = models.BooleanField(verbose_name='Active', default=True)
    registered_at = models.DateTimeField(
        verbose_name='Registered at', default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # define properties which can be used in serializers based on fields here
    def has_perm(self, perm, obj=None):

        return True

    def has_module_perms(self, app_label):

        return True

    def __str__(self):
        return self.email
