import { defineStore } from 'pinia'

import { sdk } from '@/sdk'
import { socket } from '@/socket'

export const useConnectionStore = defineStore('connection', {
  state: () => ({
    connected: false,
  }),

  actions: {
    bindEvents() {
      socket.on('connect', () => {
        this.connected = true
      })

      socket.on('disconnect', () => {
        this.connected = false
      })
    },

    connect(code: string) {
      socket.auth = { code: code, channel_id: sdk.channelId }
      socket.connect()
    },

    disconnect() {
      socket.disconnect()
    },
  },
})
