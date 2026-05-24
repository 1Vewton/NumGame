<!--
StartBotGame.vue - Bot Game Start Screen Component

This component displays the game setup screen for starting a Bot match.
It features a red and black color theme with a crosshairs icon and a
single input field for setting the game target number.

@module StartBotGame
-->
<template>
  <!-- Main start bot game screen container -->
  <div class="start-bot-game">
    <!-- Game icon - crosshairs targeting icon -->
    <div class="game-icon-container">
      <i class="fas fa-crosshairs fa-5x"></i>
    </div>

    <!-- Welcome text -->
    <div class="welcome-container">
      <h1 class="welcome-title">Bot Game</h1>
      <p class="welcome-subtitle">Set a target number and challenge the Bot</p>
    </div>

    <!-- Game setup form -->
    <div class="setup-form">
      <!-- Game target input field -->
      <AppInput
        v-model="targetNumber"
        type="number"
        placeholder="Enter the target number"
        label="Game Target"
        input-id="bot-target"
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
 * StartBotGame Component - Bot game setup screen
 * 
 * This component displays the game setup screen where the user can
 * set a target number before starting a match against the Bot.
 * It follows the same red and black color theme as the StartScreen.
 * 
 * @module StartBotGame
 */
import AppInput from './AppInput.vue';
import ErrorNotification from './ErrorNotification.vue';
import SuccessNotification from './SuccessNotification.vue';

export default {
  // Component name used for debugging and Vue devtools
  name: 'StartBotGame',

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
    ErrorNotification,
    SuccessNotification
  },

  /**
   * Component data properties
   * 
   * @property {string|number} targetNumber - The target number for the Bot game
   * @property {boolean} showError - Flag controlling error notification visibility
   * @property {string} errorMessage - The error message to display in the notification
   * @property {boolean} showSuccess - Flag controlling success notification visibility
   * @property {string} successMessage - The success message to display in the notification
   */
  data() {
    return {
      targetNumber: '',
      showError: false,
      errorMessage: '',
      showSuccess: false,
      successMessage: ''
    };
  },

  /**
   * Component lifecycle hook
   * 
   * Logs when the StartBotGame component is mounted to the DOM.
   */
  mounted() {
    console.log('StartBotGame component mounted');
  },

  /**
   * Component methods
   */
  methods: {
    // Internal logic will be added in future updates
  }
}
</script>

<style scoped>
/* Start Bot Game Screen Styles */
.start-bot-game {
  min-height: 100vh;
  background-color: #000000; /* Black background */
  color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* Move content up */
  padding-top: 15vh; /* Top padding to position content higher */
  padding-left: 2rem;
  padding-right: 2rem;
  padding-bottom: 2rem;
  margin: 0;
}

/* Game icon styling - Crosshairs icon */
.game-icon-container {
  margin-bottom: 2.5rem;
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
  margin-bottom: 2rem;
  max-width: 600px;
}

.welcome-title {
  font-size: 3.5rem;
  font-weight: 700;
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

/* Setup form styling */
.setup-form {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  margin-top: 1rem;
}

/* Responsive design */

@media (max-width: 768px) {
  .start-bot-game {
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

  .setup-form {
    max-width: 350px;
  }
}

@media (max-width: 480px) {
  .start-bot-game {
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

  .setup-form {
    max-width: 300px;
  }
}

/* Space for future functionality elements */
.start-bot-game::after {
  content: '';
  flex-grow: 1;
  min-height: 20vh; /* Reserve space at the bottom */
}
</style>
