from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        # Initialize the test client and create an admin user for testing
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)

        # Create a normal user to test regular functionality
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_list(self):
        """Test that users are listed on the page."""
        # Generate the URL for the Django admin's user changelist view
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # Ensure the user name and email are present in the list
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        # Generate the URL for editing a specific user's details
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # Ensure the response status is 200 (OK), meaning the page loaded
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        # Generate the URL for creating a new user
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        # Ensure the response status is 200 (OK), meaning the page loaded
        self.assertEqual(res.status_code, 200)
