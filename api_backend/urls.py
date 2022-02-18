from django.urls import path

from api_backend.views import ParticipantViewSet, ParticipantMatchViewSet


urlpatterns = [
    path('clients/create/', ParticipantViewSet.as_view({'post': 'create'})),
    path('list/', ParticipantViewSet.as_view({'get': 'list'})),
    path('clients/<int:pk>/match/', ParticipantMatchViewSet.as_view({'post': 'create'}))

]
