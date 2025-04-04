<template>
    <v-btn 
      variant="tonal"
      class="button" 
      @click="buttonClick"
      block>
        {{ text }}
    </v-btn>
</template>

<script setup lang="ts">
    type Props = {
        text: string;
    }

    type Emits = {
      (e: 'click'): void
    };

    const { text } = defineProps<Props>();
    const emit = defineEmits<Emits>();

    const buttonClick = () => {
      emit('click');
    }
</script>

<style>
  .button {
    background-color: rgb(var(--v-theme-button-primary));
    color: rgb(var(--v-theme-button-secondary));
  }
</style>