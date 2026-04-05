import requests
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import TravelProject, Place


def validate_place_exists_in_api(external_id: str):
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        raise ValidationError({"detail": "External API is unreachable."})


@transaction.atomic
def create_travel_project(validated_data: dict):
    places_data = validated_data.pop('places', [])
    project = TravelProject.objects.create(**validated_data)

    # Use bulk_create for better database performance
    places_to_create = [
        Place(project=project, **place_data)
        for place_data in places_data
    ]
    if places_to_create:
        Place.objects.bulk_create(places_to_create)

    return project


def delete_travel_project(project: TravelProject) -> None:
    if project.places.filter(is_visited=True).exists():
        raise ValidationError({"detail": "Cannot delete project with visited places."})
    project.delete()


def add_place_to_project(project: TravelProject, validated_data: dict):
    # Enforce maximum 10 places limit
    if project.places.count() >= 10:
        raise ValidationError({"detail": "Maximum 10 places allowed per project."})

    return Place.objects.create(project=project, **validated_data)