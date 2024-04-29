import { io } from 'socket.io-client'

const URL = import.meta.env.DEV
  ? 'http://localhost:3000'
  : 'https://trivia-activity-server.theo-guerin.dev'

export const socket = io(URL, {
  autoConnect: false,
  transports: ['websocket'],
})
