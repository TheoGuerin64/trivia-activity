<script setup lang="ts">
import { onMounted } from 'vue'

import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { authorize, sdk } from '@/sdk'
import { useConnectionStore } from '@/stores/connection'
import { useUserStore } from '@/stores/user'

const connectionStore = useConnectionStore()
const userStore = useUserStore()

connectionStore.bindEvents()
userStore.bindEvents()

onMounted(async () => {
  await sdk.ready()
  const code = await authorize()
  connectionStore.connect(code)
})
</script>

<template>
  <router-view v-slot="{ Component }" v-if="connectionStore.connected && userStore.isReady">
    <template v-if="Component">
      <keep-alive>
        <suspense timeout="0">
          <component :is="Component" />
          <template #fallback>
            <LoadingSpinner text="Loading" />
          </template>
        </suspense>
      </keep-alive>
    </template>
  </router-view>
  <LoadingSpinner text="Connecting" v-else />
</template>
