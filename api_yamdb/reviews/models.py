from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import TextModel
from core.constants import MIN_SCORE, MAX_SCORE


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.PositiveSmallIntegerField('Год выхода')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры',
    )
    description = models.TextField(
        'Описание произведения',
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='Жанры'
    )

    def __str__(self):
        return f'{self.title} {self.genre}'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Review(TextModel):
    REVIEW_DISPLAY = (
        'id: {id}, '
        'Автор: {author}, '
        'Произведение: {title}, '
        'Оценка: {score}, '
        'Отзыв: {text:.20},  '
        'Дата: {pub_date:"%d-%m-%Y"}'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)]
    )

    class Meta(TextModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author_id', 'title_id'),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.REVIEW_DISPLAY.format(
            id=self.id,
            author=self.author,
            title=self.title,
            score=self.score,
            text=self.text,
            pub_date=self.pub_date
        )


class Comment(TextModel):
    COMMENT_DISPLAY = (
        'id: {id}, '
        'Дата: {pub_date:"%d-%m-%Y"}, '
        'Автор: {author}, '
        'Отзыв: {review.text:.20}, '
        'Комментарий: {text:.20}'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(TextModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.COMMENT_DISPLAY.format(
            id=self.id,
            pub_date=self.pub_date,
            author=self.author,
            review=self.review,
            text=self.text
        )
