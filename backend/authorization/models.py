from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.validators import int_list_validator
from djongo import models
from authorization.managers import UserManager
from hotels.models import Recommendation


class User(AbstractUser):
    username = models.CharField(max_length=32, unique=False)
    email = models.EmailField(max_length=64, unique=True)
    id = models.AutoField(unique=True, primary_key=True)
    review_count = models.PositiveIntegerField(default=0)
    # TODO: add friends
    useful_votes = models.PositiveIntegerField(default=0)
    funny_votes = models.PositiveIntegerField(default=0)
    cool_votes = models.PositiveIntegerField(default=0)
    fans = models.PositiveIntegerField(default=0)
    elite = models.CharField(max_length=100, validators=[int_list_validator])
    average_stars = models.DecimalField(
        default=0.0,
        max_digits=3,
        decimal_places=2
    )
    compliment_hot = models.PositiveIntegerField(default=0)
    compliment_more = models.PositiveIntegerField(default=0)
    compliment_profile = models.PositiveIntegerField(default=0)
    compliment_cute = models.PositiveIntegerField(default=0)
    compliment_list = models.PositiveIntegerField(default=0)
    compliment_note = models.PositiveIntegerField(default=0)
    compliment_plain = models.PositiveIntegerField(default=0)
    compliment_cool = models.PositiveIntegerField(default=0)
    compliment_funny = models.PositiveIntegerField(default=0)
    compliment_writer = models.PositiveIntegerField(default=0)
    compliment_photos = models.PositiveIntegerField(default=0)
    recommendations = models.ArrayField(
        model_container=Recommendation,
    )

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # list of the field names that will be prompted for when creating a user via the createsuperuser
    REQUIRED_FIELDS = ['username', ]
