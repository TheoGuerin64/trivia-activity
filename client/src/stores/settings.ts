import { defineStore } from 'pinia'

import { socket } from '@/socket'
import { ref, watch } from 'vue'

export enum Difficulty {
  RANDOM = 'random',
  EASY = 'easy',
  MEDIUM = 'medium',
  HARD = 'hard',
}

interface SettingsData {
  round_count?: number
  difficulty?: string
  category?: number
}

export const useSettingsStore = defineStore('settings', () => {
  const categories = ref<Map<number, string> | null>(null)

  const roundCount = ref(10)
  const category = ref(0)
  const difficulty = ref(Difficulty.RANDOM)

  function bindEvents() {
    socket.on('settings_update', (data: SettingsData) => {
      if (data.round_count !== undefined) {
        roundCount.value = data.round_count
      }
      if (data.difficulty !== undefined) {
        difficulty.value = data.difficulty as Difficulty
      }
      if (data.category !== undefined) {
        category.value = data.category
      }
    })
  }

  async function fetchCategories() {
    const response = await fetch('/opentdb/api_category.php')
    const data = await response.json()
    categories.value = new Map([[0, 'Any Category']])
    for (const category of data.trivia_categories) {
      categories.value.set(category.id, category.name)
    }
  }

  watch(roundCount, (value: number) => {
    socket.emit('settings_update', { round_count: value })
  })

  watch(difficulty, (value: Difficulty) => {
    socket.emit('settings_update', { difficulty: value.valueOf() })
  })

  watch(category, (value: number) => {
    socket.emit('settings_update', { category: value })
  })

  return { roundCount, difficulty, category, bindEvents, fetchCategories, categories }
})
