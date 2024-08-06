from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from backend.constants import MIN_VALUE, MAX_VALUE

User = get_user_model()


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        'Название',
        max_length=25,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        max_length=25,
        unique=True,
        db_index=False
    )
    slug = models.SlugField(
        'Слаг',
        max_length=25,
        unique=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name} ({self.color})'


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        'Название',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        null=True
    )
    name = models.CharField(
        'Название рецепта',
        max_length=199
    )
    image = models.ImageField(
        'Изображение рецепта',
        upload_to='static/recipe/',
        blank=True,
        null=True
    )
    text = models.TextField(
        'Описание рецепта',
        max_length=1000
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                MIN_VALUE,
                message='Время приготовления не менее 1 минуты!'
            ),
            MaxValueValidator(
                MAX_VALUE,
                message='Время приготовления не более 32000 минут!'
            ),
        ],
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        through='RecipeIngredient',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        author_name = self.author.username if self.author else "Unknown Author"
        return f"{self.name} by {author_name}"


class RecipeIngredient(models.Model):
    """Промежуточная модель рецепт - ингредиент."""
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                MIN_VALUE,
                message='Время приготовления не менее 1 минуты!'
            ),
            MaxValueValidator(
                MAX_VALUE,
                message='Время приготовления не более 32000 минут!'
            ),
        ],
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Ингредиент'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количество ингредиентов в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient')
        ]

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Subscribe(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор')
    created_at = models.DateTimeField(
        'Дата подписки',
        auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author')
        ]

    def __str__(self):
        return f'Пользователь {self.user} -> автор {self.author}'


class ShoppingCart(models.Model):
    """ Модель Корзины покупок """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} -> {self.recipe}"


class FavoriteRecipe(models.Model):
    """Модель избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe')
        ]

    def __str__(self):
        return f'Избранный {self.recipe} у {self.user}'
