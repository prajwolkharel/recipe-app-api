"""
Database models.
"""
from django.db import models
# Importing required modules from Django for creating custom user models.
# AbstractBaseUser allows us to define a custom user model, and PermissionsMixin provides the permissions functionality.
from django.contrib.auth.models import (
    AbstractBaseUser,  # Base class for a custom user model with authentication features.
    BaseUserManager,  # Base class for creating a custom manager for users.
    PermissionsMixin  # Provides permissions-related fields and methods (is_staff, is_superuser, etc.).
)


class UserManager(BaseUserManager):
    """Manager for users."""

    # Custom manager class to handle user creation and superuser creation.
    # This is used to handle the creation of user instances in a flexible way (custom fields, validation, etc.).

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        # A method to create a regular user. It takes the email and password as mandatory parameters,
        # with any additional fields passed in `extra_fields` (such as `name`, etc.).

        # Ensure that the user provides an email address.
        if not email:
            raise ValueError('User must have an email address.')  # Raising a ValueError if email is not provided.

        # Normalize the email address (ensures proper case and formatting) and create a new user instance.
        user = self.model(email=self.normalize_email(email), **extra_fields)

        # Set the password for the user (hashed and salted automatically by Django).
        user.set_password(password)

        # Save the user instance to the database.
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        # This method is for creating a superuser with admin privileges.
        user = self.create_user(email, password)

        # Set the necessary flags to indicate the user is a staff member and superuser.
        user.is_staff = True
        user.is_superuser = True

        # Save the superuser to the database.
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    # Custom user model that extends `AbstractBaseUser` for authentication and `PermissionsMixin` for permissions.

    # Defining the fields for the custom user model:

    email = models.EmailField(max_length=255, unique=True)
    # The `email` field is used as the unique identifier for the user. The `unique=True` constraint ensures no two users can have the same email.
    # The `max_length=255` ensures that the email address is not too long, which is a common limit for email addresses.

    name = models.CharField(max_length=255)
    # The `name` field stores the full name of the user (can be used for display purposes in the admin or other parts of the app).

    is_active = models.BooleanField(default=True)
    # The `is_active` field indicates whether the user is active. It defaults to `True`, so the user is considered active unless explicitly disabled.

    is_staff = models.BooleanField(default=False)
    # The `is_staff` field indicates whether the user has staff privileges. It's used to determine if the user can access the Django admin site.

    # Attach the custom user manager to the model. This manager will be used to create and manage user instances.
    objects = UserManager()

    # The `USERNAME_FIELD` specifies which field will be used for authentication.
    # Instead of using the default `username`, we are using `email` as the unique identifier for the user.
    USERNAME_FIELD = 'email'

    # In addition to `USERNAME_FIELD`, Django requires that the user model has a `password` field (from AbstractBaseUser),
    # and it also requires `is_active`, `is_staff`, and `is_superuser` fields for permission management (from PermissionsMixin).
