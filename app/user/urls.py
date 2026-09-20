"""
URL mappings for the user API.
"""
from django.urls import path
from user import views


app_name = 'user'  # Used for reverse mapping

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageuserView.as_view(), name='me'),
]
