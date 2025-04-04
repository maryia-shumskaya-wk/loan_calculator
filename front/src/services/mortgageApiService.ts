import apiClient from "./apiClient"

type MortgageCalculationDTO = {
    mortgageTerm: string;
    monthlyPayment: string;
    interestRate: string;
    totalAmount: string;
    totalOverLoanTerm: string;
};

type CreateMortgageCalculationDTO = {
    purchasePrice: string;
    interestRate: string;
    downPaymentInPercents?: string;
    downPaymentInDollars?: string;
    mortgageTerm: string;
}

class MortgageApiService {
    private readonly path = '/v1/mortgage/'

    getMortgages = async (): Promise<MortgageCalculationDTO[]> => {
        const response = await apiClient.get({
            additionalPath: this.path,
        });

        return response.data;
    };

    calculateMortgages = async (data: CreateMortgageCalculationDTO): Promise<MortgageCalculationDTO> => {
        const response = await apiClient.post({
            additionalPath: this.path,
            data,
        });

        return response.data;
    };

}

export default new MortgageApiService();