<script setup lang="ts">
import {
  Category,
  CategoryNames,
  Difficulty,
  DifficultyNames,
  useSettingsStore,
} from '@/stores/settings'
import { useUserStore } from '@/stores/user'

const settingsStore = useSettingsStore()
const userStore = useUserStore()

function submit() {}
</script>

<template>
  <main>
    <h1>Lobby</h1>
    <form @submit.prevent="submit">
      <label>
        Rounds:
        <input
          type="number"
          v-model="settingsStore.roundCount"
          min="1"
          max="10"
          @keydown.prevent
          :disabled="!userStore.isLeader"
        />
      </label>

      <label>
        Difficulty:
        <select v-model="settingsStore.difficulty" :disabled="!userStore.isLeader">
          <option v-for="(value, key) in Difficulty" :key="key" :value="value">
            {{ DifficultyNames[value] }}
          </option>
        </select>
      </label>

      <label>
        Category:
        <select v-model="settingsStore.category" :disabled="!userStore.isLeader">
          <option v-for="(value, key) in Category" :key="key" :value="value">
            {{ CategoryNames[value] }}
          </option>
        </select>
      </label>

      <button type="submit" v-if="userStore.isLeader">Start Game</button>
    </form>
  </main>
</template>
