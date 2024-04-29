<script setup lang="ts">
import { RouterView } from 'vue-router'

import LoadingSpinner from './components/LoadingSpinner.vue'
</script>

<template>
  <router-view v-slot="{ Component }">
    <template v-if="Component">
      <KeepAlive>
        <suspense timeout="0">
          <component :is="Component" />
          <template #fallback>
            <LoadingSpinner />
          </template>
        </suspense>
      </KeepAlive>
    </template>
  </router-view>
</template>
