from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User
from apps.users.forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # fields on admin page
    list_display = ['email', 'is_superuser']
    fieldsets = [
        ['Auth', {'fields': ['email', 'password', 'password_reset_token']}],
        ['Personal info', {'fields': [
            'favourite_genres', 'favourite_cinemas']}],
        ['Permissions', {'fields': ['is_admin',
                                    'is_active', 'is_staff', 'is_superuser']}],
        ['Important dates', {'fields': ['last_login', 'registered_at']}],
    ]

    # define fields when adding user on admin page
    add_fieldsets = [
        [None, {'classes': ['wide'],
                'fields': ['email', 'password1', 'password2', 'is_superuser', 'favourite_genres', 'favourite_cinemas']}],
    ]
    search_fields = ['email']
    ordering = ['email']
    readonly_fields = ['last_login', 'registered_at', 'password_reset_token']


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# Unregister the Group model from admin.
admin.site.unregister(Group)
