import { io } from 'socket.io-client'

export const socket = io({
  autoConnect: false,
  transports: ['websocket'],
  path: '/server/socket.io',
})

socket.on('error', (value) => {
  console.error(value)
})
