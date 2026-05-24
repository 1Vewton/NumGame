<!--
UserInfo.vue - User Information Overlay Component

This component displays the logged-in user's profile information in a modal overlay.
It fetches user data from the backend API using the player_name and player_id stored
in the userStore. The password field is excluded from display, and the registered_at
timestamp is converted to a human-readable date format. The component uses the same
red and black color theme as the rest of the application.

@module UserInfo
-->
<template>
  <!-- Overlay background -->
  <div class="user-info-overlay">
    <!-- Modal container -->
    <div class="user-info-modal">
      <!-- Header with title and close button -->
      <div class="user-info-header">
        <h2 class="user-info-title">User Information</h2>
        <button class="close-button" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- Loading state -->
      <div v-if="isLoading" class="loading-state">
        <i class="fas fa-spinner fa-spin loading-spinner"></i>
        <span>Loading user information...</span>
      </div>

      <!-- Error state -->
      <div v-else-if="errorMessage" class="error-state">
        <i class="fas fa-exclamation-triangle"></i>
        <span>{{ errorMessage }}</span>
      </div>

      <!-- User info content -->
      <div v-else-if="userInfo" class="user-info-content">
        <!-- User ID -->
        <div class="info-row">
          <span class="info-label">User ID</span>
          <span class="info-value">{{ userInfo.id }}</span>
        </div>

        <!-- Username -->
        <div class="info-row">
          <span class="info-label">Username</span>
          <span class="info-value">{{ userInfo.user_name }}</span>
        </div>

        <!-- Registration Date (converted from timestamp) -->
        <div class="info-row">
          <span class="info-label">Registered At</span>
          <span class="info-value">{{ formattedDate }}</span>
        </div>

        <!-- Wins -->
        <div class="info-row">
          <span class="info-label">Wins</span>
          <span class="info-value">{{ userInfo.wins }}</span>
        </div>

        <!-- Total Games -->
        <div class="info-row">
          <span class="info-label">Total Games</span>
          <span class="info-value">{{ userInfo.total_games }}</span>
        </div>

        <!-- Win Rate (N/A if no games played) -->
        <div class="info-row">
          <span class="info-label">Win Rate</span>
          <span class="info-value">{{ winRate }}</span>
        </div>
      </div>

      <!-- Back button -->
      <div class="back-button-container">
        <AppButton
          label="Back"
          variant="primary"
          size="medium"
          width="100%"
          @click="$emit('close')"
        />
      </div>
    </div>
  </div>
</template>

<script>
/**
 * UserInfo Component - Displays user profile information in a modal overlay
 * 
 * This component fetches user information from the backend API using the
 * player_name and player_id stored in the userStore. It displays the user
 * profile data (excluding password) with a red and black theme matching
 * the application's design. The registered_at timestamp is formatted as
 * a readable date string (YYYY-MM-DD).
 * 
 * @module UserInfo
 */
import AppButton from './AppButton.vue';
import apiClient from '../utils/api.js';
import config from '../utils/config.js';
import userStore from '../stores/userStore.js';
import { getUserInfoBody } from '../utils/requestBodies.js';
import { extractErrorMessage } from '../utils/errorHandler.js';

export default {
  name: 'UserInfo',

  /**
   * Child components registered in this component
   * 
   * @property {Component} AppButton - Reusable styled button component for the Back button
   */
  components: {
    AppButton
  },

  /**
   * Component data properties
   * 
   * @property {Object|null} userInfo - The fetched user information object from the API
   * @property {boolean} isLoading - Flag indicating if the API request is in progress
   * @property {string} errorMessage - The error message to display if the request fails
   */
  data() {
    return {
      userInfo: null,
      isLoading: true,
      errorMessage: ''
    };
  },

  /**
   * Computed properties
   */
  computed: {
    /**
     * Formatted registration date
     * 
     * Converts the Unix timestamp (seconds since epoch) from registered_at
     * into a human-readable date string in YYYY-MM-DD format.
     * 
     * @returns {string} Formatted date string (e.g., '2026-05-24')
     */
    formattedDate() {
      if (!this.userInfo || !this.userInfo.registered_at) {
        return 'N/A';
      }
      const date = new Date(this.userInfo.registered_at * 1000);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },

    /**
     * Calculated win rate percentage
     * 
     * Computes the win rate as (wins / total_games) * 100, formatted to
     * one decimal place with a percent sign. If total_games is 0, returns 'N/A'
     * to avoid division by zero.
     * 
     * @returns {string} Win rate percentage (e.g., '75.0%') or 'N/A'
     */
    winRate() {
      if (!this.userInfo || this.userInfo.total_games === 0) {
        return 'N/A';
      }
      const rate = (this.userInfo.wins / this.userInfo.total_games) * 100;
      return `${rate.toFixed(1)}%`;
    }
  },

  /**
   * Component lifecycle hook
   * 
   * Fetches user information from the backend API when the component is mounted.
   * Uses the user's ID and name from the reactive userStore to build the request body.
   */
  mounted() {
    this.fetchUserInfo();
  },

  methods: {
    /**
     * Fetches user information from the backend API
     * 
     * This method retrieves the user's profile data by sending a POST request
     * to the user info endpoint with the user's player_name and player_id from
     * the reactive userStore. On success, it stores the response data in userInfo.
     * On failure, it displays an error message.
     * 
     * @method fetchUserInfo
     * @async
     * @returns {Promise<void>}
     */
    async fetchUserInfo() {
      this.isLoading = true;
      this.errorMessage = '';

      try {
        // Get user credentials from the reactive store
        const playerName = userStore.getUserName();
        const playerId = userStore.getUserId();

        // Validate that user is logged in
        if (!playerName || !playerId) {
          this.errorMessage = 'User not logged in';
          this.isLoading = false;
          return;
        }

        // Build the request body and endpoint
        const userInfoEndpoint = config.getUserEndpoint();
        const requestBody = getUserInfoBody(playerName, playerId);

        // Send the request to the backend API
        const response = await apiClient.post(userInfoEndpoint, requestBody);

        // Check if the request was successful
        if (response.success && response.result) {
          this.userInfo = response.result;
        } else {
          this.errorMessage = response.reason || 'Failed to fetch user information';
        }
      } catch (error) {
        // Use the unified error handler to extract the most meaningful error message
        this.errorMessage = extractErrorMessage(error, 'Failed to fetch user information');
      } finally {
        // Reset loading state
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Overlay background - full screen dark backdrop */
.user-info-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

/* Modal container */
.user-info-modal {
  background-color: #1a1a1a;
  border: 1px solid #ff0000;
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 0 30px rgba(255, 0, 0, 0.3);
  animation: fadeIn 0.3s ease;
}

/* Fade-in animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Modal header */
.user-info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #333333;
}

.user-info-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ff0000;
  margin: 0;
  text-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
}

/* Close button in header */
.close-button {
  background: none;
  border: none;
  color: #888888;
  font-size: 1.3rem;
  cursor: pointer;
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  transition: color 0.2s, background-color 0.2s;
}

.close-button:hover {
  color: #ff0000;
  background-color: rgba(255, 0, 0, 0.1);
}

/* Loading state */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
  color: #cccccc;
  gap: 1rem;
  font-size: 1rem;
}

.loading-spinner {
  font-size: 2rem;
  color: #ff0000;
}

/* Error state */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
  color: #ff4444;
  gap: 1rem;
  font-size: 1rem;
  text-align: center;
}

.error-state i {
  font-size: 2rem;
}

/* User info content area */
.user-info-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 0.5rem 0;
}

/* Individual info row */
.info-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 0.7rem 1rem;
  background-color: #2a2a2a;
  border-radius: 6px;
  border-left: 3px solid #ff0000;
}

.info-label {
  color: #aaaaaa;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  min-width: 120px;
}

.info-value {
  color: #ffffff;
  font-size: 0.9rem;
  text-align: right;
  word-break: break-all;
}

/* Back button container */
.back-button-container {
  margin-top: 0.5rem;
}

/* Responsive design */
@media (max-width: 480px) {
  .user-info-modal {
    padding: 1.5rem;
    max-width: 100%;
  }

  .user-info-title {
    font-size: 1.2rem;
  }

  .info-row {
    flex-direction: column;
    gap: 0.3rem;
  }

  .info-value {
    text-align: left;
  }
}
</style>
