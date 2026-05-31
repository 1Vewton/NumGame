<!--
BotGame.vue - Bot Game Mode Component

This component implements the Bot (PVE) game mode. It wraps the shared
GameScreen template component and will contain Bot-specific game logic,
WebSocket handling, and API calls in the future. Currently, only the
UI shell is set up with no internal logic implemented.

The Bot game mode matches the player against an AI-controlled opponent.
Game data flows from this component into GameScreen via props, and
user operations from GameScreen bubble back up via the @operate event.

@module BotGame
-->
<template>
  <!--
    Render the shared GameScreen template component.
    Props (enemyScore, playerScore, actionPoints) provide display data.
    The @operate event is emitted when the user clicks an operation button.
  -->
  <GameScreen
    :enemyScore="enemyScore"
    :playerScore="playerScore"
    :actionPoints="actionPoints"
    @operate="handleOperation"
  />
</template>

<script>
/**
 * BotGame Component - Bot game mode (PVE)
 *
 * This component serves as the parent/controller for Bot game mode.
 * It wraps the GameScreen template and currently holds placeholder
 * state and method stubs. Game logic (WebSocket connections, API
 * calls, turn management, win/loss detection) will be implemented
 * here in future iterations.
 *
 * The component manages:
 * - enemyScore: The Bot's current score
 * - playerScore: The player's current score
 * - actionPoints: The player's available action points
 *
 * @module BotGame
 */
import GameScreen from './GameScreen.vue';

export default {
  // Component name used for debugging and Vue devtools
  name: 'BotGame',

  /**
   * Child components registered in this component
   *
   * @property {Component} GameScreen - The shared game screen template component
   */
  components: {
    GameScreen
  },

  /**
   * Component data properties
   *
   * @property {number} enemyScore - The Bot's current score
   * @property {number} playerScore - The player's current score
   * @property {number} actionPoints - The player's available action points
   */
  data() {
    return {
      enemyScore: 0,
      playerScore: 0,
      actionPoints: 10
    };
  },

  /**
   * Component lifecycle hook
   *
   * Logs when the BotGame component is mounted and the game is ready.
   * Future implementations will initiate WebSocket connections here.
   */
  mounted() {
    console.log('BotGame component mounted');
  },

  /**
   * Component methods
   */
  methods: {
    /**
     * handleOperation - Handles game operation events from GameScreen
     *
     * This is a placeholder method for processing the five game operations
     * in Bot game mode. It will be implemented with actual game logic,
     * WebSocket messaging, and API calls in future iterations.
     *
     * @method handleOperation
     * @param {string} operation - The operation identifier
     *   ('produce', 'destruct', 'enhanceProductivity', 'enhanceDestructivity',
     *    'enhanceActionPoints')
     */
    handleOperation(operation) {
      console.log('BotGame operation triggered:', operation);
    }
  }
}
</script>

<style scoped src="../assets/styles/game-screen.css"></style>
