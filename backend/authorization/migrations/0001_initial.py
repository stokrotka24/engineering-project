# Generated by Django 3.1.12 on 2022-09-02 10:28

import common.utils.id
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=64, unique=True)),
                ('id', models.CharField(default=common.utils.id.random_id, max_length=22, primary_key=True, serialize=False, unique=True)),
                ('review_count', models.PositiveIntegerField(default=0)),
                ('useful_votes', models.PositiveIntegerField(default=0)),
                ('funny_votes', models.PositiveIntegerField(default=0)),
                ('cool_votes', models.PositiveIntegerField(default=0)),
                ('fans', models.PositiveIntegerField(default=0)),
                ('elite', models.CharField(max_length=100, validators=[django.core.validators.int_list_validator])),
                ('average_stars', models.DecimalField(decimal_places=2, default=2.5, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('compliment_hot', models.PositiveIntegerField(default=0)),
                ('compliment_more', models.PositiveIntegerField(default=0)),
                ('compliment_profile', models.PositiveIntegerField(default=0)),
                ('compliment_cute', models.PositiveIntegerField(default=0)),
                ('compliment_list', models.PositiveIntegerField(default=0)),
                ('compliment_note', models.PositiveIntegerField(default=0)),
                ('compliment_plain', models.PositiveIntegerField(default=0)),
                ('compliment_cool', models.PositiveIntegerField(default=0)),
                ('compliment_funny', models.PositiveIntegerField(default=0)),
                ('compliment_writer', models.PositiveIntegerField(default=0)),
                ('compliment_photos', models.PositiveIntegerField(default=0)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
