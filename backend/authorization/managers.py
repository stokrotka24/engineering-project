from django.contrib.auth.base_user import BaseUserManager

from hotels.models import get_recommendations_for_new_user


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **other_attrs):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            password=password,
            **other_attrs)
        user.set_password(password)
        user.recommendations = get_recommendations_for_new_user()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **other_attrs):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            password=password,
            **other_attrs)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user
