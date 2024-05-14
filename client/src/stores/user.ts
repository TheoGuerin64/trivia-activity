import { defineStore } from 'pinia'

import { socket } from '@/socket'
import { ref } from 'vue'

interface UserData {
  is_leader?: boolean
}

export const useUserStore = defineStore('user', () => {
  const isLeader = ref(false)

  function bindEvents() {
    socket.on('user_data', (value: UserData) => {
      if (value.is_leader !== undefined) {
        isLeader.value = value.is_leader
      }
    })

    socket.on('error', (value) => {
      console.log(value)
    })
  }

  return { isLeader, bindEvents }
})
