import pytest
from rest_framework.reverse import reverse

from mortgage.models import MortgageCalculation


@pytest.mark.django_db
class TestMortgageViewSetCreateAction:
    url = reverse("api-v1-mortgage-list")

    @pytest.fixture
    def partial_correct_payload(self) -> dict[str, any]:
        return {
            "purchase_price": 1_200_000,
            "interest_rate": 20,
        }

    @pytest.fixture
    def correct_payload__months_mortgage_term_percents_down_payment(self, partial_correct_payload):
        payload = partial_correct_payload.copy()
        payload["mortgage_term"] = "60 months"
        payload["down_payment_in_percents"] = 15
        return payload

    @pytest.fixture
    def correct_payload__months_mortgage_term_dollars_down_payment(self, partial_correct_payload):
        payload = partial_correct_payload.copy()
        payload["mortgage_term"] = "60 months"
        payload["down_payment_in_dollars"] = 180000
        return payload

    @pytest.fixture
    def correct_payload__years_mortgage_term_dollars_down_payment(self, partial_correct_payload):
        payload = partial_correct_payload.copy()
        payload["mortgage_term"] = "5 years"
        payload["down_payment_in_dollars"] = 180000
        return payload

    @pytest.fixture
    def correct_payload__years_mortgage_term_percents_down_payment(self, partial_correct_payload):
        payload = partial_correct_payload.copy()
        payload["mortgage_term"] = "5 years"
        payload["down_payment_in_percents"] = 15
        return payload

    @pytest.fixture
    def expected_response_with_correct_payload(self):
        return {
            "total_amount": '1621425.68',
            "interest_rate": '0.2000',
            "total_over_loan_term": '601425.68',
            "mortgage_term": 5.0,
            "monthly_payment": "27023.76",
        }

    @pytest.fixture
    def full_payload(self):
        return {
            "purchase_price": 1_200_000,
            "interest_rate": 20,
            "down_payment_in_dollars": 15,
            "mortgage_term": "5 years",
        }

    @pytest.mark.parametrize(
        "payload,expected_response",
        [
            pytest.param(
                pytest.lazy_fixture('correct_payload__months_mortgage_term_percents_down_payment'),
                pytest.lazy_fixture('expected_response_with_correct_payload'),
                id="Correct payload with mortgage term in months and down payment in percents",
            ),
            pytest.param(
                pytest.lazy_fixture('correct_payload__months_mortgage_term_dollars_down_payment'),
                pytest.lazy_fixture('expected_response_with_correct_payload'),
                id="Correct payload with mortgage term in months and down payment in dollars",
            ),
            pytest.param(
                pytest.lazy_fixture('correct_payload__years_mortgage_term_dollars_down_payment'),
                pytest.lazy_fixture('expected_response_with_correct_payload'),
                id="Correct payload with mortgage term in years and down payment in dollars",
            ),
            pytest.param(
                pytest.lazy_fixture('correct_payload__years_mortgage_term_percents_down_payment'),
                pytest.lazy_fixture('expected_response_with_correct_payload'),
                id="Correct payload with mortgage term in years and down payment in percents",
            ),
        ],
    )
    def test_create_view__201_created(self, api_client, payload, expected_response: dict):
        response = api_client.post(self.url, data=payload)
        assert response.status_code == 201
        content = response.json()
        assert all([content[key] == expected_response[key] for key in expected_response.keys()])
        assert MortgageCalculation.objects.count() == 1

    @pytest.mark.parametrize(
        "field_name,value",
        [
            pytest.param(
                "mortgage_term",
                "90",
                id="Mortgage term without period specification",
            ),
            pytest.param(
                "interest_rate",
                110,
                id="Interest above 100%",
            ),
            pytest.param(
                "interest_rate",
                110,
                id="Interest below 0%",
            ),
            pytest.param(
                "purchase_price",
                -10,
                id="Purchase price below 0",
            ),
            pytest.param(
                "down_payment_in_dollars",
                -10,
                id="Down Payment in dollars below 0",
            ),
            pytest.param(
                "down_payment_in_dollars",
                1_300_000,
                id="Down Payment more than purchase price",
            ),
        ],
    )
    def test_create_view__400_bad_request(self, api_client, full_payload, field_name: str, value: any):
        payload = full_payload.copy()
        payload[field_name] = value
        response = api_client.post(self.url, data=payload)
        assert response.status_code == 400
        assert MortgageCalculation.objects.count() == 0


@pytest.mark.django_db
class TestMortgageViewSetListAction:
    url = reverse("api-v1-mortgage-list")

    @pytest.fixture
    def mortgage_calculation_1(self):
        return MortgageCalculation.objects.create(
            mortgage_term_in_months=12,
            total_amount=1000000,
            total_over_loan_term=400000,
            interest_rate=0.02,
            monthly_payment=10000,
        )

    @pytest.fixture
    def mortgage_calculation_2(self):
        return MortgageCalculation.objects.create(
            mortgage_term_in_months=60,
            total_amount=4000000,
            total_over_loan_term=1000000,
            interest_rate=0.04,
            monthly_payment=50000,
        )

    @pytest.fixture
    def mortgage_calculation_3(self):
        return MortgageCalculation.objects.create(
            mortgage_term_in_months=30,
            total_amount=5000000,
            total_over_loan_term=500000,
            interest_rate=0.2,
            monthly_payment=100000,
        )

    def test_list_view__200_ok_no_instances(self, api_client):
        response = api_client.get(self.url)
        content = response.json()
        assert len(content) == 0

    def test_list_view__200_ok_one_instance(self, api_client, mortgage_calculation_1):
        response = api_client.get(self.url)
        content = response.json()
        assert len(content) == 1

    def test_list_view__200_ok_multiple_instances(
        self,
        api_client,
        mortgage_calculation_1,
        mortgage_calculation_2,
        mortgage_calculation_3,
    ):
        response = api_client.get(self.url)
        content = response.json()
        assert len(content) == 3
