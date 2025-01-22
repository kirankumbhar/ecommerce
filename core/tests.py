# tests/test_orders.py
import pytest
from django.urls import reverse
from rest_framework import status
from .models import Order, OrderItem, Product

@pytest.mark.django_db
class TestOrderAPI:
    def test_create_order_successful(self, authenticated_client, products):
        url = reverse('order-list')
        data = {
            "items": [
                {
                    "product": products[0].id,
                    "quantity": 2
                }
            ]
        }
        
        response = authenticated_client.post(url, data, format='json')
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1
        assert OrderItem.objects.count() == 1
        updated_product = Product.objects.get(id=products[0].id)
        assert updated_product.stock == 8

    def test_create_order_insufficient_stock(self, authenticated_client, products):
        url = reverse('order-list')
        data = {
            "items": [
                {
                    "product": products[0].id,
                    "quantity": 11
                }
            ]
        }
        
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Insufficient stock" in str(response.data)
        assert Order.objects.count() == 0
        updated_product = Product.objects.get(id=products[0].id)
        assert updated_product.stock == 10

    def test_create_order_multiple_items(self, authenticated_client, products):
        url = reverse('order-list')
        data = {
            "items": [
                {
                    "product": products[0].id,
                    "quantity": 2
                },
                {
                    "product": products[1].id,
                    "quantity": 1
                }
            ]
        }
        
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1
        assert OrderItem.objects.count() == 2
        product1 = Product.objects.get(id=products[0].id)
        product2 = Product.objects.get(id=products[1].id)
        assert product1.stock == 8
        assert product2.stock == 4

    def test_create_order_unauthenticated(self, api_client, products):
        url = reverse('order-list')
        data = {
            "items": [
                {
                    "product": products[0].id,
                    "quantity": 1
                }
            ]
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_order_invalid_product_id(self, authenticated_client):
        url = reverse('order-list')
        data = {
            "items": [
                {
                    "product": -1,
                    "quantity": 1
                }
            ]
        }
        
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_order_invalid_quantity(self, authenticated_client, products):
        url = reverse('order-list')
        data = {
            "items": [
                {
                    "product": products[0].id,
                    "quantity": 0
                }
            ]
        }
        
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_order_empty_items(self, authenticated_client):
        url = reverse('order-list')
        data = {
            "items": []
        }
        
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_order_invalid_quantity(self, authenticated_client, products):
        url = reverse('order-list')
        data = {
            "items": [
                {
                    "product": products[0].id,
                    "quantity": -1
                }
            ]
        }
        
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestProductViewSet:
    def test_list_products(self, authenticated_client, products):
        url = reverse('product-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(products)
        
        # Verify product data
        for product_data, product in zip(response.data, products):
            assert product_data['name'] == product.name
            assert float(product_data['price']) == float(product.price)
            assert product_data['stock'] == product.stock
    
    def test_create_product(self, authenticated_client):
        url = reverse('product-list')
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': '99.99',
            'stock': 50,
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 1
        product = Product.objects.first()
        assert product.name == data['name']
        assert float(product.price) == float(data['price'])
        assert product.stock == data['stock']
    
    def test_unauthorized_access(self, api_client, products):
        # Test unauthorized access to different endpoints
        list_url = reverse('product-list')
        detail_url = reverse('product-detail', kwargs={'pk': products[0].id})
        
        # Test GET list
        response = api_client.get(list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Test POST
        response = api_client.post(list_url, {}, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Test GET detail
        response = api_client.get(detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED