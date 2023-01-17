from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(TagsAdmin):
    ...


@admin.register(Genre)
class GenreAdmin(TagsAdmin):
    ...


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    model = Title.genre.through


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'pub_date', 'text', 'review')
    search_fields = ('text', )
    list_filter = ('pub_date', 'author')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'pub_date', 'text', 'title')
    search_fields = ('text', )
    list_filter = ('pub_date', 'author')
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'name', 'category', 'description')
    search_fields = ('name', 'description')
    list_filter = ('category', 'genre', 'year')
    empty_value_display = '-пусто-'
