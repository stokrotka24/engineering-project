from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import int_list_validator
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser):
    user_id = models.CharField(max_length=22, unique=True)
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=40, validators=[UnicodeUsernameValidator()])
    review_count = models.PositiveIntegerField(default=0)
    joined = models.DateTimeField(default=timezone.now)
    #TODO: add friends
    useful_votes = models.PositiveIntegerField(default=0)
    funny_votes = models.PositiveIntegerField(default=0)
    cool_votes = models.PositiveIntegerField(default=0)
    fans = models.PositiveIntegerField(default=0)
    elite = models.CharField(validators=int_list_validator)
    average_stars = models.DecimalField(default=2.5, decimal_places=2)
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

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [user_id, firstname]
