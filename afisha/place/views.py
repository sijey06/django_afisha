from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Place


def index(request):
    """Метод для отображения главной страницы."""

    places_geojson = {"type": "FeatureCollection", "features": []}
    places = Place.objects.all()
    for place in places:
        places_geojson["features"].append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [place.coordinates_lng,
                                    place.coordinates_lat],
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.slug,
                    "detailsUrl": reverse(
                        "places-place-json", args=(place.pk,)),
                },
            }
        )
    return render(request, "index.html",
                  context={"places_geojson": places_geojson})


def get_place_json(request, place_id):
    """Метод для загрузки данных мест в формате JSON."""

    place = get_object_or_404(Place, id=place_id)
    images = place.images.all().order_by("order_num")
    images_urls = [image.image.url for image in images]
    place_context = {
        "title": place.title,
        "imgs": images_urls,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": f"{place.coordinates_lng}",
            "lat": f"{place.coordinates_lat}",
        },
    }
    return JsonResponse(
        place_context,
        safe=False,
        json_dumps_params={"ensure_ascii": False, "indent": 2},
    )
