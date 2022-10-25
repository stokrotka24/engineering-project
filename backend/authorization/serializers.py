from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from authorization.models import User


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    password_confirmation = serializers.CharField(
        required=True,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"password": "Both password fields should be the same."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password])
    password_confirmation = serializers.CharField(
        required=True,
        write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password_confirmation')

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect")
        return old_password

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"password": "Both password fields should be the same."})

        return attrs

    def update(self, user, validated_data):
        user.set_password(validated_data['password'])
        user.average_stars = float(str(user.average_stars))
        user.save()

        return user





