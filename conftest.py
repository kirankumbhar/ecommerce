# tests/conftest.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from core.models import Product, Order

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def products():
    return [
        Product.objects.create(
            name='Test Product 1',
            price=100.00,
            stock=10
        ),
        Product.objects.create(
            name='Test Product 2',
            price=200.00,
            stock=5
        )
    ]