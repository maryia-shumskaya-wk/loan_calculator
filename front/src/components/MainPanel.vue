<template>
    <v-col
      cols="12"
      xs="12"
      md="8"
    >
        <v-card color="surface" class="rounded-xl card">
            <slot></slot>
        </v-card>
    </v-col>
</template>

<style scoped>
  .card {
    padding: 16px;
  }
</style>