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

      socket.on('error', (error: Error) => {
        console.error(error)
      })

      socket.on('connect_error', (error: Error) => {
        console.error(error)
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
