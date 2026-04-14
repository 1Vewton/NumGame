<!--
StartScreen.vue - Start Screen Component for NumGame

This component displays the welcome screen for the NumGame application.
It features a red and black color theme with the game title and a game icon.
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
  </div>
</template>

<script>
/**
 * StartScreen Component - Welcome screen for NumGame
 * 
 * This component displays the welcome screen with the game title,
 * game icon, and prepares the user for game start.
 * 
 * @module StartScreen
 */
export default {
  // Component name used for debugging and Vue devtools
  name: 'StartScreen',
  
  // Component lifecycle hook
  mounted() {
    console.log('StartScreen component mounted');
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
}

/* Space for future functionality elements */
.start-screen::after {
  content: '';
  flex-grow: 1; /* This will push future elements downward if added */
  min-height: 20vh; /* Reserve space at the bottom */
}
</style>