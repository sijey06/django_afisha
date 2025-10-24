from django.db import models
from django.db.models import Max
from tinymce.models import HTMLField

from .constants import MAX_LENGTH_TITLE
from .utils import get_slug


class Place(models.Model):
    """Модель места."""

    title = models.CharField(verbose_name="Название",
                             max_length=MAX_LENGTH_TITLE)
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description_short = models.TextField(verbose_name="Короткое описание",
                                         blank=True)
    description_long = HTMLField(verbose_name="Полное описание", blank=True)
    coordinates_lat = models.FloatField(
        verbose_name="Широта",
    )
    coordinates_lng = models.FloatField(
        verbose_name="Долгота",
    )

    class Meta:
        verbose_name = "Место города"
        verbose_name_plural = "Места города"
        ordering = ("title",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or len(self.slug.strip()) == 0:
            self.slug = get_slug(self.title)
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.order_num is None:
            last_order = (
                Image.objects.filter(place=self.place)
                .aggregate(max_order=Max('order_num'))
                .get('max_order') or 0
            )
            self.order_num = last_order + 1
        super().save(*args, **kwargs)
