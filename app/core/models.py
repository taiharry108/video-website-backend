from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Show(models.Model):
    """Show model"""
    name = models.CharField(max_length=255)
    last_update = models.DateField()
    num_seasons = models.IntegerField()
    num_eps = models.IntegerField()
    thum_img_url = models.CharField(max_length=255)
    banner_img_url = models.CharField(max_length=255, blank=True)
    rating = models.FloatField()
    is_finished = models.BooleanField()

    def __str__(self):
        return f"{self.name}:[{self.num_seasons}][{self.num_eps}]"


class FeaturedShow(models.Model):
    """Featured show model"""
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE
    )
    header = models.CharField(max_length=255)
    subheader = models.CharField(max_length=255)


class Season(models.Model):
    """Season for a show"""
    name = models.CharField(max_length=255)
    last_update = models.DateField()
    num_eps = models.IntegerField()
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.show.name} - {self.name} [{self.num_eps}]"


class Ep(models.Model):
    """Ep of a season"""
    name = models.CharField(max_length=255)
    last_update = models.DateField()
    idx = models.IntegerField()
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE
    )
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.show.name} - {self.season.name} [{self.name}]"
