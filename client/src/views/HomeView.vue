<script setup lang="ts">
import { socket, state } from '@/socket'
</script>

<template>
  <main class="container">
    <button @click="socket.disconnect" v-if="state.connected">Disconnect</button>
    <button @click="socket.connect" v-else>Connect</button>
  </main>
</template>
