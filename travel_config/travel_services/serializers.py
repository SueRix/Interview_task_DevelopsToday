from rest_framework import serializers
from .models import TravelProject, Place
from .services import validate_place_exists_in_api, create_travel_project


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'external_id', 'notes', 'is_visited']

    @staticmethod
    def validate_external_id(value):
        if not validate_place_exists_in_api(value):
            raise serializers.ValidationError("Place not found in external API.")
        return value


class TravelProjectSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, required=False)
    is_completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = TravelProject
        fields = ['id', 'name', 'description', 'start_date', 'places', 'is_completed']

    @staticmethod
    def validate_places(places_data):
        if places_data and len(places_data) > 10:
            raise serializers.ValidationError("Maximum 10 places allowed per project.")

        external_ids = [p.get('external_id') for p in places_data]
        if len(external_ids) != len(set(external_ids)):
            raise serializers.ValidationError("Duplicate external IDs in request.")

        return places_data

    def create(self, validated_data: dict) -> TravelProject:
        return create_travel_project(validated_data)