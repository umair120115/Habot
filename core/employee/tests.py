import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Employee, AppUser

# Get the custom user model (AppUser) dynamically
User = get_user_model()

class EmployeeAPITests(APITestCase):

    def setUp(self):
        # 1. Create a Test User
        # We use your custom email field for the user creation
        self.user = AppUser.objects.create_user(
            email='testuser@example.com', 
            password='password123',
            username='testuser'
        )

        # 2. Authenticate EVERY request
        # This simulates sending the "Bearer <token>" header automatically
        self.client.force_authenticate(user=self.user)

        # 3. Create initial Data
        self.employee1 = Employee.objects.create(
            name="Alice", 
            department="IT", 
            role="Developer",
            email="alice@example.com"
        )
        self.employee2 = Employee.objects.create(
            name="Bob", 
            department="HR", 
            role="Manager",
            email="bob@example.com"
        )

        # 4. URLs
        self.list_url = reverse('employee-list-create')
        self.detail_url = reverse('employee-detail', args=[self.employee1.id])

    # ----------------------------------------------------------------
    # 1. TESTS FOR LIST & CREATE
    # ----------------------------------------------------------------

    def test_get_employee_list(self):
        """Test retrieving the list of employees"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_create_employee(self):
        """Test creating a new employee"""
        data = {
            "name": "Charlie",
            "department": "Sales",
            "role": "Analyst",
            "email": "charlie@example.com"
        }
        response = self.client.post(self.list_url, data, format='json')
        
        # If this fails, print the error to see what went wrong
        if response.status_code != 201:
            print(f"\nCreate Error: {response.data}")
            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 3)

    def test_filter_employee_list(self):
        """Test filtering employees by department"""
        response = self.client.get(f"{self.list_url}?department=HR")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Alice')

    # ----------------------------------------------------------------
    # 2. TESTS FOR DETAIL VIEW (UUID Handling)
    # ----------------------------------------------------------------

    def test_get_employee_detail(self):
        """Test retrieving a single employee"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee_details']['name'], "Alice")

    def test_update_employee(self):
        """Test updating an employee"""
        data = {"role": "Senior Developer"}
        response = self.client.patch(self.detail_url, data, format='json')
        
        # DEBUGGING: Print errors if we get a 400 Bad Request
        if response.status_code == 400:
            print(f"\nUpdate Validation Errors: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee1.refresh_from_db()
        self.assertEqual(self.employee1.role, "Developer")

    def test_delete_employee(self):
        """Test deleting an employee"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 1)

    def test_employee_not_found(self):
        """Test request with a non-existent UUID"""
        # FIX: Generate a random UUID instead of using integer 999
        random_uuid = uuid.uuid4()
        invalid_url = reverse('employee-detail', args=[random_uuid])
        
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)