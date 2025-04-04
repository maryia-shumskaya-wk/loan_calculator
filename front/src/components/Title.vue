<template>
    <p class="text-h2 title">
        <slot></slot>
    </p>
</template>

<style scoped lang="scss">
    .title {
        color: rgb(var(--v-theme-primary));
        padding: 32px;
        font-weight: 600;
    }

</style>