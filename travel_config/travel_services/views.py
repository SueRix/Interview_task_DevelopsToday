from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import TravelProject, Place
from .serializers import TravelProjectSerializer, PlaceSerializer
from .services import delete_travel_project, add_place_to_project


class TravelProjectViewSet(viewsets.ModelViewSet):
    # prefetch_related prevents N+1 query problem when serializing places
    queryset = TravelProject.objects.prefetch_related('places').all()
    serializer_class = TravelProjectSerializer

    def destroy(self, request, *args, **kwargs):
        # Delegate deletion rules to the service layer
        instance = self.get_object()
        delete_travel_project(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        # Isolate places strictly to the project specified in the URL
        return Place.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        # Fetch the parent project and delegate creation to the service layer
        project = get_object_or_404(TravelProject, pk=self.kwargs['project_pk'])
        add_place_to_project(project, serializer.validated_data)