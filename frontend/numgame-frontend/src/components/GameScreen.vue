<!--
GameScreen.vue - Generic Game Screen Template Component

This component serves as a pure presentational UI shell for multiple game modes
(Bot, Player vs Player, etc.). It has NO internal game logic or state management.
All data is passed via props, and all user interactions are emitted as events.

This design ensures reusability: each game mode (Bot/PvP/etc.) can use this
template and implement their own independent game logic, WebSocket handling,
and API calls without being coupled to this component.

@module GameScreen
-->
<template>
  <!-- Main game screen container -->
  <div class="game-screen">

    <!-- Game rules icon button (top-left corner) -->
    <div class="rules-icon-container">
      <button class="rules-icon-button" @click="showGameRules = true" title="Game Rules">
        <i class="fas fa-circle-info fa-2x"></i>
      </button>
    </div>

    <!-- Game rules modal overlay (reusable component) -->
    <GameRulesModal
      :visible="showGameRules"
      @close="showGameRules = false"
    />

    <!-- Game icon -->
    <div class="game-icon-container">
      <i class="fas fa-gamepad fa-5x"></i>
    </div>

    <!-- Welcome text -->
    <div class="welcome-container">
      <h1 class="welcome-title">NumGame Battle</h1>
      <p class="welcome-subtitle">Use your AP wisely to outscore the enemy</p>
    </div>

    <!-- ============================================ -->
    <!-- Score Section                                 -->
    <!-- ============================================ -->
    <div class="game-score-section">

      <!-- Enemy score -->
      <div class="score-item score-item--enemy">
        <span class="score-label">Enemy</span>
        <span class="score-value">{{ enemyScore }}</span>
      </div>

      <!-- VS divider -->
      <div class="vs-divider">
        <i class="fas fa-bolt"></i>
      </div>

      <!-- Player score -->
      <div class="score-item score-item--player">
        <span class="score-label">My Score</span>
        <span class="score-value">{{ playerScore }}</span>
      </div>

    </div>

    <!-- Stats row: Turn, Productivity, Destructivity, Action Points, Countdown -->
    <div class="stats-row">

      <!-- Turn display -->
      <div class="stat-display stat-display--turn">
        <i class="fas fa-flag"></i>
        <span>Turn: <span class="stat-value">{{ turn }}</span></span>
      </div>

      <!-- Productivity display -->
      <div class="stat-display stat-display--productivity">
        <i class="fas fa-arrow-up"></i>
        <span>Productivity: <span class="stat-value">{{ productivity }}</span></span>
      </div>

      <!-- Destructivity display -->
      <div class="stat-display stat-display--destructivity">
        <i class="fas fa-arrow-down"></i>
        <span>Destructivity: <span class="stat-value">{{ destructivity }}</span></span>
      </div>

      <!-- Action Points display -->
      <div class="stat-display stat-display--ap">
        <i class="fas fa-bolt"></i>
        <span>AP: <span class="stat-value">{{ actionPoints }}</span></span>
      </div>

      <!-- Countdown timer display (shown only when countdown is active) -->
      <div class="stat-display stat-display--countdown" v-if="countdown > 0">
        <i class="fas fa-hourglass-half"></i>
        <span>Time: <span class="stat-value stat-value--countdown">{{ countdown }}</span>s</span>
      </div>
    </div>

    <!-- ============================================ -->
    <!-- Operation Buttons Grid                        -->
    <!-- ============================================ -->
    <div class="game-operations">

      <!-- Enhance Productivity (disabled when AP is below 10) -->
      <div class="operation-item">
        <button
          class="operation-button"
          :disabled="!isPlayerTurn || isLowAp"
          @click="$emit('operate', 'enhanceProductivity')"
        >
          <i class="fas fa-arrow-up"></i>
        </button>
        <span class="operation-label">Enhance<br/>Productivity</span>
      </div>

      <!-- Produce (disabled when AP is below 10) -->
      <div class="operation-item">
        <button
          class="operation-button"
          :disabled="!isPlayerTurn || isLowAp"
          @click="$emit('operate', 'produce')"
        >
          <i class="fas fa-plus-circle"></i>
        </button>
        <span class="operation-label">Produce</span>
      </div>

      <!-- Enhance Action Points (disabled when AP is below 10) -->
      <div class="operation-item">
        <button
          class="operation-button"
          :disabled="!isPlayerTurn || isLowAp"
          @click="$emit('operate', 'enhanceActionPoints')"
        >
          <i class="fas fa-bolt"></i>
        </button>
        <span class="operation-label">Enhance<br/>AP</span>
      </div>

      <!-- Destruct (disabled when AP is below 10) -->
      <div class="operation-item">
        <button
          class="operation-button"
          :disabled="!isPlayerTurn || isLowAp"
          @click="$emit('operate', 'destruct')"
        >
          <i class="fas fa-minus-circle"></i>
        </button>
        <span class="operation-label">Destruct</span>
      </div>

      <!-- Enhance Destructivity (disabled when AP is below 10) -->
      <div class="operation-item">
        <button
          class="operation-button"
          :disabled="!isPlayerTurn || isLowAp"
          @click="$emit('operate', 'enhanceDestructivity')"
        >
          <i class="fas fa-arrow-down"></i>
        </button>
        <span class="operation-label">Enhance<br/>Destructivity</span>
      </div>

      <!-- Skip (always enabled during player's turn, even when AP is low) -->
      <div class="operation-item">
        <button
          class="operation-button"
          :disabled="!isPlayerTurn"
          @click="$emit('operate', 'skip')"
        >
          <i class="fas fa-forward-step"></i>
        </button>
        <span class="operation-label">Skip</span>
      </div>

    </div>

  </div>
</template>

<script>
/**
 * GameScreen Component - Pure presentational UI shell for game modes
 *
 * This component is a stateless template with NO internal game logic.
 * It displays the game UI layout and delegates all behavior to the
 * parent component via props and events.
 *
 * Usage by game mode components (e.g., BotGame, PvPGame):
 * <GameScreen
 *   :enemyScore="myEnemyScore"
 *   :playerScore="myPlayerScore"
 *   :actionPoints="myActionPoints"
 *   @operate="handleOperation"
 * />
 *
 * @module GameScreen
 */
import GameRulesModal from './GameRulesModal.vue';

export default {
  // Component name used for debugging and Vue devtools
  name: 'GameScreen',

  /**
   * Child components registered in this component
   *
   * @property {Component} GameRulesModal - Reusable game rules modal component
   */
  components: {
    GameRulesModal
  },

  /**
   * Component props - External data passed to the component
   *
   * @property {number} enemyScore - The current score of the enemy/opponent
   * @property {number} playerScore - The current score of the player
   * @property {number} productivity - The player's current productivity value
   * @property {number} destructivity - The player's current destructivity value
   * @property {number} actionPoints - The current action points available
   * @property {number} countdown - The countdown timer value for the current turn,
   *   in seconds (0 = no active timer). When greater than 0, a countdown display
   *   is shown in the stats row.
   */
  props: {
    enemyScore: {
      type: Number,
      default: 0
    },
    playerScore: {
      type: Number,
      default: 0
    },
    productivity: {
      type: Number,
      default: 1
    },
    destructivity: {
      type: Number,
      default: 1
    },
    turn: {
      type: Number,
      default: 1
    },
    actionPoints: {
      type: Number,
      default: 10
    },
    countdown: {
      type: Number,
      default: 0
    },
    /**
     * Controls whether the operation buttons are enabled (clickable).
     * When true (player's turn), buttons are enabled.
     * When false (bot's turn or between turns), buttons are disabled.
     *
     * @property {Boolean} isPlayerTurn
     */
    isPlayerTurn: {
      type: Boolean,
      default: false
    }
  },

  /**
   * Component emits - Events emitted to the parent
   *
   * @event operate - Emitted when a game operation button is clicked
   *   @param {string} operation - The operation identifier
   *     ('produce', 'destruct', 'enhanceProductivity', 'enhanceDestructivity',
   *      'enhanceActionPoints', 'skip')
   */
  emits: ['operate'],

  /**
   * Component computed properties
   *
   * @property {boolean} isLowAp - Whether the player's AP is below 10.
   *   When true, all operation buttons except "Skip" are disabled,
   *   forcing the player to skip their turn.
   */
  computed: {
    isLowAp() {
      return this.actionPoints < 10;
    }
  },

  /**
   * Component data properties
   *
   * @property {boolean} showGameRules - Flag controlling the game rules modal visibility
   */
  data() {
    return {
      showGameRules: false
    };
  }
}
</script>

<style scoped src="../assets/styles/game-screen.css"></style>
