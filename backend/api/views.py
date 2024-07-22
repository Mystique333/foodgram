import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
import pyshorteners

from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredients, ShoppingCart, Subscribe, Tag)

from backend.filters import IngredientFilter, RecipeFilter
from backend.pagination import CustomPagination
from backend.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeShortSerializer, RecipeWriteSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UsersSerializer, UserAvatarSerializer,
                          SetPasswordSerializer)

User = get_user_model()


class UsersViewSet(ModelViewSet):
    """Вьюсет для пользователей и подписок."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    @action(detail=False, methods=['put', 'patch', 'delete', 'get'], url_path='me/avatar', permission_classes=[IsAuthenticated])
    def avatar(self, request):
        user = request.user
        if request.method in ['PUT', 'PATCH']:
            if 'avatar' not in request.data:
                return Response({'detail': 'Поле avatar обязательно.'}, status=status.HTTP_400_BAD_REQUEST)
                
            serializer = UserAvatarSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            if user.avatar:
                user.avatar.delete()
                user.avatar = None
                user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'GET':
            if user.avatar:
                return Response({'avatar': request.build_absolute_uri(user.avatar.url)})
            return Response({'message': 'Avatar not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], url_path='set_password', permission_classes=[IsAuthenticated])
    def set_password(self, request):
        user = request.user
        current_password_input = request.data.get('current_password')
        new_password = request.data.get('new_password')

        # Проверяем, что переданы оба пароля
        if not current_password_input or not new_password:
            return Response({'error': 'Требуется указать текущий и новый пароли.'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем текущий пароль
        if not check_password(current_password_input, user.password):
            return Response({'current_password': ['Текущий пароль неверен.']}, status=status.HTTP_400_BAD_REQUEST)

        # Устанавливаем новый пароль и сохраняем пользователя
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Пароль успешно изменен.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='subscriptions', permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscribe.objects.filter(user=user)
        page = self.paginate_queryset(subscriptions)
        if page is not None:
            serializer = SubscriptionSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionSerializer(subscriptions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)

        if request.method == 'POST':
            recipes_limit = request.query_params.get('recipes_limit', 5)

            if user == author:
                return Response({'detail': 'Вы не можете подписаться на себя.'}, status=status.HTTP_400_BAD_REQUEST)

            if Subscribe.objects.filter(user=user, author=author).exists():
                serializer = SubscriptionSerializer(author, context={'request': request, 'recipes_limit': int(recipes_limit)})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            subscription = Subscribe(user=user, author=author)
            subscription.save()

            serializer = SubscriptionSerializer(author, context={'request': request, 'recipes_limit': int(recipes_limit)})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            subscription = Subscribe.objects.filter(user=user, author=author).first()

            if subscription:
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'Вы не подписаны на этого пользователя.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Метод не поддерживается'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        eprint("ЧТО_ТО ПОШЛО НЕ ТАК !!!!!!!!!!!!!!!!!")
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class RecipeViewSet(ModelViewSet):
    """Вьюсет для рецептов и операций с ними."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        eprint(request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            eprint(serializer.errors)
            if 'ingredients' in e.get_full_details():
                return Response(
                    {'error': 'Bad Request: Поле "ingredients" пустое.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'error': 'Bad Request'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        recipe = serializer.instance
        read_serializer = RecipeReadSerializer(recipe, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        instance = serializer.instance
        self.check_object_permissions(self.request, instance)
        super().perform_update(serializer)

    def update(self, request, *args, **kwargs):
        return self.update_instance(request, partial=False, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update_instance(request, partial=True, **kwargs)

    def update_instance(self, request, partial, **kwargs):
        instance = self.get_object()
        eprint(f"User: {request.user}, Author: {instance.author}!!!!!!!!")
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        eprint('ВЫЗВАН WRITE SERIALIZEER!!!!!!!!!!!!!!!!!!!!!!!')
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

    def add_to(self, model, user, pk):
        try:
            recipe = Recipe.objects.get(id=pk)
        except Recipe.DoesNotExist:
            return Response(
                {'error': 'Not Found: Рецепт не существует.'},
                status=status.HTTP_404_NOT_FOUND  # Изменяем статус код на 404
            )
        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'error': 'Рецепт уже добавлен в корзину!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        try:
            recipe = Recipe.objects.get(id=pk)
        except Recipe.DoesNotExist:
            return Response(
                {'error': 'Not Found: Рецепт не существует.'},
                status=status.HTTP_404_NOT_FOUND
            )

        obj = model.objects.filter(user=user, recipe=recipe).first()
        if not obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        def get_user_shopping_cart_ingredients():
            return RecipeIngredients.objects.filter(
                recipe__shopping_cart__user=request.user
            ).values(
                'ingredient__name',
                'ingredient__measurement_unit'
            )

        def aggregate_ingredient_amount(ingredients):
            return ingredients.annotate(amount=Sum('amount'))

        def format_ingredient_line(ingredient):
            return (
                f'- {ingredient["ingredient__name"]}'
                f'({ingredient["ingredient__measurement_unit"]})'
                f'- {ingredient["amount"]}'
            )

        user_ingredients = get_user_shopping_cart_ingredients()
        agg_ing = aggregate_ingredient_amount(user_ingredients)
        name = f'shopping_list_for_{user.get_username}.txt'
        shopping_list = f'Что купить для {user.get_username()}:\n'
        shopping_list += '\n'.join(
            [format_ingredient_line(ingredient) for ingredient in agg_ing]
        )

        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={name}'

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
