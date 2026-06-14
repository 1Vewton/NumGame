/**
 * userStore.js - User Session Store Module
 * 
 * This module provides a reactive in-memory store for the current user's session data.
 * It stores user information (user_id and user_name) in memory during the browser session.
 * The data is not persisted (no localStorage/cookies) and will be lost when the page is closed.
 * Other components can import this module to access or modify the current user state.
 * 
 * @module userStore
 */
import { reactive } from 'vue';

/**
 * Reactive user state object
 * 
 * Holds the current user's session information in memory.
 * Initially empty until login successfully sets the user data.
 * 
 * @type {Object}
 * @property {string|null} userId - The unique identifier of the logged-in user
 * @property {string|null} userName - The display name of the logged-in user
 * @property {boolean} isLoggedIn - Flag indicating whether a user is currently logged in
 */
const state = reactive({
  userId: null,
  userName: null,
  isLoggedIn: false
});

/**
 * User Store API
 * 
 * Provides methods to access, set, and clear user session data.
 * All state changes are reactive and will trigger Vue component updates.
 */
export default {
  /**
   * Gets the reactive state object
   * 
   * Provides access to the raw reactive state for direct property binding in components.
   * 
   * @returns {Object} The reactive state object containing userId, userName, and isLoggedIn
   */
  getState() {
    return state;
  },

  /**
   * Gets the current user's unique identifier
   * 
   * @returns {string|null} The user ID if logged in, or null if not authenticated
   */
  getUserId() {
    return state.userId;
  },

  /**
   * Gets the current user's display name
   * 
   * @returns {string|null} The user name if logged in, or null if not authenticated
   */
  getUserName() {
    return state.userName;
  },

  /**
   * Checks if a user is currently logged in
   * 
   * @returns {boolean} True if a user is logged in, false otherwise
   */
  isUserLoggedIn() {
    return state.isLoggedIn;
  },

  /**
   * Sets the current user's session data after successful login
   * 
   * Updates the reactive state with the user's ID and name,
   * and sets the logged-in flag to true. This data is stored
   * in memory only and will be lost on page refresh.
   * 
   * @function setUser
   * @param {string} userId - The unique identifier of the user
   * @param {string} userName - The display name of the user
   */
  setUser(userId, userName) {
    state.userId = userId;
    state.userName = userName;
    state.isLoggedIn = true;
  },

  /**
   * Clears the current user's session data on logout
   * 
   * Resets all state properties to their initial values.
   * Should be called when the user logs out or when their
   * session expires.
   * 
   * @function clearUser
   */
  clearUser() {
    state.userId = null;
    state.userName = null;
    state.isLoggedIn = false;
  },

  /**
   * Clears all stored user data in the store
   * 
   * This method resets every property in the reactive state back to its initial value.
   * It is more comprehensive than clearUser() as it ensures all fields (current and future)
   * are reset, making it suitable for complete session cleanup or hard logout scenarios.
   * 
   * @function clearAll
   */
  clearAll() {
    state.userId = null;
    state.userName = null;
    state.isLoggedIn = false;
  }
};
