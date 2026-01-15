from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.cache import cache
from .models import Employee

class EmployeeAPITests(APITestCase):
    
    def setUp(self):
        """
        This runs BEFORE every single test method.
        We use it to set up initial data (so we don't repeat code).
        """
        # 1. Create a sample product to test with
        self.product = Product.objects.create(
            name="John Doe", 
            email="johndoe@example.com", 
            department="HR",
            role ="Manager"
        )
        
        # 2. Get the URL for the API (Assume your urls.py has name='product-list')
        # If your URL is 'api/products/', use reverse to find it dynamically.
        self.list_url = reverse('product-list') 
        
        # 3. Clear cache before tests so old data doesn't interfere
        cache.clear()

    def test_get_all_products(self):
        """
        Test GET: Ensure we can retrieve the list of products.
        """
        response = self.client.get(self.list_url)
        
        # Check if status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if the data returned matches what we put in setUp
        # (Assuming pagination is on, data might be in response.data['results'])
        # If no pagination, just use response.data
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['name'], "Test Laptop")
        else:
            self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        """
        Test POST: Ensure we can create a new product.
        """
        data = {
            "name": "New Phone",
            "price": 500,
            "description": "A smartphone"
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        # Check if status is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if the object actually exists in the database
        self.assertEqual(Product.objects.count(), 2) # 1 from setUp + 1 new
        self.assertEqual(Product.objects.get(name="New Phone").price, 500)

    def test_update_product(self):
        """
        Test PATCH: Ensure we can update an existing product.
        """
        # Define the URL for a specific product (e.g., /api/products/1/)
        # Assumes your detail URL is named 'product-detail'
        url = reverse('product-detail', args=[self.product.id])
        
        data = {
            "price": 1200 # Changing price from 1000 to 1200
        }
        
        response = self.client.patch(url, data, format='json')
        
        # Check status 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh the object from DB to see if it changed
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 1200)

    def test_delete_product(self):
        """
        Test DELETE: Ensure we can delete a product.
        """
        url = reverse('product-detail', args=[self.product.id])
        
        response = self.client.delete(url)
        
        # Check status 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Ensure it is gone from the DB
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
# Create your tests here.
