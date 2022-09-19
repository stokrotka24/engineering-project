from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from authorization.forms import CustomUserCreationForm, CustomUserChangeForm
from authorization.models import User


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('username', 'email', 'id', 'is_superuser')
    list_filter = ('is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'last_login', 'is_active')}),
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
    search_fields = ('username', 'email', 'id')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
