from django.db import models
from django.utils import timezone


class Blog(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название заголовка",
        help_text="Введите название заголовка",
    )
    slug = models.CharField(
        max_length=100,
        verbose_name="url-адрес",
        null=True,
        blank=True,
    )
    content = models.TextField(
        max_length=5000,
        verbose_name="Содержимое",
        help_text="Описание блога",
    )
    preview = models.ImageField(
        upload_to='imgproduct/',
        blank=True,
        null=True,
        verbose_name='Фото',
        help_text='Загрузите фото',
    )
    created_date = models.DateTimeField(
        verbose_name='Дата создания',
        default=timezone.now,
    )
    published = models.BooleanField(
        verbose_name='Признак публикации',
        default=True,
    )
    views_counter = models.PositiveIntegerField(
        verbose_name='Количество просмотров',
        default=0
    )

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'

    def __str__(self):
        return self.title


