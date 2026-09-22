"""
Serializers for the Recipe API
"""
from django.contrib.auth import get_user_model, authenticate
from core import models

from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    """serializer for Tag"""
    class Meta():
        model = models.Tag
        fields = ('id', 'name',)

        read_only_fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):
    """Serializers for Ingredient"""
    class Meta():
        model = models.Ingredient
        fields = ['id','name']  #  we can use either list / Tuple
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    """serializer for Recipe model"""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta():
        model = models.Recipe
        fields = ('id', 'title', 'time_minutes', 'price', 'link','tags', 'ingredients')
        read_only_fields = ('id',)

    def _get_or_create_tags(self, tags, recipe):
        """Hendle getting or creating tags"""
        # We need to take request from contect becuase we are in Serializers not in Views
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = models.Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Hendle getting or creating tags"""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = models.Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient
            )
            recipe.ingredients.add(ingredient_obj)




    def create(self, validated_data):
        """Create a Recipe"""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = models.Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update a recipe"""

        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        return super().update(instance, validated_data)



class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for the recipe detail view"""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)

