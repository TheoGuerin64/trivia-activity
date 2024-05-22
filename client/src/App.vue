<script setup lang="ts">
import { onMounted } from 'vue'

import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { authorize, sdk } from '@/sdk'
import { useConnectionStore } from '@/stores/connection'
import { useGameStore } from '@/stores/game'
import { useSettingsStore } from '@/stores/settings'
import { useUserStore } from '@/stores/user'

const connectionStore = useConnectionStore()
const userStore = useUserStore()
const settingsStore = useSettingsStore()
const gameStore = useGameStore()

connectionStore.bindEvents()
userStore.bindEvents()
settingsStore.bindEvents()
gameStore.bindEvents()

async function connect() {
  await sdk.ready()
  const code = await authorize()
  connectionStore.connect(code)
}

onMounted(() => {
  connect()
  settingsStore.fetchCategories()
})
</script>

<template>
  <router-view v-slot="{ Component }" v-if="connectionStore.connected && settingsStore.categories">
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
