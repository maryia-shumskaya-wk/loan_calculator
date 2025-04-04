<template>
  <v-app>
    <v-main>
      <Suspense>
        <LoanPaymentCalculator />
      </Suspense>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
  import LoanPaymentCalculator from './pages/LoanPaymentCalculator.vue';

</script>
