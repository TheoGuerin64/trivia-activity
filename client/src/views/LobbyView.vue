<script setup lang="ts">
import { useGameStore } from '@/stores/game'
import { Difficulty, useSettingsStore } from '@/stores/settings'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const router = useRouter()

const settingsStore = useSettingsStore()
const userStore = useUserStore()
const gameStore = useGameStore()

gameStore.$subscribe((_mutation, state) => {
  if (state.started) {
    router.push({ name: 'game' })
  }
})
</script>

<template>
  <main>
    <h1>Lobby</h1>
    <form @submit.prevent="gameStore.start_game">
      <label>
        Rounds:
        <input
          type="number"
          v-model="settingsStore.settings.round_count"
          min="1"
          max="10"
          @keydown.prevent
          :disabled="!userStore.isLeader"
        />
      </label>

      <label>
        Difficulty:
        <select v-model="settingsStore.settings.difficulty" :disabled="!userStore.isLeader">
          <option :value="Difficulty.RANDOM">Any Difficulty</option>
          <option :value="Difficulty.EASY">Easy</option>
          <option :value="Difficulty.MEDIUM">Medium</option>
          <option :value="Difficulty.HARD">Hard</option>
        </select>
      </label>

      <label>
        Category:
        <select v-model="settingsStore.settings.category" :disabled="!userStore.isLeader">
          <option v-for="(value, key) in settingsStore.categories" :key="key" :value="value[0]">
            {{ value[1] }}
          </option>
        </select>
      </label>

      <button type="submit" v-if="userStore.isLeader">Start Game</button>
    </form>
  </main>
</template>
