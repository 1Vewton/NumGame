<!--
App.vue - Main Application Component
This is the root component of the NumGame frontend application.
It serves as the entry point for the Vue.js application and renders
the main layout with the game interface.
-->

<template>
  <!-- Main application container -->
  <div id="app">
    <!-- Vue logo (placeholder for game logo) -->
    <img alt="Vue logo" src="./assets/logo.png">
    <!-- HelloWorld component - placeholder for actual game components -->
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// Import the HelloWorld component
import HelloWorld from './components/HelloWorld.vue'

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
    HelloWorld
  }
}
</script>

<style>
/* Global application styles */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
