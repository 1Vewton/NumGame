<!--
GameInfo.vue - Game Information Page Component

This component displays a list of all games the player has participated in.
It fetches game history from the backend GamesInfoEndpoint and renders each
game as a card showing the matchup, scores, win/loss status, and metadata.
The card border color indicates win (green) or loss (red), and the player's
side is highlighted in green while the opponent's side is in red.

@module GameInfo
-->
<template>
  <div class="game-info-page">
    <!-- Page header -->
    <div class="game-info-header">
      <h1 class="game-info-title">Game History</h1>
      <button class="back-btn" @click="$router.push({ name: 'StartScreen' })" title="Back to Home">
        <i class="fas fa-house"></i>
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="game-info-loading">
      <i class="fas fa-spinner fa-spin"></i>
      <span>Loading game history...</span>
    </div>

    <!-- Error state -->
    <div v-else-if="errorMessage" class="game-info-error">
      <i class="fas fa-exclamation-triangle"></i>
      <span>{{ errorMessage }}</span>
    </div>

    <!-- Empty state -->
    <div v-else-if="games.length === 0" class="game-info-empty">
      <i class="fas fa-gamepad"></i>
      <span>No games played yet. Start a game to see your history!</span>
    </div>

    <!-- Games list -->
    <div v-else class="game-list">
      <div
        v-for="game in games"
        :key="game.id"
        class="game-card"
        :class="getCardClass(game)"
      >
        <!-- Win/Loss icon row -->
        <div
          class="game-card-result"
          :class="getResultClass(game)"
        >
          <i v-if="isWin(game)" class="fas fa-trophy"></i>
          <i v-else-if="isLose(game)" class="fas fa-skull"></i>
        </div>

        <!-- Players and scores row -->
        <div class="game-card-players">
          <!-- Left player (first_move) -->
          <div
            class="player-side player-side--left"
            :class="getPlayerSideClass(game.firstMove)"
          >
            <span class="player-name">{{ getPlayerName(game.firstMove) }}</span>
            <span class="player-score">{{ formatScore(game.firstMoveScore) }}</span>
          </div>

          <!-- Crossed swords VS icon -->
          <div class="game-card-vs">
            <i class="fas fa-crossed-swords"></i>
          </div>

          <!-- Right player (second_move) -->
          <div
            class="player-side player-side--right"
            :class="getPlayerSideClass(game.secondMove)"
          >
            <span class="player-name">{{ getPlayerName(game.secondMove) }}</span>
            <span class="player-score">{{ formatScore(game.secondMoveScore) }}</span>
          </div>
        </div>

        <!-- Game meta info row -->
        <div class="game-card-meta">
          <span>
            <i class="fas fa-repeat"></i>
            {{ game.rounds }} rounds
          </span>
          <span>
            <i class="fas fa-calendar-alt"></i>
            {{ formatDate(game.endedTime) }}
          </span>
          <span>
            <i class="fas fa-clock"></i>
            {{ formatDuration(game.startedTime, game.endedTime) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * GameInfo Component - Displays a list of all played games
 *
 * This component fetches game history from the backend GamesInfoEndpoint
 * and renders each game as a card in a list view. It parses and normalizes
 * the game data, resolves player names from the appeared_users mapping,
 * and determines win/loss status for appropriate color coding.
 *
 * @module GameInfo
 */
import { fetchGamesInfo, parseGameRecord } from '../utils/gamesService.js';
import userStore from '../stores/userStore.js';

export default {
  name: 'GameInfo',

  /**
   * Component data properties
   *
   * @property {Array<Object>} games - List of parsed game records
   * @property {Object} appearedUsers - Mapping of user IDs to display names
   * @property {boolean} isLoading - Flag indicating if data is being fetched
   * @property {string} errorMessage - Error message if the request fails
   */
  data() {
    return {
      games: [],
      appearedUsers: {},
      isLoading: true,
      errorMessage: ''
    };
  },

  /**
   * Component lifecycle hook
   *
   * Fetches game history when the component is mounted.
   */
  mounted() {
    this.fetchGames();
  },

  methods: {
    /**
     * Fetches all games for the current player
     *
     * Retrieves the player's credentials from the reactive userStore,
     * sends a request to the GamesInfoEndpoint, and stores the parsed
     * game records along with the appeared users mapping.
     *
     * @method fetchGames
     * @async
     * @returns {Promise<void>}
     */
    async fetchGames() {
      this.isLoading = true;
      this.errorMessage = '';

      try {
        const playerName = userStore.getUserName();
        const playerId = userStore.getUserId();

        if (!playerName || !playerId) {
          this.errorMessage = 'User not logged in';
          this.isLoading = false;
          return;
        }

        const response = await fetchGamesInfo(playerName, playerId);

        if (response.success && Array.isArray(response.data)) {
          this.appearedUsers = response.appeared_users || {};
          // Reverse the array so the most recent games appear at the top
          this.games = response.data.map(parseGameRecord).reverse();

        } else {
          this.errorMessage = response.reason || 'Failed to fetch game history';
        }
      } catch (error) {
        this.errorMessage = error.message || 'Failed to fetch game history';
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Gets the current player's user ID
     *
     * @method getPlayerId
     * @returns {string|null} The current player's user ID
     */
    getPlayerId() {
      return userStore.getUserId();
    },

    /**
     * Resolves a user ID to a display name
     *
     * Looks up the user ID in the appearedUsers mapping returned from the API.
     * Falls back to the user ID if the name is not found.
     *
     * @method getPlayerName
     * @param {string} userId - The user ID to look up
     * @returns {string} The display name or the user ID
     */
    getPlayerName(userId) {
      return this.appearedUsers[userId] || userId;
    },

    /**
     * Formats a score value for display
     *
     * If the score is null or undefined, returns 'N/A'. Otherwise returns the score.
     *
     * @method formatScore
     * @param {number|null} score - The score value to format
     * @returns {string|number} Formatted score string
     */
    formatScore(score) {
      if (score === null || score === undefined) {
        return 'N/A';
      }
      return score;
    },

    /**
     * Formats a Date object to a readable date string
     *
     * @method formatDate
     * @param {Date} date - The Date object to format
     * @returns {string} Formatted date string (YYYY-MM-DD)
     */
    formatDate(date) {
      if (!date || !(date instanceof Date) || isNaN(date.getTime())) {
        return 'N/A';
      }
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },

    /**
     * Calculates and formats the duration between two Date objects
     *
     * @method formatDuration
     * @param {Date} startTime - The start Date object
     * @param {Date} endTime - The end Date object
     * @returns {string} Duration string (e.g., '2m 15s')
     */
    formatDuration(startTime, endTime) {
      if (!startTime || !endTime) return 'N/A';
      const diffMs = endTime.getTime() - startTime.getTime();
      if (diffMs < 0) return 'N/A';
      const totalSeconds = Math.floor(diffMs / 1000);
      const minutes = Math.floor(totalSeconds / 60);
      const seconds = totalSeconds % 60;
      if (minutes > 0) {
        return `${minutes}m ${seconds}s`;
      }
      return `${seconds}s`;
    },

    /**
     * Determines if the current player won a given game
     *
     * @method isWin
     * @param {Object} game - The parsed game record
     * @returns {boolean} True if the current player is the winner
     */
    isWin(game) {
      return game.winner === this.getPlayerId();
    },

    /**
     * Determines if the current player lost a given game
     *
     * @method isLose
     * @param {Object} game - The parsed game record
     * @returns {boolean} True if the current player is not the winner
     */
    isLose(game) {
      return game.winner && game.winner !== this.getPlayerId();
    },

    /**
     * Gets the CSS class for the game card based on win/loss
     *
     * @method getCardClass
     * @param {Object} game - The parsed game record
     * @returns {string} CSS class name ('game-card--win' or 'game-card--lose')
     */
    getCardClass(game) {
      if (this.isWin(game)) return 'game-card--win';
      if (this.isLose(game)) return 'game-card--lose';
      return '';
    },

    /**
     * Gets the CSS class for the result icon row based on win/loss
     *
     * @method getResultClass
     * @param {Object} game - The parsed game record
     * @returns {string} CSS class name ('game-card-result--win' or 'game-card-result--lose')
     */
    getResultClass(game) {
      if (this.isWin(game)) return 'game-card-result--win';
      if (this.isLose(game)) return 'game-card-result--lose';
      return '';
    },

    /**
     * Gets the CSS class for a player side based on whether it's the current user
     *
     * If the given user ID matches the current player's ID, the side is marked
     * as 'is-user' (green text), otherwise 'is-opponent' (red text).
     *
     * @method getPlayerSideClass
     * @param {string} userId - The user ID of the player on this side
     * @returns {string} CSS class name ('player-side--is-user' or 'player-side--is-opponent')
     */
    getPlayerSideClass(userId) {
      if (userId === this.getPlayerId()) {
        return 'player-side--is-user';
      }
      return 'player-side--is-opponent';
    }
  }
};
</script>

<style scoped src="../assets/styles/game-info.css"></style>
