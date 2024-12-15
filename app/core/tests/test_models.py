"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test Models."""
    # The `ModelTests` class inherits from `TestCase`, which provides testing utilities for database-backed tests.
    # This class contains tests that ensure our user model behaves as expected.

    def test_create_user_with_email_success(self):
        """Test creating a user with an email is successful."""
        # This test case verifies that we can successfully create a user when providing an email and password.

        email = 'test@gmail.com'
        password = 'testpass123'

        # Create the user using the custom user manager.
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        # Assert that the email on the user matches the one provided.
        self.assertEqual(user.email, email)

        # Assert that the user's password is correctly set and can be verified using `check_password`.
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        # This test ensures that email addresses are normalized (lowercased) when a new user is created.
        # This helps prevent issues related to case sensitivity when performing operations with emails (e.g., login).

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],  # Test various uppercase variations of emails.
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        # Loop through the sample emails and check that they are normalized.
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)  # Assert that the email has been normalized.

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        # This test ensures that an exception is raised if a user is created without an email address.

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')  # Pass an empty string for the email, which should fail.

    def test_create_superuser(self):
        """Test creating a superuser."""
        # This test checks that the `create_superuser` method properly sets up a superuser.

        # Create a superuser by passing an email and password.
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        # Assert that the created user has superuser privileges and is marked as staff.
        self.assertTrue(user.is_superuser)  # Superusers should have `is_superuser=True`.
        self.assertTrue(user.is_staff)      # Superusers should also have `is_staff=True`.
