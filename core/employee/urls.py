from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import EmployeeListCreateView, EmployeeDetailView, UserSignUpView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # Cleaned up URL: Handles List AND Create
    path('signup/',UserSignUpView.as_view(), name='user-signup'),
    path('token/', TokenObtainPairView.as_view(), name='access_token_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<uuid:id>/', EmployeeDetailView.as_view(), name='employee-detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 