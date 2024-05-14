import { defineStore } from 'pinia'

import { socket } from '@/socket'
import { ref, watch } from 'vue'

export enum Difficulty {
  RANDOM = 0,
  EASY = 1,
  MEDIUM = 2,
  HARD = 3,
}

interface SettingsData {
  round_count?: number
  difficulty?: Difficulty
}

export const useSettingsStore = defineStore('settings', () => {
  const roundCount = ref(10)
  const difficulty = ref(Difficulty.RANDOM)

  function bindEvents() {
    socket.on('setting_update', (data: SettingsData) => {
      if (data.round_count !== undefined) {
        roundCount.value = data.round_count
      }
      if (data.difficulty !== undefined) {
        difficulty.value = data.difficulty
      }
    })
  }

  watch(roundCount, (value: number) => {
    socket.emit('setting_update', { round_count: value })
  })

  watch(difficulty, (value: Difficulty) => {
    socket.emit('setting_update', { difficulty: value.valueOf() })
  })

  return { roundCount, difficulty, bindEvents }
})
