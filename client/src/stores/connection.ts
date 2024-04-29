import { socket } from '@/socket'
import { defineStore } from 'pinia'

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

    connect() {
      socket.connect()
    },
    disconnect() {
      socket.disconnect()
    },
  },
})
