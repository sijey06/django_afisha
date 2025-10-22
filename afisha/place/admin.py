from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    fields = ('image', 'preview_image')
    readonly_fields = ('preview_image', )
    extra = 1

    def preview_image(self, instance):
        """Метод для отображения превью"""
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="200" />')
        return '(Нет изображения)'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description_short', 'description_long',
                    'coordinates_lng', 'coordinates_lat',)

    inlines = [ImageInline]
