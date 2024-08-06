from django.contrib import admin
from django.contrib.admin import display

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Subscribe, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка для ингредиентов."""
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка для тегов."""
    list_display = ('name', 'color', 'slug',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка для рецептов."""
    list_display = ('name', 'id', 'author', 'added_in_favorites')
    readonly_fields = ('added_in_favorites',)
    list_filter = ('author', 'name', 'tags',)

    @display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(RecipeIngredient)
class IngredientInRecipe(admin.ModelAdmin):
    """Админка для промежуточной модели ингредиент - рецепт."""
    list_display = ('recipe', 'ingredient', 'amount',)


@admin.register(FavoriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка для Избранного."""
    list_display = ('user', 'recipe',)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Админка для подписок."""
    list_display = ('user', 'author',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админка для корзины покупок."""
    list_display = ('user', 'recipe',)
