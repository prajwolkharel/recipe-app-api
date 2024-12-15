"""
Django admin customization
"""
from django.contrib import admin
# Import the default UserAdmin from django.contrib.auth, which handles user-related administrative tasks.
# We will extend this class to customize the admin interface for our `User` model.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _  # Import gettext_lazy for translating strings in the admin interface.

# Import the custom User model from the `core` app
from core import models


# Custom UserAdmin class to define the admin interface for the User model
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    # The ordering of the user records in the admin interface (default ordering by 'id').
    ordering = ['id']

    # List of fields displayed in the user list page in the admin interface.
    # Here, we display 'email' and 'name' of the user.
    list_display = ['email', 'name']

    # Define the fieldsets for the User model's edit page. This controls the layout of the form when editing users.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # The basic fields section with 'email' and 'password'.
        (
            _('Permissions'),  # Translated section title using gettext_lazy.
            {
                'fields': (
                    'is_active',  # Indicates if the user account is active.
                    'is_staff',   # Indicates if the user has staff privileges.
                    'is_superuser',  # Indicates if the user has superuser privileges.
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),  # Display the 'last_login' field.
    )

    # The `last_login` field will be displayed as readonly since it is typically not editable by admins.
    readonly_fields = ['last_login']

    # Add additional fields when creating a new user through the admin interface.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # Apply the 'wide' class to the fieldset to make it more spacious.
            'fields': (
                'email',  # Email field for the user.
                'password1',  # Password field (for password creation).
                'password2',  # Password confirmation field.
                'name',  # Name field for the user.
                'is_active',  # Whether the user account is active.
                'is_staff',  # Whether the user has staff privileges.
                'is_superuser',  # Whether the user is a superuser.
            )
        }),
    )

# Register the custom `UserAdmin` for the `User` model in the admin interface.
# This custom admin class ensures that the `User` model's admin interface is displayed according to our configuration.
admin.site.register(models.User, UserAdmin)
