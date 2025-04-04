from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.mortgage.views import MortgageViewSet

router = DefaultRouter()

router.register("mortgage", MortgageViewSet, basename="api-v1-mortgage")

urlpatterns = [
    path('', include(router.urls)),
]
