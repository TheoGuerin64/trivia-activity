<script setup lang="ts">
import { useConnectionStore } from '@/stores/connection'

const connectionStore = useConnectionStore()
connectionStore.bindEvents()
</script>

<template>
  <main class="container">
    <button @click="connectionStore.disconnect" v-if="connectionStore.connected">Disconnect</button>
    <button @click="connectionStore.connect" v-else>Connect</button>
  </main>
</template>
