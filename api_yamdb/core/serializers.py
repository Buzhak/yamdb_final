from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        SlugRelatedField)


class AuthorSerializer(ModelSerializer):
    """Сериалайзер для валидации текущего пользователя как автора."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
