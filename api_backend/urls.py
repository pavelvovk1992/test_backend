from django.urls import path

from api_backend.views import UserViewSet


urlpatterns = [
    path('clients/create/', UserViewSet.as_view({'post': 'create'})),
]
