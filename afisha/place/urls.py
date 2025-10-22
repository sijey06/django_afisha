from django.urls import path

from .views import get_place_json, index


urlpatterns = [
    path("", index, name="index"),
    path("places/<int:place_id>/", get_place_json, name="places-place-json"),
]
