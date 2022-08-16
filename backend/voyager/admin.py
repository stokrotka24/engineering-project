from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django import forms

from voyager.models import User


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


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('username', 'email', 'id', 'is_superuser')
    list_filter = ('is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'id', 'last_login', 'is_active')}),
        ('Personal info', {'fields': (
            'date_joined', 'review_count', 'useful_votes', 'funny_votes',
            'cool_votes', 'fans', 'elite', 'average_stars',
            'compliment_hot', 'compliment_more', 'compliment_profile', 'compliment_cute',
            'compliment_list', 'compliment_note', 'compliment_plain', 'compliment_cool',
            'compliment_funny', 'compliment_writer', 'compliment_photos')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password'),
        }),
    )
    search_fields = ('username', 'email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
