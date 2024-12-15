from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,  # Base class for user models
    BaseUserManager,  # Manages user creation
    PermissionsMixin  # Grants permission functionality to the user
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save, and return a new user."""
        # Ensure email is provided, raise an error if not
        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )
        # Set the password and save the user
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True  # Set staff to True for admin access
        user.is_superuser = True  # Grant superuser privileges
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)  # Name field
    is_active = models.BooleanField(default=True)  # Active status field
    is_staff = models.BooleanField(default=False)  # Staff access (admin)

    objects = UserManager()  # Use the custom UserManager for user creation

    USERNAME_FIELD = 'email'  # Use email as the unique identifier for login

    REQUIRED_FIELDS = ['name']  # Name is required when creating a user
