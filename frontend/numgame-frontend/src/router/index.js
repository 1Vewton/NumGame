/**
 * index.js - Vue Router Configuration
 * 
 * This module configures Vue Router for the NumGame frontend application.
 * It defines the routing rules for navigating between different views/pages
 * and maps URL paths to their corresponding Vue components.
 * 
 * @module RouterConfig
 */

import { createRouter, createWebHistory } from 'vue-router'
import StartScreen from '../components/StartScreen.vue'
import StartBotGame from '../components/StartBotGame.vue'

/**
 * Route configuration array
 * 
 * Defines all application routes with their associated components.
 * The root path ('/') renders the StartScreen component.
 * The '/startBotGame' path renders the StartBotGame component.
 * Additional routes can be added here to support more views.
 * 
 * @constant routes
 * @type {Array<Object>}
 */
const routes = [
  {
    /**
     * Root route - StartScreen
     * 
     * When accessing http://localhost:8080/ (no specific endpoint),
     * this route renders the StartScreen component which displays
     * the welcome/login screen.
     * 
     * @route GET /
     * @component StartScreen
     */
    path: '/',
    name: 'StartScreen',
    component: StartScreen
  },
  {
    /**
     * StartBotGame route
     * 
     * When accessing http://localhost:8080/startBotGame,
     * this route renders the StartBotGame component which displays
     * the Bot game setup screen with a target number input field.
     * 
     * @route GET /startBotGame
     * @component StartBotGame
     */
    path: '/startBotGame',
    name: 'StartBotGame',
    component: StartBotGame
  }
]

/**
 * Creates and exports the Vue Router instance
 * 
 * Uses HTML5 history mode (createWebHistory) for clean URLs
 * without hash marks (#). The router manages navigation between
 * different views and provides navigation guards and route
 * parameter handling.
 * 
 * @function createRouter
 * @param {Object} options - Router configuration options
 * @param {string} options.history - History mode for URL management
 * @param {Array} options.routes - Route definitions
 * @returns {Router} Configured Vue Router instance
 */
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
