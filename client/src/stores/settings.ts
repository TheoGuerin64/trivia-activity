import { defineStore } from 'pinia'

import { socket } from '@/socket'
import { ref, watch } from 'vue'

export enum Difficulty {
  RANDOM = 'random',
  EASY = 'easy',
  MEDIUM = 'medium',
  HARD = 'hard',
}

export const DifficultyNames = {
  [Difficulty.RANDOM]: 'Any Difficulty',
  [Difficulty.EASY]: 'Easy',
  [Difficulty.MEDIUM]: 'Medium',
  [Difficulty.HARD]: 'Hard',
}

export enum Category {
  RANDOM = '0',
  GENERAL_KNOWLEDGE = '9',
  ENTERTAINMENT_BOOKS = '10',
  ENTERTAINMENT_FILM = '11',
  ENTERTAINMENT_MUSIC = '12',
  ENTERTAINMENT_MUSICALS_THEATRES = '13',
  ENTERTAINMENT_TELEVISION = '14',
  ENTERTAINMENT_VIDEO_GAMES = '15',
  ENTERTAINMENT_BOARD_GAMES = '16',
  SCIENCE_NATURE = '17',
  SCIENCE_COMPUTERS = '18',
  SCIENCE_MATHEMATICS = '19',
  MYTHOLOGY = '20',
  SPORTS = '21',
  GEOGRAPHY = '22',
  HISTORY = '23',
  POLITICS = '24',
  ART = '25',
  CELEBRITIES = '26',
  ANIMALS = '27',
  VEHICLES = '28',
  ENTERTAINMENT_COMICS = '29',
  SCIENCE_GADGETS = '30',
  ENTERTAINMENT_JAPANESE_ANIME_MANGA = '31',
  ENTERTAINMENT_CARTOON_ANIMATIONS = '32',
}

export const CategoryNames = {
  [Category.RANDOM]: 'Any Category',
  [Category.GENERAL_KNOWLEDGE]: 'General Knowledge',
  [Category.ENTERTAINMENT_BOOKS]: 'Entertainment: Books',
  [Category.ENTERTAINMENT_FILM]: 'Entertainment: Film',
  [Category.ENTERTAINMENT_MUSIC]: 'Entertainment: Music',
  [Category.ENTERTAINMENT_MUSICALS_THEATRES]: 'Entertainment: Musicals & Theatres',
  [Category.ENTERTAINMENT_TELEVISION]: 'Entertainment: Television',
  [Category.ENTERTAINMENT_VIDEO_GAMES]: 'Entertainment: Video Games',
  [Category.ENTERTAINMENT_BOARD_GAMES]: 'Entertainment: Board Games',
  [Category.SCIENCE_NATURE]: 'Science & Nature',
  [Category.SCIENCE_COMPUTERS]: 'Science: Computers',
  [Category.SCIENCE_MATHEMATICS]: 'Science: Mathematics',
  [Category.MYTHOLOGY]: 'Mythology',
  [Category.SPORTS]: 'Sports',
  [Category.GEOGRAPHY]: 'Geography',
  [Category.HISTORY]: 'History',
  [Category.POLITICS]: 'Politics',
  [Category.ART]: 'Art',
  [Category.CELEBRITIES]: 'Celebrities',
  [Category.ANIMALS]: 'Animals',
  [Category.VEHICLES]: 'Vehicles',
  [Category.ENTERTAINMENT_COMICS]: 'Entertainment: Comics',
  [Category.SCIENCE_GADGETS]: 'Science: Gadgets',
  [Category.ENTERTAINMENT_JAPANESE_ANIME_MANGA]: 'Entertainment: Japanese Anime & Manga',
  [Category.ENTERTAINMENT_CARTOON_ANIMATIONS]: 'Entertainment: Cartoon & Animations',
}

interface SettingsData {
  round_count?: number
  difficulty?: string
  category?: number
}

export const useSettingsStore = defineStore('settings', () => {
  const roundCount = ref(10)
  const difficulty = ref(Difficulty.RANDOM)
  const category = ref(Category.RANDOM)

  function bindEvents() {
    socket.on('settings_update', (data: SettingsData) => {
      if (data.round_count !== undefined) {
        roundCount.value = data.round_count
      }
      if (data.difficulty !== undefined) {
        difficulty.value = data.difficulty as Difficulty
      }
      if (data.category !== undefined) {
        category.value = data.category.toString() as Category
      }
    })
  }

  watch(roundCount, (value: number) => {
    socket.emit('settings_update', { round_count: value })
  })

  watch(difficulty, (value: Difficulty) => {
    socket.emit('settings_update', { difficulty: value.valueOf() })
  })

  watch(category, (value: Category) => {
    socket.emit('settings_update', { category: parseInt(value.valueOf()) })
  })

  return { roundCount, difficulty, category, bindEvents }
})
