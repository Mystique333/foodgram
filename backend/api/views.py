from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
import pyshorteners

from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Subscribe, Tag)
from backend.filters import IngredientFilter, RecipeFilter
from backend.pagination import CustomPagination
from backend.permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeShortSerializer, RecipeWriteSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UsersSerializer, UserAvatarSerializer,
                          UsersCreateSerializer, SetPasswordSerializer)

User = get_user_model()


class UsersViewSet(ModelViewSet):
    """Вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UsersCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.get_response()
        return Response(response_data,
                        status=status.HTTP_201_CREATED, headers=headers)

    @action(
        detail=False,
        methods=['put', 'patch', 'delete', 'get'],
        url_path='me/avatar',
        permission_classes=[IsAuthenticated]
    )
    def avatar(self, request):
        user = request.user
        if request.method in ['PUT', 'PATCH']:
            serializer = UserAvatarSerializer(
                user, data=request.data,
                context={'request': request}, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == 'DELETE':
            if user.avatar:
                user.avatar.delete()
                user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'GET':
            if user.avatar:
                return Response(
                    {'avatar': request.build_absolute_uri(user.avatar.url)})
            return Response({'message': 'Avatar not found'},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=False,
            methods=['post'],
            url_path='set_password',
            permission_classes=[IsAuthenticated]
            )
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            url_path='subscriptions',
            permission_classes=[IsAuthenticated]
            )
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscribe.objects.filter(user=user)
        page = self.paginate_queryset(subscriptions)
        if page is not None:
            serializer = SubscriptionSerializer(page, many=True,
                                                context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionSerializer(subscriptions, many=True,
                                            context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated]
            )
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)

        if request.method == 'POST':
            recipes_limit = request.query_params.get('recipes_limit', 5)

            if user == author:
                return Response(
                    {'detail': 'Вы не можете подписаться на себя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            existing_subscription = Subscribe.objects.filter(
                user=user,
                author=author
            ).first()

            if existing_subscription:
                serializer = SubscriptionSerializer(
                    existing_subscription,
                    context={'request': request,
                             'recipes_limit': int(recipes_limit)}
                )
                return Response(serializer.data,
                                status=status.HTTP_400_BAD_REQUEST)

            subscription = Subscribe(user=user, author=author)
            subscription.save()

            serializer = SubscriptionSerializer(
                subscription,
                context={'request': request,
                         'recipes_limit': int(recipes_limit)}
            )
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        subscription = Subscribe.objects.filter(
            user=user, author=author).first()

        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'detail': 'Вы не подписаны на этого пользователя.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class RecipeViewSet(ModelViewSet):
    """Вьюсет операций с рецептами."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['get'],
        url_path='get-link',
    )
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_url = request.build_absolute_uri(f"/recipes/{recipe.id}/")
        s = pyshorteners.Shortener()
        short_link = s.tinyurl.short(recipe_url)
        return Response({'short-link': short_link}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(FavoriteRecipe, request.user, pk)
        return self.delete_from(FavoriteRecipe, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        return self.delete_from(ShoppingCart, request.user, pk)

    def get_recipe_or_404(self, pk):
        try:
            return Recipe.objects.get(id=pk)
        except Recipe.DoesNotExist:
            return Response(
                {'error': 'Not Found: Рецепт не существует.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def add_to(self, model, user, pk):
        recipe_or_response = self.get_recipe_or_404(pk)
        if isinstance(recipe_or_response, Response):
            return recipe_or_response
        if model.objects.filter(user=user, recipe=recipe_or_response).exists():
            return Response(
                {'error': 'Рецепт уже добавлен в корзину!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        model.objects.create(user=user, recipe=recipe_or_response)
        serializer = RecipeShortSerializer(recipe_or_response)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        recipe_or_response = self.get_recipe_or_404(pk)
        if isinstance(recipe_or_response, Response):
            return recipe_or_response
        obj = model.objects.filter(
            user=user, recipe=recipe_or_response
        ).first()
        if not obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_user_shopping_cart_ingredients(self, user):
        return RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(total_amount=Sum('amount'))

    def aggregate_ingredient_amount(self, ingredients):
        return ingredients

    def format_ingredient_line(self, ingredient):
        return (
            f'- {ingredient["ingredient__name"]}'
            f' ({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["total_amount"]}'
        )

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user

        if not user.shopping_cart.exists():
            return Response(
                {'error': 'Корзина покупок пуста.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_ingredients = self.get_user_shopping_cart_ingredients(user)
        agg_ing = self.aggregate_ingredient_amount(user_ingredients)
        name = f'shopping_list_for_{user.get_username()}.txt'
        shopping_list = f'Что купить для {user.get_username()}:\n'
        shopping_list += '\n'.join(
            [self.format_ingredient_line(ingredient) for ingredient in agg_ing]
        )

        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{name}"'

        return response


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    search_fields = ['^name', ]
    filter_backends = [IngredientFilter, ]


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для тегов."""
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None
