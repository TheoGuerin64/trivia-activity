import { io } from 'socket.io-client'
import { reactive } from 'vue'

export const state = reactive({
  connected: false,
})

const URL = import.meta.env.DEV
  ? 'http://localhost:3000'
  : 'https://trivia-activity-server.theo-guerin.dev'

export const socket = io(URL, {
  autoConnect: false,
  transports: ['websocket'],
})

socket.on('connect', () => {
  state.connected = true
})

socket.on('disconnect', () => {
  state.connected = false
})
