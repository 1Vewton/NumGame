<!--
StartScreen.vue - Start Screen Component for NumGame

This component displays the welcome screen for the NumGame application.
It features a red and black color theme with the game title, login form,
registration form, and notification functionality. The component supports
switching between login and registration views. The registration form
includes password format validation and confirm password matching.

@module StartScreen
-->
<template>
  <!-- Main start screen container -->
  <div class="start-screen">
    <!-- Game rules icon button (top-left corner) -->
    <div class="rules-icon-container">
      <button class="rules-icon-button" @click="showGameRules = true" title="Game Rules">
        <i class="fas fa-circle-info fa-2x"></i>
      </button>
    </div>

    <!-- User info icon button (top-right corner, only visible when logged in) -->
    <div v-if="loggedIn" class="user-icon-container">
      <button class="user-icon-button" @click="showUserInfo = true" title="User Info">
        <i class="fas fa-circle-user fa-2x"></i>
      </button>
    </div>

    <!-- Game history icon button (top-right corner, only visible when logged in) -->
    <div v-if="loggedIn" class="history-icon-container">
      <button class="history-icon-button" @click="goToGameInfo" title="Game History">
        <i class="fas fa-clock-rotate-left fa-2x"></i>
      </button>
    </div>


    <!-- User information modal overlay -->
    <UserInfo v-if="showUserInfo" @close="showUserInfo = false" />

    <!-- Game rules modal overlay (reusable component) -->
    <GameRulesModal
      :visible="showGameRules"
      @close="showGameRules = false"
    />

    <!-- Game icon -->
    <div class="game-icon-container">
      <!-- Font Awesome x-mark icon -->
      <i class="fas fa-xmark fa-5x"></i>
    </div>

    <!-- Welcome text -->
    <div class="welcome-container">
      <h1 class="welcome-title">Welcome to Numgame!</h1>
      <p class="welcome-subtitle">A strategic number-based game</p>
    </div>

    <!-- Game mode selection (shown after successful login) -->
    <div v-if="loggedIn" class="game-mode-container">
      <!-- PVE button - the only playable mode -->
      <div class="game-mode-item">
        <i class="fas fa-robot game-mode-icon"></i>
        <AppButton
          label="PVE"
          variant="primary"
          size="large"
          width="100%"
          @click="goToBotGame"
        />
        <span class="game-mode-tooltip">Play against a state machine Bot</span>
      </div>

      <!-- PVP button - disabled -->
      <div class="game-mode-item">
        <i class="fas fa-people-group game-mode-icon"></i>
        <AppButton
          label="PVP"
          variant="secondary"
          size="large"
          width="100%"
          :disabled="true"
        />
        <span class="game-mode-tooltip">Play against other players</span>
      </div>

      <!-- LLM button - disabled -->
      <div class="game-mode-item">
        <i class="fas fa-brain game-mode-icon"></i>

        <AppButton
          label="LLM"
          variant="secondary"
          size="large"
          width="100%"
          :disabled="true"
        />
        <span class="game-mode-tooltip">Play against an LLM</span>
      </div>

      <!-- AI button - disabled -->
      <div class="game-mode-item">
        <i class="fas fa-fax game-mode-icon"></i>

        <AppButton
          label="AI"
          variant="secondary"
          size="large"
          width="100%"
          :disabled="true"
        />
        <span class="game-mode-tooltip">Play against a reinforcement learning model</span>
      </div>

    </div>


    <!-- Login form (hidden after successful login) -->
    <div v-if="!loggedIn">

      <div v-if="showLogin" class="login-form">
        <!-- Username input field -->
        <AppInput
          v-model="username"
          type="text"
          placeholder="Enter your username"
          label="Username"
          input-id="login-username"
          @enter="handleLogin"
        />

        <!-- Password input field -->
        <AppInput
          v-model="password"
          type="password"
          placeholder="Enter your password"
          label="Password"
          input-id="login-password"
          @enter="handleLogin"
        />

        <!-- Login button using reusable AppButton component -->
        <AppButton
          label="Login"
          :is-loading="isLoggingIn"
          loading-label="Logging in..."
          variant="primary"
          size="medium"
          width="100%"
          @click="handleLogin"
        />

        <!-- Register button using reusable AppButton component -->
        <AppButton
          label="Register"
          variant="primary"
          size="medium"
          width="100%"
          @click="switchToRegister"
        />

      </div>

      <!-- Registration form -->
      <div v-else class="login-form">
        <!-- Username input field with random generation button -->
        <div class="register-username-wrapper">
          <AppInput
            v-model="registerUsername"
            type="text"
            placeholder="Enter your username"
            label="Username"
            input-id="register-username"
          />
          <button
            class="random-username-button"
            @click="generateRandomUsername"
            title="Generate random username"
          >
            <i class="fas fa-arrows-rotate"></i>
          </button>
        </div>

        <!-- Password input field -->
        <AppInput
          v-model="registerPassword"
          type="password"
          placeholder="Enter your password"
          label="Password"
          input-id="register-password"
        />

        <!-- Confirm password input field -->
        <AppInput
          v-model="registerConfirmPassword"
          type="password"
          placeholder="Confirm your password"
          label="Confirm Password"
          input-id="register-confirm-password"
        />

        <!-- Password format hint -->
        <div class="password-hint">
          Password must be at least 8 characters, with at least one uppercase letter,
          one lowercase letter, one digit, and one special character (@$!%*?&)
        </div>

        <!-- Register button - primary when valid, secondary when invalid -->
        <AppButton
          label="Register"
          :is-loading="isRegistering"
          loading-label="Registering..."
          :variant="canRegister ? 'primary' : 'secondary'"
          size="medium"
          width="100%"
          :disabled="!canRegister || isRegistering"
          @click="handleRegister"
        />

        <!-- Back to Login button -->
        <AppButton
          label="Back to Login"
          variant="primary"
          size="medium"
          width="100%"
          @click="switchToLogin"
        />

      </div>
    </div>

    <!-- Error notification toast -->
    <ErrorNotification
      :visible="showError"
      :message="errorMessage"
      @close="showError = false"
    />

    <!-- Success notification toast -->
    <SuccessNotification
      :visible="showSuccess"
      @close="showSuccess = false"
    >
      {{ successMessage }}
    </SuccessNotification>

  </div>
</template>

<script>
/**
 * StartScreen Component - Welcome screen with login and registration functionality
 * 
 * This component displays the welcome screen with the game title,
 * game icon, and a form that can switch between login and registration views.
 * It uses the reusable AppInput component for input fields and the reusable
 * ErrorNotification component for displaying error messages.
 * The registration form validates password format and confirm password matching.
 * 
 * @module StartScreen
 */
import AppInput from './AppInput.vue';
import AppButton from './AppButton.vue';
import ErrorNotification from './ErrorNotification.vue';
import SuccessNotification from './SuccessNotification.vue';
import UserInfo from './UserInfo.vue';
import GameRulesModal from './GameRulesModal.vue';
import userStore from '../stores/userStore.js';
import { extractErrorMessage } from '../utils/errorHandler.js';
import { login, register, autoLogin } from '../utils/authService.js';
import { generateUserName } from '../utils/gamesService.js';



/**
 * Regular expression for password validation
 * Requires at least 8 characters, one uppercase letter, one lowercase letter,
 * one digit, and one special character (@$!%*?&)
 */
const PASSWORD_REGEX = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

export default {
  // Component name used for debugging and Vue devtools
  name: 'StartScreen',

  /**
   * Child components registered in this component
   * 
   * @property {Component} AppInput - Reusable white input field component
   * @property {Component} AppButton - Reusable styled button component
   * @property {Component} ErrorNotification - Reusable error toast notification component
   * @property {Component} SuccessNotification - Reusable success toast notification component
   * @property {Component} UserInfo - User information modal overlay component
   */
  components: {
    AppInput,
    AppButton,
    ErrorNotification,
    SuccessNotification,
    UserInfo,
    GameRulesModal
  },

  /**
   * Component data properties
   * 
   * @property {string} username - The username entered by the user (login form)
   * @property {string} password - The password entered by the user (login form)
   * @property {boolean} isLoggingIn - Flag indicating if a login request is in progress
   * @property {boolean} isRegistering - Flag indicating if a registration request is in progress
   * @property {boolean} showLogin - Flag indicating whether to show login or registration form
   * @property {string} registerUsername - The username entered in the registration form
   * @property {string} registerPassword - The password entered in the registration form
   * @property {string} registerConfirmPassword - The confirm password entered in the registration form
   * @property {boolean} showError - Flag controlling error notification visibility
   * @property {string} errorMessage - The error message to display in the notification
   * @property {boolean} showSuccess - Flag controlling success notification visibility
   * @property {string} successMessage - The success message to display in the notification
   * @property {boolean} showUserInfo - Flag controlling the user info modal visibility
   * @property {boolean} showGameRules - Flag controlling the game rules modal visibility
   */
  data() {
    return {
      username: '',
      password: '',
      isLoggingIn: false,
      isRegistering: false,
      showLogin: true,
      registerUsername: '',
      registerPassword: '',
      registerConfirmPassword: '',
      showError: false,
      errorMessage: '',
      showSuccess: false,
      successMessage: '',
      showUserInfo: false,
      showGameRules: false
    };

  },

  /**
   * Computed properties
   */
  computed: {
    /**
     * Indicates whether the user is currently logged in
     * 
     * Returns the login status from the reactive userStore.
     * When true, the login/registration forms are hidden.
     * 
     * @returns {boolean} True if user is logged in
     */
    loggedIn() {
      return userStore.isUserLoggedIn();
    },

    /**
     * Determines whether the registration button should be enabled
     * 
     * Returns true only when the password meets the format requirements
     * and the confirm password matches the password.
     * 
     * @returns {boolean} True if registration form data is valid
     */
    canRegister() {
      return (
        PASSWORD_REGEX.test(this.registerPassword) &&
        this.registerConfirmPassword === this.registerPassword
      );
    }
  },


  /**
   * Component lifecycle hook
   * 
   * Logs when the StartScreen component is mounted to the DOM.
   * Triggers an automatic login attempt to check if the user has
   * an existing session via cookies/tokens. No notifications are
   * shown regardless of success or failure.
   */
  mounted() {
    console.log('StartScreen component mounted');
    this.handleAutoLogin();
  },


  /**
   * Component methods
   */
  methods: {
    /**
     * Handles automatic login attempt on component mount
     * 
     * This method sends a GET request to the auto-login endpoint without
     * any request body. If the server returns success with user data, the
     * user is automatically logged in (form fields disappear). If auto-login
     * fails or the server returns an error, no notification is shown to the
     * user - they will simply see the normal login form.
     * 
     * @method handleAutoLogin
     * @async
     * @returns {Promise<void>}
     */
    async handleAutoLogin() {
      const response = await autoLogin();

      if (response.success) {
        // Auto-login succeeded - store user data silently
        userStore.setUser(response.user_id, response.user_name);
        console.log('Auto-login successful:', response.user_name, response.user_id);
      }
      // Auto-login failed silently - no notification shown
    },

    /**
     * Switches the view to the registration form
     * 
     * This method sets showLogin to false, which triggers the v-if directive
     * to display the registration form instead of the login form.
     * 
     * @method switchToRegister
     */
    switchToRegister() {
      this.showLogin = false;
    },


    /**
     * Switches the view to the login form
     * 
     * This method sets showLogin to true, which triggers the v-if directive
     * to display the login form instead of the registration form.
     * 
     * @method switchToLogin
     */
    switchToLogin() {
      this.showLogin = true;
    },

    /**
     * Handles the user login process
     * 
     * This method validates that both username and password are provided,
     * then sends a login request to the backend API. On success, it stores
     * the user's ID and name in the reactive userStore. On failure, it
     * displays an error notification toast with the reason from the server response.
     * 
     * @method handleLogin
     * @async
     * @returns {Promise<void>}
     */
    async handleLogin() {
      // Validate that username and password are provided
      if (!this.username.trim() || !this.password.trim()) {
        this.showErrorMessage('Please enter both username and password');
        return;
      }

      // Set loading state to prevent duplicate submissions
      this.isLoggingIn = true;

      try {
        const response = await login(this.username.trim(), this.password);

        // Check if login was successful
        if (response.success) {
          // Store user information in the reactive in-memory userStore
          userStore.setUser(response.user_id, response.user_name);
          console.log('Login successful:', response.user_name, response.user_id);

          // Set success message and show success notification toast
          this.successMessage = 'Login Successful';
          this.showSuccess = true;

        } else {
          // Display the error reason from the server response
          this.showErrorMessage(response.reason || 'Login failed');
        }
      } catch (error) {
        // Use the unified error handler to extract the most meaningful error message
        this.showErrorMessage(extractErrorMessage(error, 'Login failed'));

      } finally {
        // Reset loading state
        this.isLoggingIn = false;
      }
    },

    /**
     * Shows an error notification toast with the specified message
     * 
     * This method sets the error message and makes the notification visible.
     * The notification will auto-dismiss after 1 second via the ErrorNotification component.
     * 
     * @method showErrorMessage
     * @param {string} message - The error message to display
     */
    showErrorMessage(message) {
      this.errorMessage = message;
      this.showError = true;
    },

    /**
     * Handles the user registration process
     * 
     * This method validates that the registration form data is complete and valid,
     * then sends a registration request to the backend API. On success, it displays
     * a success notification toast. On failure, it displays an error notification
     * toast with the reason from the server response.
     * 
     * @method handleRegister
     * @async
     * @returns {Promise<void>}
     */
    async handleRegister() {
      // Set loading state to prevent duplicate submissions
      this.isRegistering = true;

      try {
        const response = await register(this.registerUsername.trim(), this.registerPassword);

        // Check if registration was successful
        if (response.success) {
          console.log('Registration successful for:', this.registerUsername.trim());

          // Set success message and show success notification toast
          this.successMessage = 'Registration Successful';
          this.showSuccess = true;

          // Switch back to login screen after successful registration
          this.switchToLogin();

        } else {
          // Display the error reason from the server response
          this.showErrorMessage(response.reason || 'Registration failed');
        }
      } catch (error) {
        // Use the unified error handler to extract the most meaningful error message
        this.showErrorMessage(extractErrorMessage(error, 'Registration failed'));

      } finally {
        // Reset loading state
        this.isRegistering = false;
      }
    },

    /**
     * Generates a random username via the backend API
     * 
     * This method sends a GET request to the user name generation endpoint.
     * On success, it fills the registration username field with the generated
     * username from the server response.
     * 
     * @method generateRandomUsername
     * @async
     * @returns {Promise<void>}
     */
    async generateRandomUsername() {
      try {
        const response = await generateUserName();

        if (response.success && response.username) {
          this.registerUsername = response.username;
        } else {
          this.showErrorMessage(response.reason || 'Failed to generate username');
        }
      } catch (error) {
        this.showErrorMessage(extractErrorMessage(error, 'Failed to generate username'));
      }
    },

    /**
     * Navigates to the Bot game setup screen
     * 
     * This method uses Vue Router to navigate to the /startBotGame route,
     * which renders the StartBotGame component where the user can set a
     * target number and start a game against the Bot.
     * 
     * @method goToBotGame
     */
    goToBotGame() {
      this.$router.push({ name: 'StartBotGame' });
    },

    /**
     * Navigates to the Game History page
     * 
     * This method uses Vue Router to navigate to the /gameInfo route,
     * which renders the GameInfo component showing a list of all games
     * the player has participated in.
     * 
     * @method goToGameInfo
     */
    goToGameInfo() {
      this.$router.push({ name: 'GameInfo' });
    }
  }

}
</script>

<style scoped src="../assets/styles/start-screen.css"></style>


