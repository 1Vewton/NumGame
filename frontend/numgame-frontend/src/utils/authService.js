/**
 * authService.js - Authentication Service Module
 *
 * This module provides functions for user authentication operations including
 * login, registration, and auto-login. It encapsulates all API communication
 * logic for authentication endpoints and returns normalized response objects.
 *
 * @module AuthService
 * @author System
 * @created July 10, 2026
 */

import apiClient from './api.js';
import config from './config.js';
import {
  getUserLoginBody,
  getUserRegisterBody,
  getUserLoginResponse,
  getUserRegisterResponse,
  getAutoLoginResponse
} from './requestBodies.js';

/**
 * Authenticates a user with their credentials
 *
 * This function sends a POST request to the login endpoint with the user's
 * username and password. On success, it returns a normalized response with
 * the user's ID and name. On failure, it returns a normalized response with
 * the error reason.
 *
 * @async
 * @function login
 * @param {string} playerName - The username of the player
 * @param {string} playerPassword - The password credential for authentication
 * @returns {Promise<Object>} The normalized login response
 * @property {boolean} success - Whether login was successful
 * @property {string} user_id - The unique identifier of the user (empty on failure)
 * @property {string} user_name - The display name of the user (empty on failure)
 * @property {string} reason - Error reason if login failed (empty on success)
 * @throws {Error} If the API request fails
 * @example
 * const response = await login('player1', 'securePass123');
 * if (response.success) {
 *   console.log(response.user_id, response.user_name);
 * }
 */
export async function login(playerName, playerPassword) {
  const endpoint = config.getLoginEndpoint();
  const requestBody = getUserLoginBody(playerName, playerPassword);
  const response = await apiClient.post(endpoint, requestBody);

  if (response.success) {
    return getUserLoginResponse(true, response.user_id, response.user_name, '');
  }

  return getUserLoginResponse(false, '', '', response.reason || 'Login failed');
}

/**
 * Registers a new user account
 *
 * This function sends a POST request to the registration endpoint with the
 * chosen username and password. On success, it returns a normalized success
 * response. On failure, it returns a normalized response with the error reason.
 *
 * @async
 * @function register
 * @param {string} playerName - The username for the new account
 * @param {string} playerPassword - The password for the new account
 * @returns {Promise<Object>} The normalized registration response
 * @property {boolean} success - Whether registration was successful
 * @property {string} reason - Error reason if registration failed (empty on success)
 * @throws {Error} If the API request fails
 * @example
 * const response = await register('player1', 'securePass123');
 * if (response.success) {
 *   console.log('Registration successful');
 * }
 */
export async function register(playerName, playerPassword) {
  const endpoint = config.getRegisterEndpoint();
  const requestBody = getUserRegisterBody(playerName, playerPassword);
  const response = await apiClient.post(endpoint, requestBody);

  if (response.success) {
    return getUserRegisterResponse(true, '');
  }

  return getUserRegisterResponse(false, response.reason || 'Registration failed');
}

/**
 * Attempts an automatic login using existing session cookies
 *
 * This function sends a GET request to the auto-login endpoint. On success,
 * it returns a normalized response with the user's ID and name. On failure,
 * it returns a normalized failure response. No user-facing notifications
 * should be shown regardless of the result.
 *
 * @async
 * @function autoLogin
 * @returns {Promise<Object>} The normalized auto-login response
 * @property {boolean} success - Whether auto-login was successful
 * @property {string} user_id - The unique identifier of the user (empty on failure)
 * @property {string} user_name - The display name of the user (empty on failure)
 * @example
 * const response = await autoLogin();
 * if (response.success) {
 *   userStore.setUser(response.user_id, response.user_name);
 * }
 */
export async function autoLogin() {
  try {
    const endpoint = config.getAutoLoginEndpoint();
    const response = await apiClient.get(endpoint);

    if (response.success) {
      return getAutoLoginResponse(true, response.user_id, response.user_name);
    }

    return getAutoLoginResponse(false, '', '');
  } catch (error) {
    // Auto-login request failed silently - return failure
    return getAutoLoginResponse(false, '', '');
  }
}

export default {
  login,
  register,
  autoLogin
};