from dataclasses import dataclass
from decimal import Decimal

from django.utils.functional import cached_property

from mortgage.models import MortgageCalculation


@dataclass(frozen=True)
class MortgageService:
    purchase_price: Decimal
    interest_rate: Decimal
    down_payment_in_dollars: Decimal | None
    down_payment_in_percents: Decimal | None
    mortgage_term: str

    @cached_property
    def mortgage_term_in_months(self):
        """
        Converts mortgage term from 'term years/months' to decimal representation of months
        """

        mortgage_term = self.mortgage_term
        is_in_years = 'year' in mortgage_term
        if is_in_years:
            mortgage_term = mortgage_term.replace('year', '')
        else:
            mortgage_term = mortgage_term.replace('month', '')

        mortgage_term = mortgage_term.replace('s', '')  # Replace for plural name of month and year
        mortgage_term = mortgage_term.replace(' ', '')  # Cleans spaces for case

        value = Decimal(mortgage_term)

        if is_in_years:
            value *= 12  # Converts to months

        return value

    @cached_property
    def monthly_interest_rate(self):
        """
        Converts interest_rate from yearly numeric to monthly numeric representation
        """
        return self.numeric_interest_rate / 12

    @cached_property
    def total_amount(self):
        return self.monthly_payment * self.mortgage_term_in_months

    @cached_property
    def total_over_loan_term(self):
        return self.total_amount - self.present_value

    @cached_property
    def present_value(self):
        if self.down_payment_in_dollars is not None:
            return self.purchase_price - self.down_payment_in_dollars
        if self.down_payment_in_percents is not None:
            return self.purchase_price * (1 - self.down_payment_in_percents / 100)

    @cached_property
    def numeric_interest_rate(self):
        return self.interest_rate / 100

    @cached_property
    def monthly_payment(self):
        return (
            self.present_value
            * self.monthly_interest_rate
            / (1 - (1 + self.monthly_interest_rate) ** (-1 * self.mortgage_term_in_months))
        )

    def calculate_mortgage(self) -> MortgageCalculation:
        return MortgageCalculation.objects.create(
            mortgage_term_in_months=self.mortgage_term_in_months,
            monthly_payment=self.monthly_payment,
            interest_rate=self.numeric_interest_rate,
            total_amount=self.total_amount,
            total_over_loan_term=self.total_over_loan_term,
        )
