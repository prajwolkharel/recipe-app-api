"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', {})
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user

        # Debugging: print tags to check what is being passed
        print(f"Tags passed: {tags}")

        for tag in tags:
            # Debugging: print tag object creation or fetching
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            print(f"Tag created: {created}, Tag object: {tag_obj}")
            recipe.tags.add(tag_obj)

        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
