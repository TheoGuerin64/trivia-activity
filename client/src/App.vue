<script setup lang="ts">
import { onMounted } from 'vue'

import { authorize, sdk } from '@/sdk'
import { useConnectionStore } from './stores/connection'

import LoadingSpinner from '@/components/LoadingSpinner.vue'

const connectionStore = useConnectionStore()
connectionStore.bindEvents()

onMounted(async () => {
  await sdk.ready()
  const code = await authorize()
  connectionStore.connect(code)
})
</script>

<template>
  <router-view v-slot="{ Component }" v-if="connectionStore.connected">
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
  <LoadingSpinner v-else />
</template>
