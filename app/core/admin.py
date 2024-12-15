from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']  # Order the list by user ID

    # Fields to display in the user list view
    list_display = ['email', 'name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Basic fields
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',  # Whether the user is active
                    'is_staff',  # Staff access (used for admin)
                    'is_superuser',  # Superuser privileges
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    readonly_fields = ['last_login']  # Make last_login read-only in the admin

    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # Style class for the fieldset
            'fields': (
                'email',
                'password1',  # Password field
                'password2',  # Password confirmation
                'name',
                'is_active',  # Whether the user is active
                'is_staff',  # Staff access
                'is_superuser',  # Superuser privileges
            )
        }),
    )


# Register the custom UserAdmin class with the User model
admin.site.register(models.User, UserAdmin)
