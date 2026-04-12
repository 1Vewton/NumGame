/**
 * main.js - Application Entry Point
 * 
 * This is the main entry point for the NumGame Vue.js application.
 * It initializes the Vue application and mounts it to the DOM.
 */

// Import Vue's createApp function for creating Vue applications
import { createApp } from 'vue'

// Import the root App component
import App from './App.vue'

/**
 * Creates and mounts the Vue application
 * 
 * This function initializes the Vue 3 application with the root App component
 * and mounts it to the HTML element with id 'app'.
 * 
 * @function createApp
 * @param {Component} App - The root component of the application
 * @returns {App} The created Vue application instance
 * 
 * @function mount
 * @param {string} selector - CSS selector for the DOM element to mount to
 */
createApp(App).mount('#app')
