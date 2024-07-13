import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
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

from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredients, ShoppingCart, Subscribe, Tag)

from backend.filters import IngredientFilter, RecipeFilter
from backend.pagination import CustomPagination
from backend.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeShortSerializer, RecipeWriteSerializer,
                          SubscribeSerializer, TagSerializer,
                          UsersSerializer, UserAvatarSerializer)

User = get_user_model()


class UsersViewSet(UserViewSet):
    """Вьюсет для пользователей и подписок."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    @action(detail=False, methods=['put'], url_path='me/avatar', permission_classes=[IsAuthenticated])
    def update_avatar(self, request):
        user = request.user
        eprint("Received PUT request for updating avatar")
        eprint(f"User: {user.username}")
        eprint(f"Request data: {request.data}")
        serializer = UserAvatarSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            print("Data is valid")
            serializer.save()
            return Response(serializer.data)
        print("Data is invalid")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='me/avatar', permission_classes=[IsAuthenticated])
    def delete_avatar(self, request):
        user = request.user
        eprint("Received DELETE request for deleting avatar")
        eprint(f"User: {user.username}")
        if user.avatar:
            user.avatar.delete()
            user.avatar = None
            user.save()
            return Response({'message': 'Avatar deleted successfully'})
        return Response({'message': 'No avatar to delete'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='me/avatar', permission_classes=[IsAuthenticated])
    def get_avatar(self, request):
        user = request.user
        eprint("Received GET request for getting avatar")
        eprint(f"User: {user.username}")
        if user.avatar:
            return Response({'avatar': request.build_absolute_uri(user.avatar.url)})
        return Response({'message': 'Avatar not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author,
                data=request.data,
                context={"request": request}
            )
            try:
                serializer.is_valid(raise_exception=True)
                Subscribe.objects.create(user=user, author=author)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response(
                    {'detail': 'Уже подписан.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        elif request.method == 'DELETE':
            subscription = get_object_or_404(
                Subscribe,
                user=user,
                author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribing__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
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
    """Вьюсет для рецептов и операций с ними."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

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

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        eprint('ВЫЗВАН WRITE SERIALIZEER!!!!!!!!!!!!!!!!!!!!!!!')
        return RecipeWriteSerializer

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
        recipe = get_object_or_404(Recipe, id=pk)
        existing_entry = model.objects.filter(
            user=user,
            recipe=recipe
        ).first()
        if existing_entry:
            return Response(
                {'errors': 'Рецепт уже добавлен в корзину!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = get_object_or_404(model, user=user, recipe__id=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
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
