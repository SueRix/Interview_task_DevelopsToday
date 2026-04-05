from django.urls import path
from .views import TravelProjectViewSet, PlaceViewSet

# Explicit view bindings for standard REST actions
project_list = TravelProjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
project_detail = TravelProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

place_list = PlaceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
place_detail = PlaceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    # Project routes
    path('projects/', project_list, name='project-list'),
    path('projects/<int:pk>/', project_detail, name='project-detail'),

    # Nested Place routes
    path('projects/<int:project_pk>/places/', place_list, name='place-list'),
    path('projects/<int:project_pk>/places/<int:pk>/', place_detail, name='place-detail'),
]