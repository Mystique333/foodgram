from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from backend.constants import MIN_VALUE, MAX_VALUE
from recipes.models import (
    Ingredient, Recipe, RecipeIngredient, Subscribe, Tag
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


class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Текущий пароль неверен.")
        return value

    def validate(self, data):
        if not data.get('current_password') or not data.get('new_password'):
            raise serializers.ValidationError(
                'Требуется указать текущий и новый пароли.'
            )
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserAvatarSerializer(serializers.ModelSerializer):
    """Сериалайзер аватара пользователей"""

    avatar = Base64ImageField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = ['avatar']

    def validate(self, data):
        request = self.context.get('request')
        if request.method in ['PUT', 'PATCH']:
            if not data or 'avatar' not in data:
                raise serializers.ValidationError(
                    {'avatar': 'Поле "avatar" обязательно для обновления.'}
                )
        return data

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
        if user.is_anonymous or user == obj:
            return False
        is_subscribed = Subscribe.objects.filter(
            user=user, author=obj).exists()
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

    def get_response(self):
        response_data = {
            key: value
            for key, value in self.data.items()
            if key not in ['is_subscribed', 'avatar']}
        return response_data


class IngredientReadSerializer(serializers.ModelSerializer):
    """READ ONLY сериалайзер ингредиентов."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    """Сериалайзер ингредиентов-рецептов."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')
    amount = serializers.ReadOnlyField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(ModelSerializer):
    """READ ONLY сериалайзер рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = UsersSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientReadSerializer(
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


class RecipeIngredientWriteSerializer(ModelSerializer):
    """Сериалайзер для добавления ингредиентов в рецепт."""

    id = serializers.IntegerField(source='ingredient.id')
    amount = serializers.IntegerField(
        min_value=MIN_VALUE,
        max_value=MAX_VALUE,
        error_messages={
            'min_value':
                f'Количество ингредиентов должно быть больше {MIN_VALUE}',
            'max_value':
                f'Количество ингредиентов должно быть меньше {MAX_VALUE}',
        }
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeWriteSerializer(ModelSerializer):
    """Сериалайзер для создания рецептов."""

    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = UsersSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientWriteSerializer(
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

    def validate(self, data):
        if 'ingredient_list' not in data:
            raise ValidationError(
                {"ingredients": "В запросе не передано поле."})

        if 'tags' not in data:
            raise ValidationError(
                {"tags": "В запросе не передано поле."})

        return data

    def validate_image(self, value):
        if not value:
            raise ValidationError('Поле "image" не может быть пустым!')

        return value

    def validate_ingredients(self, value):
        ingredients = value
        if (
            ingredients is None
            or not isinstance(ingredients, list)
            or len(ingredients) == 0
        ):
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
                ingredient = Ingredient.objects.get(
                    id=item['ingredient']['id'])
            except Ingredient.DoesNotExist:
                raise ValidationError(
                    {'ingredients': 'Ингредиент не существует!'}
                )

            amount = item.get('amount')
            if amount is None or amount < MIN_VALUE:
                raise ValidationError({
                    'amount': (
                        'Количество ингредиентов должно быть больше '
                        f'{MIN_VALUE}'
                    )
                })

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
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        instances = [
            RecipeIngredient(
                ingredient_id=ingredient['ingredient']['id'],
                recipe=recipe,
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(instances)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredient_list', None)
        tags_data = validated_data.pop('tags', [])
        user = self.context['request'].user
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredient_list', None)
        tags_data = validated_data.pop('tags', None)

        instance = super().update(instance, validated_data)
        instance.tags.set(tags_data)
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
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'avatar', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscribe.objects.filter(user=request.user,
                                            author=obj).exists()
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
