"""
Test for Django admin modifications.
"""
from django.test import TestCase
# Import Django's TestCase class to write unit tests.
# TestCase is a subclass of unittest.TestCase, providing utility methods for testing Django apps.

from django.contrib.auth import get_user_model
# Import `get_user_model` to fetch the custom user model (if customized), otherwise the default user model.
from django.urls import reverse
# Import `reverse` to dynamically generate URLs for views, especially useful for testing purposes.
from django.test import Client
# Import `Client` to simulate a dummy web client for testing HTTP requests.

class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        # The `setUp` method is called before each test to set up any state that is shared by all tests.
        self.client = Client()
        # Create a superuser (admin) for testing. This user will have full privileges in the admin site.
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        # Log in as the admin user using `force_login` to simulate an authenticated admin session.
        self.client.force_login(self.admin_user)

        # Create a normal user to test regular user functionality on the admin site.
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_list(self):
        """Test that users are listed on the page."""
        # Generate the URL for the Django admin's user changelist view using the `reverse` function.
        # `admin:core_user_changelist` is the admin URL namespace for the user changelist page.
        url = reverse('admin:core_user_changelist')

        # Send a GET request to the admin user changelist URL.
        res = self.client.get(url)

        # Assert that the response contains the user's name and email to verify that the user appears in the admin list.
        self.assertContains(res, self.user.name)  # Ensure that `Test User` is visible on the list page.
        self.assertContains(res, self.user.email)  # Ensure that `user@example.com` is visible as well.

    def test_edit_user_page(self):
        """Test the edit user page works."""
        # Generate the URL for the "change" page of the user model in the admin. The `args=[self.user.id]` ensures that we are targeting this specific user.
        url = reverse('admin:core_user_change', args=[self.user.id])

        # Send a GET request to the user edit page in the admin.
        res = self.client.get(url)

        # Check that the response status code is 200, indicating the page loads correctly.
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        # Generate the URL for the "add" page of the user model in the admin.
        # This page is where admin users can create new users.
        url = reverse('admin:core_user_add')

        # Send a GET request to the user creation page in the admin.
        res = self.client.get(url)

        # Check that the response status code is 200, indicating the page loads successfully.
        self.assertEqual(res.status_code, 200)
