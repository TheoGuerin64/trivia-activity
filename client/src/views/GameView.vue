<script setup lang="ts">
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { useGameStore } from '@/stores/game'

const gameStore = useGameStore()
</script>

<template>
  <main>
    <div class="game-view__content" v-if="gameStore.question">
      <h3>{{ gameStore.question.question }}</h3>
      <div class="game-view__meta">
        <h5>{{ gameStore.question.category }}</h5>
        <h5>{{ gameStore.question.difficulty }}</h5>
      </div>
      <div class="grid">
        <button v-for="(answer, index) in gameStore.question.answers" :key="index">
          {{ answer }}
        </button>
      </div>
    </div>
    <LoadingSpinner text="Loading" v-else />
  </main>
</template>

<style lang="scss">
@media (min-width: 768px) {
  .game-view__content {
    margin-top: 18vh;
  }
}

.game-view__meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
}
</style>
