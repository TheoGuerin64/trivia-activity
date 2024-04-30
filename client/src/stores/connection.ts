import { defineStore } from 'pinia'

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
      socket.auth = { code }
      socket.connect()
    },

    disconnect() {
      socket.disconnect()
    },
  },
})
