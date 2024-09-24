from django.db import models
from django.utils import timezone

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="наименование",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        max_length=1000, verbose_name="описание", help_text="Введите описание категории",
    )

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ("name",)


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="наименование",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        max_length=1000, verbose_name="описание", help_text="Введите описание продукта",
    )
    img_preview = models.ImageField(
        upload_to="imgproduct/",
        blank=True,
        null=True,
        verbose_name="изображение",
        help_text="Загрузите фото продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="категория",
        help_text="Введите категорию товара",
        related_name="products",
    )
    price = models.PositiveIntegerField(
        verbose_name="цена за покупку", help_text="Введите цену продукта"
    )
    created_at = models.DateTimeField(
        verbose_name="дата создания", default=timezone.now
    )
    last_modified_date = models.DateTimeField(
        verbose_name="дата последнего изменения", default=timezone.now
    )
    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Введите колличество просмотров",
        default=0)
    is_published = models.BooleanField(default=False, verbose_name="опубликовано")
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    manufacturer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Производитель",
                                     null=True, blank=True)


    def __str__(self):
        return f"{self.name} {self.description} {self.price} {self.category}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = [
            "name",
            "category",
        ]
        permissions = [
            ("can_edit_category", "Can edit category"),
            ("can_edit_description", "Can edit description"),
            ("can_edit_is_published", "Can edit is_published")
        ]


class Version(models.Model):
    product = models.ForeignKey(Product,
                                related_name="versions",
                                on_delete=models.SET_NULL,
                                null=True, blank=True,
                                verbose_name="продукт")
    version_number = models.PositiveIntegerField(default=0, verbose_name="номер версии")
    version_name = models.CharField(max_length=100, verbose_name="название версии")
    version_flag = models.BooleanField(default=True, verbose_name="актуальная версия")

    def __str__(self):
        return f"{self.product} {self.version_number} {self.version_name} {self.version_flag}"

    class Meta:
        verbose_name = "версия продукта"
        verbose_name_plural = "версии продуктов"


