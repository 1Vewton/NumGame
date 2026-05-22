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
      <!-- Username input field -->
      <AppInput
        v-model="registerUsername"
        type="text"
        placeholder="Enter your username"
        label="Username"
        input-id="register-username"
      />

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
import apiClient from '../utils/api.js';
import config from '../utils/config.js';
import { getUserLoginBody, getUserRegisterBody } from '../utils/requestBodies.js';
import userStore from '../stores/userStore.js';
import { extractErrorMessage } from '../utils/errorHandler.js';



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
   */
  components: {
    AppInput,
    AppButton,
    ErrorNotification,
    SuccessNotification
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
      successMessage: ''
    };
  },

  /**
   * Computed properties
   */
  computed: {
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
   */
  mounted() {
    console.log('StartScreen component mounted');
  },

  /**
   * Component methods
   */
  methods: {
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
        // Get the login endpoint and request body
        const loginEndpoint = config.getLoginEndpoint();
        const requestBody = getUserLoginBody(this.username.trim(), this.password);

        // Send the login request to the backend
        const response = await apiClient.post(loginEndpoint, requestBody);

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
        // Get the register endpoint and request body
        const registerEndpoint = config.getRegisterEndpoint();
        const requestBody = getUserRegisterBody(this.registerUsername.trim(), this.registerPassword);

        // Send the registration request to the backend
        const response = await apiClient.post(registerEndpoint, requestBody);

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

/* Password format hint styling */
.password-hint {
  font-size: 0.8rem;
  color: #aaaaaa;
  line-height: 1.4;
  padding: 0 0.2rem;
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
