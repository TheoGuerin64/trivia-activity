import { defineStore } from 'pinia'

import { sdk } from '@/sdk'
import { socket } from '@/socket'
import { ref } from 'vue'

export const useConnectionStore = defineStore('connection', () => {
  const connected = ref<boolean>(false)

  function bindEvents() {
    socket.on('connect', () => {
      connected.value = true
    })

    socket.on('disconnect', () => {
      connected.value = false
    })
  }

  function connect(code: string) {
    socket.auth = { code: code, channel_id: sdk.channelId }
    socket.connect()
  }

  function disconnect() {
    socket.disconnect()
  }

  return { connected, bindEvents, connect, disconnect }
})
