"""
Serializers for the user API Vew.
"""
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _  # Common syntax for translations in Django

class UserSerializer(serializers.ModelSerializer):
    """Serialier for the user object"""


    class Meta():

        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        """Crete and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self,instance, validate_data):
        """Update and return user"""
        password = validate_data.pop('password', None)
        user = super().update(instance, validate_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={
            'input_type': 'password'
        },
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate the credentials and provide authToken"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
