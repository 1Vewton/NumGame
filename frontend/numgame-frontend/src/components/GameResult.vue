<!--
GameResult.vue - Game Result Modal Component

This component displays the game result (victory or defeat) overlay
after a game finishes. It shows an icon, title, final scores comparison,
and action buttons (Play Again / Back to Setup).

The overlay uses a dark backdrop with centered modal container.
Victory shows green accents, defeat shows red accents.

@module GameResult
-->
<template>
  <div v-if="visible" class="game-result-overlay">
    <div
      class="game-result-container"
      :class="isVictory ? 'game-result-container--victory' : 'game-result-container--defeat'"
    >

      <!-- Result icon -->
      <div
        class="game-result-icon"
        :class="isVictory ? 'game-result-icon--victory' : 'game-result-icon--defeat'"
      >
        <i :class="isVictory ? 'fas fa-trophy' : 'fas fa-skull'"></i>
      </div>

      <!-- Result title -->
      <h2
        class="game-result-title"
        :class="isVictory ? 'game-result-title--victory' : 'game-result-title--defeat'"
      >
        {{ isVictory ? 'Victory' : 'Defeat' }}
      </h2>

      <!-- Final scores comparison -->
      <div class="game-result-scores">
        <div class="game-result-score-item">
          <span class="game-result-score-label">Enemy</span>
          <span
            class="game-result-score-value"
            :class="isVictory ? 'game-result-score-value--enemy' : 'game-result-score-value--winner'"
          >
            {{ enemyScore }}
          </span>
        </div>

        <div class="game-result-vs">VS</div>

        <div class="game-result-score-item">
          <span class="game-result-score-label">My Score</span>
          <span
            class="game-result-score-value"
            :class="isVictory ? 'game-result-score-value--winner' : 'game-result-score-value--player'"
          >
            {{ playerScore }}
          </span>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="game-result-buttons">
        <AppButton
          label="Play Again"
          variant="primary"
          size="medium"
          width="100%"
          @click="$emit('playAgain')"
        />
        <AppButton
          label="Back to Title"
          variant="secondary"
          size="medium"
          width="100%"
          @click="$emit('backToTitle')"
        />
      </div>

    </div>
  </div>
</template>

<script>
/**
 * GameResult Component - Game result overlay modal
 *
 * This component displays the final game outcome (victory or defeat)
 * with an icon, title, score comparison, and action buttons.
 * It is used by parent game components (e.g., BotGame) after receiving
 * a win/loss signal from the backend.
 *
 * @module GameResult
 */
import AppButton from './AppButton.vue';

export default {
  // Component name used for debugging and Vue devtools
  name: 'GameResult',

  /**
   * Child components registered in this component
   *
   * @property {Component} AppButton - Reusable styled button component
   */
  components: {
    AppButton
  },

  /**
   * Component props - External data passed to the component
   *
   * @property {boolean} visible - Controls whether the result overlay is shown
   * @property {boolean} isVictory - True if the player won, false if defeated
   * @property {number} playerScore - The player's final score
   * @property {number} enemyScore - The enemy's final score
   */
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    isVictory: {
      type: Boolean,
      default: false
    },
    playerScore: {
      type: Number,
      default: 0
    },
    enemyScore: {
      type: Number,
      default: 0
    }
  },

  /**
   * Component emits - Events emitted to the parent
   *
   * @event playAgain - Emitted when the user clicks "Play Again"
   *   Parent should navigate to StartBotGame to setup a new game
   * @event backToTitle - Emitted when the user clicks "Back to Title"
   *   Parent should navigate to the welcome screen (StartScreen)
   */
  emits: ['playAgain', 'backToTitle']

}
</script>

<style scoped src="../assets/styles/game-result.css"></style>
