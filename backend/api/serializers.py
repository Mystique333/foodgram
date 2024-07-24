# import sys
# def eprint(*args, **kwargs):
#     print(*args, file=sys.stderr, **kwargs)
from django.contrib.auth import get_user_model
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


class TagSerializer(ModelSerializer):
    """Сериалайзер тегов."""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class IngredientSerializer(ModelSerializer):
    """Сериалайзер ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class UserAvatarSerializer(serializers.ModelSerializer):
    """Сериалайзер аватара пользователей"""

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
    """Сериалайзер пользователей."""
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
    """READ ONLY сериалайзер ингредиентов."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientsReadSerializer(serializers.ModelSerializer):
    """Сериалайзер ингредиентов-рецептов."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    amount = serializers.ReadOnlyField()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(ModelSerializer):
    """READ ONLY сериалайзер рецептов."""

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
    """Сериалайзер для добавления ингредиентов в рецепт."""

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
    """Сериалайзер для создания рецептов."""

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
        if ingredients is None:
            return True
        if not isinstance(ingredients, list):
            raise ValidationError(
                {'ingredients': 'Нужен хотя бы один ингредиент!'}
            )

        ingredients_list = []

        for item in ingredients:
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
        ingredients_data = validated_data.pop('ingredient_list', None)
        if not ingredients_data:
            raise serializers.ValidationError({"ingredients": "Нужен хотя бы один ингредиент."})

        tags_data = validated_data.pop('tags', [])
        user = self.context['request'].user
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe


    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredient_list', None)
        tags_data = validated_data.pop('tags', None)

        if self.context['request'].method == 'PATCH':
            if ingredients_data is None or (not isinstance(ingredients_data, list) or len(ingredients_data) == 0):
                raise serializers.ValidationError({"ingredients": "Нужен хотя бы один ингредиент."})
            
            if tags_data is None or (not isinstance(tags_data, list) or len(tags_data) == 0):
                raise serializers.ValidationError({"tags": "Нужно выбрать хотя бы один тег."})

        elif ingredients_data is None:
            raise serializers.ValidationError({"ingredients": "Нужен хотя бы один ингредиент."})
        
        if tags_data is None:
            raise serializers.ValidationError({"tags": "Нужно выбрать хотя бы один тег."})

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)

        if tags_data is not None:
            instance.tags.set(tags_data)
        else:
            instance.tags.clear()

        if ingredients_data is not None:
            instance.ingredient_list.set([])
            self.create_ingredients(ingredients_data, instance)

        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data


class SimpleUserSerializer(serializers.ModelSerializer):
    """Упрощенный сериалайзер пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscribe.objects.filter(user=request.user, author=obj).exists()
        return False


class RecipeShortSerializer(serializers.ModelSerializer):
    """Упрощенный сериалайзер рецептов."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериалайзер подписок."""

    id = serializers.IntegerField(source='author.id')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    email = serializers.EmailField(source='author.email')
    avatar = serializers.ImageField(source='author.avatar', allow_null=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 
            'avatar', 'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscribe.objects.filter(
                user=request.user, 
                author=instance.author
                ).exists()
        return False

    def get_recipes(self, instance):
        request = self.context.get('request')
        recipes_limit = int(request.query_params.get('recipes_limit', 5))
        recipes = instance.author.recipes.all()[:recipes_limit]
        return RecipeShortSerializer(recipes, many=True).data

    def get_recipes_count(self, instance):
        return instance.author.recipes.count()

class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
