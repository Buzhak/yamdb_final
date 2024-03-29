from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

DATA_PATH = '/static/data/'
SCV = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv'
}


class Command(BaseCommand):
    '''Загрузка тестовых данных из csv в БД.'''
    def handle(self, *args, **kwargs):
        for model, file in SCV.items():
            with open(f'{settings.BASE_DIR}{DATA_PATH}{file}',
                      'r', encoding='utf-8') as csv_file:
                reader = DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Successfully load data'))
