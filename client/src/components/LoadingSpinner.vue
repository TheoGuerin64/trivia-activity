<script setup lang="ts">
const props = defineProps<{
  text?: string
}>()
</script>

<template>
  <div class="loading-spinner">
    <span class="loading-spinner__text">{{ props.text }}</span>
    <span class="loading-spinner__spinner" aria-busy="true" />
  </div>
</template>

<style lang="scss">
.loading-spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
}

.loading-spinner__text {
  font-size: 2rem;
}

.loading-spinner__spinner {
  font-size: 5rem;
}
</style>
