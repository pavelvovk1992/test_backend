from django.urls import path

from api_backend.views import UserViewSet, ParticipantMatchViewSet
# ParticipantMatchViewSet

urlpatterns = [
    path('clients/create/', UserViewSet.as_view({'post': 'create'})),
    # path('clients/list/', ParticipantViewSet.as_view({'get': 'list'})),
    # path('clients/<int:pk>/', ParticipantViewSet.as_view({'get': 'retrieve'})),
    path('clients/<int:pk>/match/', ParticipantMatchViewSet.as_view({'post': 'create'}))
    # path('clients/<int:pk>/match/', ParticipantMatchViewSet.as_view()),
]
