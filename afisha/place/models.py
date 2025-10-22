from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    """Модель места."""

    title = models.CharField(verbose_name="Название", max_length=60)
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description_short = models.TextField(verbose_name="Короткое описание",
                                         blank=True)
    description_long = HTMLField(verbose_name="Полное описание", blank=True)
    coordinates_lng = models.FloatField(
        verbose_name="Долгота",
    )
    coordinates_lat = models.FloatField(
        verbose_name="Широта",
    )

    class Meta:
        verbose_name = "Место города"
        verbose_name_plural = "Места города"
        ordering = ("title",)

    def __str__(self):
        return self.title


class Image(models.Model):
    """Модель картинки места."""

    place = models.ForeignKey(
        Place,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Место",
    )

    order_num = models.PositiveIntegerField(verbose_name="Номер", blank=True)

    image = models.ImageField(verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

        ordering = ("order_num",)

    def __str__(self):
        return f"{self.order_num} в {self.place}"
