<template>
    <v-container>

        <Title>Loan Payment Calculator</Title>
        <Layout>
            <SidePanel>
                <template v-for="item in fields">
                    <CustomInput
                        :fieldName="item.fieldName"
                        :title="item.title"
                        :placeholder="item.placeholder"
                        :value="inputData[item.fieldName]"
                        @changeValue="valueChanged"
                    />
                </template>
                <Button 
                    text="Generate Rates"
                    @click="submit"
                />
            </SidePanel>
            <MainPanel>
                <Table 
                    :data="tableData"
                    :columns="columnMapping"
                > </Table>
            </MainPanel>
        </Layout>

    </v-container>
</template>

<script setup lang="ts">
    import Layout from '@/components/Layout.vue';
    import MainPanel from '@/components/MainPanel.vue';
    import SidePanel from '@/components/SidePanel.vue';
    import Title from '@/components/Title.vue';
    import CustomInput from '@/components/CustomInput.vue';
    import Table from '@/components/Table.vue';
    import Button from '@/components/Button.vue';
    import { ref } from 'vue';
    
    import mortgageApiService from '@/services/mortgageApiService';

    const inputData = ref({
        purchasePrice: '',
        interestRate: '',
        downPaymentInDollars: '',
        downPaymentInPercents: '',
        mortgageTerm: '',
        
    });

    type FieldName = keyof typeof inputData.value;
    type FieldType = {
        fieldName: FieldName;
        title: string;
        placeholder: string;
        required: boolean;
    }

    const fields = ref<FieldType[]>([
        {
            fieldName: "purchasePrice",
            title: "Purchase Price *",
            placeholder: "E.g. $ 100 000 000",
            required: true,
        }, 
        {
            fieldName: "interestRate",
            title: "Interest Rate *",
            placeholder: "E.g. 20 %",
            required: true,
        },
        {
            fieldName: "downPaymentInDollars",
            title: "Down Payment in $",
            placeholder: "E.g. $ 15 000 000" ,
            required: false,
        },
        {
            fieldName: "downPaymentInPercents",
            title: "Down Payment in %",
            placeholder: "E.g. 20 %",
            required: false,
        },
        {
            fieldName: "mortgageTerm",
            title: "Mortgage Term *",
            placeholder: "E.g. 90 months",
            required: true,
        },
    ])

    const fetchTableData = async () => {
        try {
            return await mortgageApiService.getMortgages();
        } catch (err) {
            console.log(err);
            return []
        }
    }

    const tableData = ref(await fetchTableData());
    const columnMapping = {
        "mortgageTerm": "Mortgage Term",
        "interestRate": "Interest Rate",
        "monthlyPayment": "Monthly Payment",
        "totalAmount": "Total Amount",
        "totalOverLoanTerm": "Total Over Loan Term"

    };
    
    const valueChanged = (fieldName: Extract<FieldName, string>, value: string) => {
        inputData.value[fieldName] = value;
    }

    const submit = async () => {
        try {
            const data = await mortgageApiService.calculateMortgages({
                ...inputData.value
            });
            tableData.value.unshift(data);
        } catch (error) {
            // TODO: error handling
            console.log(error);
        }
    };

</script>