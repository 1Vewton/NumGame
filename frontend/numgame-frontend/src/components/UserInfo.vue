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

      <!-- Log out button -->
      <div class="logout-button-container">
        <AppButton
          label="Log Out"
          variant="primary"
          size="medium"
          width="100%"
          :disabled="isLoggingOut"
          @click="handleLogOut"
        />
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
      <!-- Logout error notification -->
      <ErrorNotification
        :visible="showLogoutError"
        :message="logoutErrorMessage"
        @close="showLogoutError = false"
      />
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
import ErrorNotification from './ErrorNotification.vue';
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
   * @property {Component} AppButton - Reusable styled button component
   * @property {Component} ErrorNotification - Reusable error notification toast component
   */
  components: {
    AppButton,
    ErrorNotification
  },

  /**
   * Component data properties
   * 
   * @property {Object|null} userInfo - The fetched user information object from the API
   * @property {boolean} isLoading - Flag indicating if the API request is in progress
   * @property {string} errorMessage - The error message to display
   * @property {boolean} isLoggingOut - Flag indicating if a log out request is in progress
   * @property {boolean} showError - Flag controlling the error notification visibility
   */
  data() {
    return {
      userInfo: null,
      isLoading: true,
      errorMessage: '',
      isLoggingOut: false,
      showLogoutError: false,
      logoutErrorMessage: ''
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
    },

    /**
     * Handles user log out
     * 
     * Sends a GET request to the log out endpoint to terminate the server-side session.
     * If the response contains "success": true, clears all stored user data via
     * userStore.clearAll() and reloads the page to reset the application state.
     * If the response contains "success": false, displays an error notification
     * with the reason from the response.
     * 
     * @method handleLogOut
     * @async
     * @returns {Promise<void>}
     */
    async handleLogOut() {
      this.isLoggingOut = true;
      this.logoutErrorMessage = '';
      this.showLogoutError = false;

      try {
        // Send GET request to the log out endpoint
        const logOutUrl = config.getLogOutUrl();
        const response = await apiClient.get(logOutUrl);

        if (response.success) {
          // Logout successful — clear data and reload
          userStore.clearAll();
          window.location.reload();
        } else {
          // Logout failed — show error notification with reason
          this.logoutErrorMessage = response.reason || 'Logout failed';
          this.showLogoutError = true;
          this.isLoggingOut = false;
        }
      } catch (error) {
        // Even if the request fails, clear local data and reload
        userStore.clearAll();
        window.location.reload();
      }
    }
  }
};
</script>

<style scoped src="../assets/styles/user-info.css"></style>
