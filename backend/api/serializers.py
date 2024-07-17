import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from backend.constants import MIN_VALUE, MAX_VALUE
from recipes.models import (
    Ingredient, Recipe, RecipeIngredients, Subscribe, Tag
)

User = get_user_model()


class IngredientSerializer(ModelSerializer):
    """Сериалайзер для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(ModelSerializer):
    """Сериалайзер для тегов."""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class UserAvatarSerializer(serializers.ModelSerializer):
    """Сериалайзер для аватара пользователей"""

    avatar = Base64ImageField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = ['avatar']

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class UsersSerializer(UserSerializer):
    """Сериалайзер для пользователей."""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        if user == obj:
            return False
        is_subscribed = Subscribe.objects.filter(user=user, author=obj).exists()
        eprint(f"User: {user}, Author: {obj}, is_subscribed: {is_subscribed}")
        return is_subscribed


class UsersCreateSerializer(UserCreateSerializer):
    """Сериалайзер для создания пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Невозможно создать аккаунт с username "me!"'
            )
        return value


class IngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientsReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    amount = serializers.ReadOnlyField()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(ModelSerializer):
    """Сериалайзер для рецептов. Режим безопасных методов."""
    tags = TagSerializer(many=True, read_only=True)
    author = UsersSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientsReadSerializer(
        source='ingredient_list', many=True
    )
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    # def get_ingredients(self, obj):
    #     eprint(obj)
    #     return self.ingredients

    def is_user_anonymous(self):
        return self.context['request'].user.is_anonymous

    def get_is_favorited(self, obj):
        if self.is_user_anonymous():
            return False
        user = self.context['request'].user
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.is_user_anonymous():
            return False
        user = self.context['request'].user
        return user.shopping_cart.filter(recipe=obj).exists()


class RecipeIngredientsWriteSerializer(ModelSerializer):
    """Сериалайзер для модели добавления ингредиентов в рецепт."""
    id = serializers.IntegerField(source='ingredient.id')
    amount = serializers.IntegerField(
        min_value=MIN_VALUE,
        max_value=MAX_VALUE,
        error_messages={
            'min_value': f'Количество ингредиентов должно быть больше {MIN_VALUE}',
            'max_value': f'Количество ингредиентов должно быть меньше {MAX_VALUE}',
        }
    )

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')

    def get_id(self, instance):
        return instance.ingredient.id


class RecipeWriteSerializer(ModelSerializer):
    """Сериалайзер для рецептов. Режим методов записи."""
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = UsersSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientsWriteSerializer(
        source='ingredient_list', many=True,
    )
    cooking_time = serializers.IntegerField(
        min_value=MIN_VALUE,
        max_value=MAX_VALUE,
        error_messages={
            'min_value': f'Время приготовления не менее {MIN_VALUE} минут!',
            'max_value': f'Время приготовления не более {MAX_VALUE} минут!',
        }
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_image(self, value):
        if not value:
            raise ValidationError('Поле "image" не может быть пустым!')
        return value

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise ValidationError(
                {'ingredients': 'Нужен хотя бы один ингредиент!'}
            )

        ingredients_list = []

        for item in ingredients:
            eprint()
            eprint(ingredients)
            eprint(item)
            eprint()
            if 'id' not in item['ingredient']:
                raise ValidationError(
                    {'ingredients': 'Указан некорректный формат ингредиента!'}
                )

            try:
                ingredient = Ingredient.objects.get(id=item['ingredient']['id'])
            except Ingredient.DoesNotExist:
                raise ValidationError(
                    {'ingredients': 'Ингредиент не существует!'}
                )

            if ingredient in ingredients_list:
                raise ValidationError(
                    {'ingredients': 'Ингредиенты не могут повторяться!'}
                )

            ingredients_list.append(ingredient)

        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError(
                {'tags': 'Нужно выбрать хотя бы один тег!'}
            )
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError(
                    {'tags': 'Теги должны быть уникальными!'}
                )
            tags_list.append(tag)
        return value

    def create_ingredients(self, ingredients, recipe):
        eprint(ingredients)
        eprint('ВЫЗВАНА ФУНКЦИЯ CREATE_INGREDIENTS!!!!!!!!!!!!!!')
        instances = [
            RecipeIngredients(
                ingredient=Ingredient.objects.get(id=ingredient['ingredient']['id']),
                recipe=recipe,
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        RecipeIngredients.objects.bulk_create(instances)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredient_list', [])
        eprint('ВЫЗВАНА ГЛАВНАЯ ФУНКЦИЯ CREATE!!!!!!!!!!!!!!')
        eprint(ingredients_data)
        eprint(validated_data)
        tags_data = validated_data.pop('tags', [])
        user = self.context['request'].user
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        tags_data = validated_data.pop('tags', None)
        if ingredients_data is None:
            raise serializers.ValidationError({"ingridients": "Нужен хотя бы один ингредиент."})
        if tags_data is None:
            raise serializers.ValidationError({"tags": "Нужен хотя бы один тег."})
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)

        instance.save()

# TODO тут какая хуйня надо подумать.
        if tags_data is not None:
            instance.tags.set(tags_data)
        else:
            instance.tags.clear()

        instance.ingredients.all().delete()
        self.create_ingredients(ingredients_data, instance)

        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data


class RecipeShortSerializer(ModelSerializer):
    """Сериалайзер для рецептов. Режим краткого ответа на запрос."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='author.email', read_only=True)
    id = serializers.IntegerField(source='author.id', read_only=True)
    username = serializers.CharField(source='author.username', read_only=True)
    first_name = serializers.CharField(source='author.first_name', read_only=True)
    last_name = serializers.CharField(source='author.last_name', read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    avatar = serializers.ImageField(source='author.avatar', read_only=True)

    class Meta:
        model = Subscribe
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 
            'is_subscribed', 'recipes', 'recipes_count', 'avatar'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscribe.objects.filter(user=user, author=obj.author).exists()

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get('recipes_limit')
        recipes = obj.author.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        return RecipeShortSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()