<template>
    <div class="label text-h5">{{ title }}</div>

    <v-text-field
      v-model="value"
      :placeholder="placeholder"
      class="rounded-xl"
      density="compact"
    ></v-text-field>
</template>

<script setup lang="ts" generic="T">
    import { ref, watch } from 'vue';

    type Props = {
        title: string;
        placeholder: string;
        value: string;
        fieldName: T;
        required?: boolean;
    };

    type Emits = {
        (e: 'changeValue', fieldName: T, value: string): void
    }

    const props = withDefaults(defineProps<Props>(), {
        required: true,
    });

    const emit = defineEmits<Emits>();

    const value = ref(props.value);

    watch(value, (newValue) => {
        emit("changeValue", props.fieldName, newValue);
    });

</script>

<style scoped lang="scss">
    .label {
        color: rgb(var(--v-theme-primary));
        font-weight: 500;
    }
</style>