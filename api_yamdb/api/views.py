from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView


from core.constants import CODE_LENGTH
from core.views import (DefaultPaginationViewSet,
                        AdminModeratorAuthorOrReadOnlyViewSet)
from reviews.models import Category, Genre, Review, Title
from users.models import User, Code
from users.serializers import UserCodeSerializer, UserSerializer
from .core import get_code, send_email, get_tokens_for_user
from .filters import TitleFilter
from .mixins import CreateDestroyListViewSet
from .permissions import IsAdmin, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          )


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdmin | ReadOnly, )


class GenresViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdmin | ReadOnly, )


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    search_fields = ('genre__slug',)
    filterset_fields = ('genre__slug',)
    permission_classes = (IsAdmin | ReadOnly, )

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreateSerializer
        return TitleListSerializer


class ReviewViewSet(DefaultPaginationViewSet,
                    AdminModeratorAuthorOrReadOnlyViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(DefaultPaginationViewSet,
                     AdminModeratorAuthorOrReadOnlyViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class Sign_up(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(
                User,
                username=serializer.data['username']
            )
            random_code = get_code(CODE_LENGTH)
            confirmation_code = Code(code=random_code, user=user)
            confirmation_code.save()
            send_email(
                serializer.data['email'],
                str(confirmation_code),
                str(user.username)
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Token(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = get_object_or_404(
                Code,
                code=serializer.data['confirmation_code']
            )
            token = get_tokens_for_user(code.user)
            return Response(token, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
