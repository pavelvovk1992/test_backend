from django.urls import path, include
from api_backend.views import ParticipantViewSet, ParticipantMatchViewSet


urlpatterns = [
    path('clients/create/', ParticipantViewSet.as_view({'post': 'create'})),
    path('clients/<int:pk>/delete/', ParticipantViewSet.as_view({'post': 'destroy'})),
    path('clients/<int:pk>/', ParticipantViewSet.as_view({'get': 'retrieve'}), name='client-detail'),
    path('clients/list/', ParticipantViewSet.as_view({'get': 'list'}), name='clients-list'),

    path('clients/<int:pk>/match/', ParticipantMatchViewSet.as_view({'post': 'create'}), name='create-match'),
    path('clients/match/<int:pk>/delete/', ParticipantMatchViewSet.as_view({'post': 'destroy'})),

]
