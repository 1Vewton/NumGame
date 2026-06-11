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
import BotGame from '../components/BotGame.vue'
import GameInfo from '../components/GameInfo.vue'
import userStore from '../stores/userStore.js'


/**
 * Route configuration array
 * 
 * Defines all application routes with their associated components.
 * The root path ('/') renders the StartScreen component.
 * The '/startBotGame' path renders the StartBotGame component.
 * The '/botGame' path renders the BotGame component.
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
    component: StartBotGame,
    /**
     * Navigation guard that checks if the user is logged in
     * 
     * If the user is not logged in, redirects to the home page (StartScreen).
     * This prevents unauthorized access to the Bot game setup screen.
     * 
     * @function beforeEnter
     * @param {Object} to - Target route object
     * @param {Object} from - Current route object
     * @param {Function} next - Function to resolve the navigation
     */
    beforeEnter: (to, from, next) => {
      if (!userStore.isUserLoggedIn()) {
        // Redirect to home page if user is not logged in
        next({ name: 'StartScreen' });
      } else {
        // Allow navigation to proceed
        next();
      }
    }
  },

  {
    /**
     * GameInfo route
     * 
     * When accessing http://localhost:8080/gameInfo,
     * this route renders the GameInfo component which displays
     * the player's game history fetched from the backend GamesInfoEndpoint.
     * 
     * @route GET /gameInfo
     * @component GameInfo
     */
    path: '/gameInfo',
    name: 'GameInfo',
    component: GameInfo,
    /**
     * Navigation guard that checks if the user is logged in
     * 
     * If the user is not logged in, redirects to the home page (StartScreen).
     * This prevents unauthorized access to the game history page.
     * 
     * @function beforeEnter
     * @param {Object} to - Target route object
     * @param {Object} from - Current route object
     * @param {Function} next - Function to resolve the navigation
     */
    beforeEnter: (to, from, next) => {
      if (!userStore.isUserLoggedIn()) {
        next({ name: 'StartScreen' });
      } else {
        next();
      }
    }
  },

  {
    /**
     * BotGame route

     * 
     * When accessing http://localhost:8080/botGame,
     * this route renders the BotGame component which wraps the
     * shared GameScreen template and adds Bot mode-specific logic.
     * The GameScreen is a reusable UI shell that can be used
     * by multiple game modes (Bot, PvP, etc.) with different
     * internal logic implementations.
     * 
     * @route GET /botGame
     * @component BotGame
     */
    path: '/botGame',
    name: 'BotGame',
    component: BotGame,
    /**
     * Navigation guard that checks if the user is logged in
     * 
     * If the user is not logged in, redirects to the home page (StartScreen).
     * This prevents unauthorized access to the Bot game screen.
     * 
     * @function beforeEnter
     * @param {Object} to - Target route object
     * @param {Object} from - Current route object
     * @param {Function} next - Function to resolve the navigation
     */
    beforeEnter: (to, from, next) => {
      // Check if user is logged in
      if (!userStore.isUserLoggedIn()) {
        // Redirect to home page if user is not logged in
        next({ name: 'StartScreen' });
        return;
      }

      // Only allow access from StartBotGame (programmatic navigation via "Start" button)
      // Block direct URL access, browser back/forward, and navigation from any other page
      if (from.name !== 'StartBotGame') {
        // Redirect to StartBotGame if the user did not come from the setup screen
        next({ name: 'StartBotGame' });
        return;
      }

      // Allow navigation to proceed
      next();
    }
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
