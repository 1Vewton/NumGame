/**
 * main.js - Application Entry Point
 * 
 * This is the main entry point for the NumGame Vue.js application.
 * It initializes the Vue application, registers Vue Router, and
 * mounts the application to the DOM.
 */

// Import Vue's createApp function for creating Vue applications
import { createApp } from 'vue'

// Import the root App component
import App from './App.vue'

// Import the Vue Router for page navigation
import router from './router/index.js'

// Import global reusable styles (shared patterns)
import './assets/styles/scrollbar.css'
import './assets/styles/app.css'
import './assets/styles/page-layout.css'
import './assets/styles/welcome-section.css'
import './assets/styles/modal-pattern.css'
import './assets/styles/animations.css'


/**
 * Creates, configures, and mounts the Vue application
 * 
 * This function initializes the Vue 3 application with the root App component,
 * registers the Vue Router for page navigation, and mounts the application
 * to the HTML element with id 'app'.
 * 
 * @function createApp
 * @param {Component} App - The root component of the application
 * @returns {App} The created Vue application instance
 * 
 * @function use
 * @param {Router} router - The Vue Router instance for navigation
 * @returns {App} The Vue application instance with router registered
 * 
 * @function mount
 * @param {string} selector - CSS selector for the DOM element to mount to
 */
createApp(App).use(router).mount('#app')
