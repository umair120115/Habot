from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Employee, AppUser
from .serializers import EmployeeSerializer , AppUserSignUpSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.
class UserSignUpView(generics.CreateAPIView):
    permission_classes=[permissions.AllowAny]
    serializer_class= AppUserSignUpSerializer
    queryset = AppUser.objects.all()
class EmployeePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class EmployeeListCreateView(generics.ListCreateAPIView):
    # This single view handles both GET (List) and POST (Create)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    pagination_class = EmployeePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department', 'role']

class EmployeeDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        employee_id = self.kwargs.get('id')
        if not employee_id:
            return Response({"error":"Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            employee = Employee.objects.get(id=employee_id)
            serializer = EmployeeSerializer(employee)
            return Response({"employee_details":serializer.data}, status = status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"error":"No employee found with the given ID"}, status = status.HTTP_404_NOT_FOUND)

    
    
    def patch(self, request, *args, **kwargs):
        employee_id = self.kwargs.get('id')
        if not employee_id:
            return Response({"error":"Employee ID is required!"}, status = status.HTTP_400_BAD_REQUEST)
        try:
            employee = Employee.objects.get(id=employee_id)
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Employee updated successfully", "employee":serializer.data}, status= status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        except Employee.DoesNotExist:
            return Response({"error":"No employee found with the given ID"}, status = status.HTTP_404_NOT_FOUND)


    def delete(self, request, *args, **kwargs):
        employee_id = self.kwargs.get('id')
        if not employee_id:
            return Response({"error":"Employee ID is required!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            employee = Employee.objects.get(id = employee_id)
            employee.delete()
            return Response({"message":"Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({"error":"No employee found with the given ID"}, status=status.HTTP_404_NOT_FOUND)