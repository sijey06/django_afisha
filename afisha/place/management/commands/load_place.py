import os

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
import requests
from requests.compat import urlparse

from place.models import Image, Place
from place.utils import get_slug


def save_place_image(place, image_url, order_num):
    """Скачивание изображения по указанному URL и привязывание его к месту."""
    filename = os.path.basename(urlparse(image_url).path)
    image = Image(place=place, order_num=order_num)

    img_response = requests.get(image_url)
    img_response.raise_for_status()

    image.image.save(filename, ContentFile(img_response.content), save=False)
    image.save()


class Command(BaseCommand):
    """Команда для загрузки данных о местах и изображениях из JSON-файлов."""

    help = "Загружает данные о местах из указанного JSON."

    def add_arguments(self, parser):
        parser.add_argument("urls", nargs="+", type=str)

    def handle(self, *args, **options):
        for url in options["urls"]:
            try:
                resp = requests.get(url=url)
                resp.raise_for_status()
            except requests.exceptions.HTTPError as err:
                self.stdout.write(self.style.NOTICE(err))
                continue
            except requests.exceptions.ConnectionError as err:
                self.stdout.write(self.style.NOTICE(err))
                continue
            try:
                place_raw = resp.json()
            except requests.exceptions.JSONDecodeError:
                self.stdout.write(
                    self.style.NOTICE(
                        f"Указанный URL {url} не содержит JSON-данные.")
                )
                continue
            place, created = Place.objects.get_or_create(
                title=place_raw["title"],
                coordinates_lng=place_raw["coordinates"]["lng"],
                coordinates_lat=place_raw["coordinates"]["lat"],
                defaults={
                    "slug": get_slug(place_raw["title"]),
                    "description_short": place_raw["description_short"],
                    "description_long": place_raw["description_long"],
                },
            )
            if created:
                for i, image_url in enumerate(place_raw["imgs"], 1):
                    try:
                        save_place_image(place,
                                         image_url=image_url, order_num=i)
                    except requests.exceptions.HTTPError as err:
                        self.stdout.write(self.style.NOTICE(err))
                        continue
                    except requests.exceptions.ConnectionError as err:
                        self.stdout.write(self.style.NOTICE(err))
                        continue

                    self.stdout.write(
                        self.style.SUCCESS(f"Изображение №{i} для места"
                                           f"{place_raw['title']}"
                                           "успешно сохранено.")
                    )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Место {place_raw['title']} успешно создано.")
                )
            else:
                self.stdout.write(
                    self.style.NOTICE(
                        f"Место {place_raw['title']} уже существует в БД.")
                )
