from rest_framework import serializers
from rest_framework.validators import ValidationError

from core.constants import MIN_SCORE, MAX_SCORE
from core.serializers import AuthorSerializer
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'year', 'genre',
                  'category', 'description', 'rating')
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(AuthorSerializer):

    class Meta(AuthorSerializer.Meta):
        model = Review
        read_only_fields = ('title', )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data

        if Review.objects.filter(
            author=request.user,
            title=self.context['view'].kwargs.get('title_id')
        ).exists():
            raise serializers.ValidationError(
                'К одному произведению можно оставить один отзыв.'
            )
        return data

    def validate_score(self, value):
        if value not in range(MIN_SCORE, MAX_SCORE + 1):
            raise ValidationError(f'Оцените от {MIN_SCORE} до {MAX_SCORE}.')
        return value


class CommentSerializer(AuthorSerializer):

    class Meta(AuthorSerializer.Meta):
        model = Comment
        read_only_fields = ('review', )
