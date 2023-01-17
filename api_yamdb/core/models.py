from django.db import models
from users.models import User


class TextModel(models.Model):
    """Абстрактная модель. Дата создания, текст, автор."""
    text = models.TextField('Текст', help_text='Введите тескт')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Автор'
    )

    class Meta:
        abstract = True
        ordering = ('pub_date', )
