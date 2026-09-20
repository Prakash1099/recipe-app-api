"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer, AuthTokenSerializer



class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create new Auth Token for user"""
    serializer_class = AuthTokenSerializer

    # We include this so that this view include in the Browsable API
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageuserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # print("Getting Userinfo")
        # print("USER:", self.request.user)
        # print("AUTH:", self.request.auth)
        return self.request.user





