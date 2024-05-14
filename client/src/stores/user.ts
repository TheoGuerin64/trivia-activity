import { defineStore } from 'pinia'

import { socket } from '@/socket'
import { computed, ref } from 'vue'

interface UserData {
  is_leader?: boolean
}

export const useUserStore = defineStore('user', () => {
  const isLeader = ref<boolean | null>(null)

  function bindEvents() {
    socket.on('user_data', (value: UserData) => {
      if (value.is_leader !== undefined) {
        isLeader.value = value.is_leader
      }
    })
  }

  const isReady = computed(() => {
    return isLeader.value !== null
  })

  return { isLeader, isReady, bindEvents }
})
