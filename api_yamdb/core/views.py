from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdmin, IsModerator, IsAuthor, ReadOnly


class DefaultPaginationViewSet(ModelViewSet):
    """Вьюсет c пагинацией по умолчанию."""
    pagination_class = LimitOffsetPagination


class AdminModeratorAuthorOrReadOnlyViewSet(ModelViewSet):
    """Вьюсет с доступом админиистратора, модератора, автора или для чтения."""
    permission_classes = (IsAdmin | IsModerator | IsAuthor | ReadOnly, )
