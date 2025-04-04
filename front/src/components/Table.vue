<template>
    <v-data-table 
        :items="props.data"
        :headers="headers"
        items-per-page="-1"
    >
        <template #bottom></template>
    </v-data-table>
</template>

<script setup lang="ts" generic="T">

    type KeyToColumn = {
        [key: string]: string;
    }

    type Props = {
        data: T[];
        columns: KeyToColumn;
    }

    const props = defineProps<Props>();

    const headers = Object
        .entries(props.columns)
        .map(([key, value]) => ({
            title: value,
            value: key,
            sortable: true,
         }));
</script>