from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from authorization.models import User


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        # doesn't work in admin files
        fields = UserCreationForm.Meta.fields

    # analogical to save() in UserCreationForm
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        # doesn't work in admin files
        fields = UserChangeForm.Meta.fields
