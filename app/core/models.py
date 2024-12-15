"""
Database models for custom user management.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,  # Provides core user authentication functionality.
    BaseUserManager,   # A base class for custom user model managers.
    PermissionsMixin   # Adds permission-related fields and methods (e.g., is_staff, is_superuser).
)


class UserManager(BaseUserManager):
    """Custom manager for managing User instances."""

    def create_user(self, email, password=None, **extra_fields):
        """
        Create, save, and return a new user with an email and password.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user.
            **extra_fields: Additional fields to be passed for the user (e.g., name).

        Returns:
            User: The created user instance.
        """
        if not email:
            raise ValueError('User must have an email address.')

        # Normalize the email address before creating the user.
        user = self.model(email=self.normalize_email(email), **extra_fields)

        # Set and hash the password for the user.
        user.set_password(password)

        # Save the user to the database.
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create and return a new superuser with admin privileges.

        Args:
            email (str): The email address of the superuser.
            password (str): The password for the superuser.

        Returns:
            User: The created superuser instance.
        """
        # Create a regular user first, then set the staff and superuser flags.
        user = self.create_user(email, password)

        user.is_staff = True
        user.is_superuser = True

        # Save the superuser to the database.
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with authentication and permissions features."""

    email = models.EmailField(max_length=255, unique=True)
    # Email is used as the unique identifier for authentication.
    # The max_length of 255 ensures it's within the standard limit for email addresses.

    name = models.CharField(max_length=255)
    # Name field to store the user's full name.

    is_active = models.BooleanField(default=True)
    # Indicates whether the user account is active. Defaults to True.

    is_staff = models.BooleanField(default=False)
    # Determines if the user has access to the Django admin. Defaults to False.

    # Attach custom user manager to handle user creation.
    objects = UserManager()

    USERNAME_FIELD = 'email'
    # Use email instead of the default username field for user identification.

    # Django requires these fields for authentication and permission handling.
    REQUIRED_FIELDS = ['name']
    # `REQUIRED_FIELDS` specifies additional fields required during user creation via the admin.
