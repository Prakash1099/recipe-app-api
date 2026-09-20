"""
Serializers for the Recipe API
"""
from django.contrib.auth import get_user_model, authenticate
from core import models

from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    """serializer for Recipe model"""
    class Meta():
        model = models.Recipe
        fields = ('id', 'title', 'time_minutes', 'price', 'link', 'user')
        read_only_fields = ('id','user')


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for the recipe detail view"""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)


class TagSerializer(serializers.ModelSerializer):
    """serializer for Tag"""
    class Meta():
        model = models.Tag
        fields = ('id', 'name',)

        read_only_fields = ('id',)