<!--
App.vue - Main Application Component
This is the root component of the NumGame frontend application.
It serves as the entry point for the Vue.js application and renders
the current route's view component using Vue Router's router-view.
-->

<template>
  <!-- Main application container -->
  <div id="app">
    <!-- 
      Router view - Renders the component mapped to the current route
      When accessing / (no endpoint), StartScreen will be displayed.
    -->
    <router-view />
  </div>
</template>

<script>
/**
 * App Component - Root component of the NumGame application
 * 
 * This component initializes the main Vue application layout and
 * uses Vue Router to render the appropriate view component based
 * on the current URL path.
 * 
 * @module App
 */
export default {
  // Component name used for debugging and Vue devtools
  name: 'App'
}
</script>

<style src="./assets/styles/app.css"></style>
