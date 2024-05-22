import { defineStore } from 'pinia'
import { ref } from 'vue'

import { socket } from '@/socket'

interface QuestionData {
  question: string
  difficulty: string
  category: string
  answers: string[]
}

export const useGameStore = defineStore('game', () => {
  const started = ref<boolean>(false)
  const question = ref<QuestionData | null>(null)

  function bindEvents() {
    socket.on('start_game', () => {
      started.value = true
    })

    socket.on('question', (data: QuestionData) => {
      question.value = data
    })
  }

  function start_game() {
    socket.emit('start_game')
  }

  return { started, question, bindEvents, start_game }
})
