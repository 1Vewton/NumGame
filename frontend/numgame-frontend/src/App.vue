<!--
App.vue - Main Application Component
This is the root component of the NumGame frontend application.
It serves as the entry point for the Vue.js application and renders
the main layout with the game interface.
-->

<template>
  <!-- Main application container -->
  <div id="app">
    <!-- StartScreen component - Welcome screen with red+black theme -->
    <StartScreen />
  </div>
</template>

<script>
// Import the StartScreen component
import StartScreen from './components/StartScreen.vue'

/**
 * App Component - Root component of the NumGame application
 * 
 * This component initializes the main Vue application and registers
 * all child components used in the application.
 * 
 * @module App
 */
export default {
  // Component name used for debugging and Vue devtools
  name: 'App',
  
  // Child components registered in this component
  components: {
    StartScreen
  }
}
</script>

<style>
/* Global application styles */
#app {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  font-family: 'Cascadia Code', 'Consolas', 'Monaco', 'Courier New', monospace;
}
</style>
