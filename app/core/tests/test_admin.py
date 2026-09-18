"""
Tests for the djago admin modifications
"""

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class AdminSiteTests(TestCase):
    """Tests for djanfo admin"""

    def setUp(self):  # This has to be exactly like this
        """Setting up super user and user"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='admintest@123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            name='TestUser',
        )

    def test_user_list(self):
        """Test that the users are listed on the page"""
        # the url patter is admi:<app name>_<model name>_<valid namespace from django doc
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works"""
        url = reverse('admin:core_user_change', args=(self.user.id,))
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test to create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)