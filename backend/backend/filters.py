from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag

User = get_user_model()


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    is_in_purchase = filters.BooleanFilter(
        method='filter_is_in_purchase'
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_in_purchase',
                  'is_favorited', 'is_in_shopping_cart')

    def is_user_anonymous(self):
        return self.request.user.is_anonymous

    def filter_is_in_purchase(self, queryset, name, value):
        if value and not self.is_user_anonymous():
            return queryset.filter(purchase__user=self.request.user)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.is_user_anonymous():
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.is_user_anonymous():
            return queryset.filter(shopping_cart__isnull=False)
        return queryset.filter(shopping_cart__isnull=True)
