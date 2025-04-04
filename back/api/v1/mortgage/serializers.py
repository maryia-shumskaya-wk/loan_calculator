import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from mortgage.models import MortgageCalculation

MORTGAGE_TERM_REGEX = re.compile(r"\d{1,13}(\.\d*)? (month|year)s?")


class CreateMortgageCalculationSerializer(serializers.Serializer):
    purchase_price = serializers.DecimalField(
        write_only=True,
        max_digits=15,
        decimal_places=2,
        min_value=0,
    )
    interest_rate = serializers.DecimalField(
        write_only=True,
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )  # I understand that interest rate could be above 100, but it's nonsense
    down_payment_in_dollars = serializers.DecimalField(
        write_only=True,
        max_digits=15,
        decimal_places=2,
        min_value=0,
        required=False,
        allow_null=True,
    )
    down_payment_in_percents = serializers.DecimalField(
        write_only=True,
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
        allow_null=True,
    )
    mortgage_term = serializers.RegexField(
        regex=MORTGAGE_TERM_REGEX,
        max_length=23,
    )

    def validate(self, attrs):
        down_payment_in_percents = attrs.get('down_payment_in_percents')
        down_payment_in_dollars = attrs.get('down_payment_in_dollars')
        down_payments = [down_payment_in_percents, down_payment_in_dollars]
        if all(down_payments):
            raise ValidationError('You must specify only one of the down payments')
        if not any(down_payments):
            raise ValidationError('Please specify only one of the down payments')

        purchase_price = attrs.get('purchase_price')
        if down_payment_in_dollars and purchase_price <= down_payment_in_dollars:
            raise ValidationError('Down payment cannot be more than purchase price')

        return attrs


class ListGetMortgageCalculationSerializer(serializers.ModelSerializer):
    mortgage_term = serializers.SerializerMethodField()

    class Meta:
        model = MortgageCalculation
        fields = (
            'id',
            'mortgage_term',
            'monthly_payment',
            'interest_rate',
            'total_amount',
            'total_over_loan_term',
        )
        read_only_fields = (
            'id',
            'mortgage_term',
            'monthly_payment',
            'interest_rate',
            'total_amount',
            'total_over_loan_term',
        )

    def get_mortgage_term(self, instance: MortgageCalculation):
        return instance.mortgage_term_in_months / 12
