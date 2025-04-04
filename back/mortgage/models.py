from django.db import models

from common.models import BaseModel


class MortgageCalculation(BaseModel):
    mortgage_term_in_months = models.IntegerField()
    monthly_payment = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=7, decimal_places=4)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    total_over_loan_term = models.DecimalField(max_digits=15, decimal_places=2)
