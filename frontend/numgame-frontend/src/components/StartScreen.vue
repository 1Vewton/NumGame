<!--
StartScreen.vue - Start Screen Component for NumGame

This component displays the welcome screen for the NumGame application.
It features a red and black color theme with the game title, login form,
and error notification functionality. Users can enter their credentials
to log in, and their user information is stored in the browser's localStorage
upon successful authentication.

@module StartScreen
-->
<template>
  <!-- Main start screen container -->
  <div class="start-screen">
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

    <!-- Login form -->
    <div class="login-form">
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

      <!-- Login button -->
      <button
        class="login-button"
        @click="handleLogin"
        :disabled="isLoggingIn"
      >
        {{ isLoggingIn ? 'Logging in...' : 'Login' }}
      </button>
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
      Login Successful
    </SuccessNotification>

  </div>
</template>

<script>
/**
 * StartScreen Component - Welcome screen with login functionality
 * 
 * This component displays the welcome screen with the game title,
 * game icon, and a login form for user authentication. It uses
 * the reusable AppInput component for input fields and the reusable
 * ErrorNotification component for displaying login error messages.
 * On successful login, the user's ID and name are stored in localStorage
 * for session persistence.
 * 
 * @module StartScreen
 */
import AppInput from './AppInput.vue';
import ErrorNotification from './ErrorNotification.vue';
import SuccessNotification from './SuccessNotification.vue';
import apiClient from '../utils/api.js';
import config from '../utils/config.js';
import { getUserLoginBody } from '../utils/requestBodies.js';


export default {
  // Component name used for debugging and Vue devtools
  name: 'StartScreen',

  /**
   * Child components registered in this component
   * 
   * @property {Component} AppInput - Reusable white input field component
   * @property {Component} ErrorNotification - Reusable error toast notification component
   */
  components: {
    AppInput,
    ErrorNotification,
    SuccessNotification
  },


  /**
   * Component data properties
   * 
   * @property {string} username - The username entered by the user
   * @property {string} password - The password entered by the user
   * @property {boolean} isLoggingIn - Flag indicating if a login request is in progress
   * @property {boolean} showError - Flag controlling error notification visibility
   * @property {string} errorMessage - The error message to display in the notification
   */
  data() {
    return {
      /**
       * The username entered by the user in the login form
       * @type {string}
       */
      username: '',

      /**
       * The password entered by the user in the login form
       * @type {string}
       */
      password: '',

      /**
       * Flag indicating whether a login request is currently in progress
       * Used to disable the login button and prevent multiple submissions
       * @type {boolean}
       */
      isLoggingIn: false,

      /**
       * Flag controlling the visibility of the error notification toast
       * @type {boolean}
       */
      showError: false,

      /**
       * The error message text to display in the notification toast
       * @type {string}
       */
      errorMessage: '',

      /**
       * Flag controlling the visibility of the success notification toast
       * @type {boolean}
       */
      showSuccess: false
    };

  },

  /**
   * Component lifecycle hook
   * 
   * Logs when the StartScreen component is mounted to the DOM.
   */
  mounted() {
    console.log('StartScreen component mounted');
  },

  /**
   * Component methods
   */
  methods: {
    /**
     * Handles the user login process
     * 
     * This method validates that both username and password are provided,
     * then sends a login request to the backend API. On success, it stores
     * the user's ID and name in localStorage. On failure, it displays an
     * error notification toast with the reason from the server response.
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
        // Get the login endpoint and request body
        const loginEndpoint = config.getLoginEndpoint();
        const requestBody = getUserLoginBody(this.username.trim(), this.password);

        // Send the login request to the backend
        const response = await apiClient.post(loginEndpoint, requestBody);

        // Check if login was successful
        if (response.success) {
          // Store user information in localStorage for session persistence
          localStorage.setItem('user_id', response.user_id);
          localStorage.setItem('user_name', response.user_name);
          console.log('Login successful:', response.user_name, response.user_id);
          // Show success notification toast
          this.showSuccess = true;

        } else {
          // Display the error reason from the server response
          this.showErrorMessage(response.reason || 'Login failed');
        }
      } catch (error) {
        // Handle network errors or unexpected failures
        this.showErrorMessage(error.message || 'Unable to connect to server');
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
    }
  }
}
</script>

<style scoped>
/* Start Screen Styles - Adjusted for future functionality */
.start-screen {
  min-height: 100vh;
  background-color: #000000; /* Black background */
  color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* Changed from center to flex-start to move content up */
  padding-top: 15vh; /* Add top padding to position content higher */
  padding-left: 2rem;
  padding-right: 2rem;
  padding-bottom: 2rem;
  margin: 0;
}

/* Game icon styling - Simple red X without any background */
.game-icon-container {
  margin-bottom: 2.5rem; /* Slightly reduced margin */
  margin-top: 2rem;
}

.fa-5x {
  color: #ff0000; /* Red icon */
  text-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  font-size: 5rem; /* Use rem units for better scaling */
}

/* Welcome text styling */
.welcome-container {
  text-align: center;
  margin-bottom: 2rem; /* Reduced margin to leave space for future elements */
  max-width: 600px;
}

.welcome-title {
  font-size: 3.5rem; /* Slightly reduced from 4rem */
  font-weight: 700; /* Slightly reduced weight */
  margin-bottom: 0.8rem;
  background: linear-gradient(to right, #ff0000, #ff6666);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
  letter-spacing: 1.5px;
}

.welcome-subtitle {
  font-size: 1.3rem;
  color: #cccccc;
  font-weight: 300;
  letter-spacing: 0.8px;
}

/* Login form styling */
.login-form {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  margin-top: 1rem;
}

/* Login button styling */
.login-button {
  width: 100%;
  padding: 12px 20px;
  background-color: #ff0000;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 600;
  font-family: 'Cascadia Code', 'Consolas', 'Monaco', 'Courier New', monospace;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  letter-spacing: 1px;
  margin-top: 0.5rem;
}

/* Login button hover state */
.login-button:hover:not(:disabled) {
  background-color: #cc0000;
  box-shadow: 0 0 12px rgba(255, 0, 0, 0.5);
}

/* Login button active/pressed state */
.login-button:active:not(:disabled) {
  background-color: #990000;
}

/* Login button disabled state */
.login-button:disabled {
  background-color: #662222;
  cursor: not-allowed;
  opacity: 0.7;
}

/* Responsive design */
@media (max-width: 768px) {
  .start-screen {
    padding-top: 12vh; /* Adjust top padding for smaller screens */
  }
  
  .welcome-title {
    font-size: 2.8rem;
  }
  
  .fa-5x {
    font-size: 4rem;
  }
  
  .game-icon-container {
    margin-bottom: 2rem;
  }

  .login-form {
    max-width: 350px;
  }
}

@media (max-width: 480px) {
  .start-screen {
    padding-top: 10vh; /* Further adjust for mobile */
  }
  
  .welcome-title {
    font-size: 2rem;
  }
  
  .welcome-subtitle {
    font-size: 1.1rem;
  }
  
  .fa-5x {
    font-size: 3.5rem;
  }
  
  .game-icon-container {
    margin-bottom: 1.5rem;
  }

  .login-form {
    max-width: 300px;
  }
}

/* Space for future functionality elements */
.start-screen::after {
  content: '';
  flex-grow: 1; /* This will push future elements downward if added */
  min-height: 20vh; /* Reserve space at the bottom */
}
</style>
