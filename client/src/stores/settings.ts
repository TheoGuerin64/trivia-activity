import { defineStore } from 'pinia'

import { socket } from '@/socket'
import { reactive, ref, watch } from 'vue'

export enum Difficulty {
  RANDOM = 'random',
  EASY = 'easy',
  MEDIUM = 'medium',
  HARD = 'hard',
}

interface Settings {
  round_count: number
  difficulty: string
  category: number
}

export const useSettingsStore = defineStore('settings', () => {
  const categories = ref<Map<number, string> | null>(null)
  const settings = reactive<Settings>({
    round_count: 10,
    difficulty: Difficulty.RANDOM,
    category: 0,
  })

  function bindEvents() {
    socket.on('settings_update', (data: Settings) => {
      settings.round_count = data.round_count
      settings.difficulty = data.difficulty
      settings.category = data.category
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

  watch(settings, (value: Settings) => {
    socket.emit('settings_update', value)
  })

  return { settings, bindEvents, fetchCategories, categories }
})
