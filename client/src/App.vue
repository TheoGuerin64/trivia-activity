<script setup lang="ts">
import LoadingSpinner from './components/LoadingSpinner.vue'
</script>

<template>
  <router-view v-slot="{ Component }">
    <template v-if="Component">
      <keep-alive>
        <suspense timeout="0">
          <component :is="Component" />
          <template #fallback>
            <LoadingSpinner />
          </template>
        </suspense>
      </keep-alive>
    </template>
  </router-view>
</template>
