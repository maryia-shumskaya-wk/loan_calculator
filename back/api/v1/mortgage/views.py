from django.db.models import Model
from rest_framework.serializers import Serializer

from api.v1.mortgage.serializers import (
    CreateMortgageCalculationSerializer,
    ListGetMortgageCalculationSerializer,
)
from common.viewset import (
    SeparateRequestAndResponseSerializerCreateModelMixin,
    SeparateRequestAndResponseSerializerListModelMixin,
    SeparateRequestAndResponseSerializersGenericViewSet,
)
from mortgage.models import MortgageCalculation
from mortgage.services.mortgage_service import MortgageService


class MortgageViewSet(
    SeparateRequestAndResponseSerializersGenericViewSet,
    SeparateRequestAndResponseSerializerCreateModelMixin,
    SeparateRequestAndResponseSerializerListModelMixin,
):
    queryset = MortgageCalculation.objects.all()

    request_serializers_by_action = {
        "create": CreateMortgageCalculationSerializer,
    }
    response_serializers_by_action = {
        "create": ListGetMortgageCalculationSerializer,
        "list": ListGetMortgageCalculationSerializer,
    }

    def perform_create(self, serializer: Serializer) -> Model:
        validated_data = serializer.validated_data
        (
            purchase_price,
            interest_rate,
            down_payment_in_dollars,
            down_payment_in_percents,
            mortgage_term,
        ) = (
            validated_data["purchase_price"],
            validated_data["interest_rate"],
            validated_data.get("down_payment_in_dollars"),
            validated_data.get("down_payment_in_percents"),
            validated_data["mortgage_term"],
        )
        return MortgageService(
            purchase_price=purchase_price,
            interest_rate=interest_rate,
            down_payment_in_dollars=down_payment_in_dollars,
            down_payment_in_percents=down_payment_in_percents,
            mortgage_term=mortgage_term,
        ).calculate_mortgage()
