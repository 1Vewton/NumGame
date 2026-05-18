/**
 * requestBodies.js - API Request Body Templates Module
 *
 * This module provides centralized request body templates for API endpoints.
 * It defines standard request body structures used for user authentication
 * and information retrieval operations, ensuring consistent payload formatting
 * across the application. Each request body is generated through functions,
 * allowing dynamic creation of payloads with actual data at runtime.
 *
 * @module RequestBodies
 * @author System
 * @created May 18, 2026
 * @updated May 18, 2026
 */

/**
 * Generates a request body for user registration
 *
 * This function creates the payload structure required for the user registration
 * endpoint. It contains the player's chosen name and password credentials
 * needed to create a new account.
 *
 * @function getUserRegisterBody
 * @param {string} [playerName='string'] - The username for the new player account
 * @param {string} [playerPassword='stringst'] - The password for the new player account
 * @returns {Object} The request body for user registration
 * @property {string} player_name - The chosen username for the new player account
 * @property {string} player_password - The password credential for the new player account
 * @example
 * // Returns default template body
 * const registerBody = getUserRegisterBody();
 * console.log(registerBody);
 * // { player_name: 'string', player_password: 'stringst' }
 *
 * @example
 * // Returns customized body with actual data
 * const registerBody = getUserRegisterBody('player1', 'securePass123');
 * console.log(registerBody);
 * // { player_name: 'player1', player_password: 'securePass123' }
 */
export function getUserRegisterBody(playerName = 'string', playerPassword = 'stringst') {
  return {
    player_name: playerName,
    player_password: playerPassword
  };
}

/**
 * Generates a request body for user login
 *
 * This function creates the payload structure required for the user login
 * endpoint. It contains the player's credentials (name and password) needed
 * to authenticate and establish a session.
 *
 * @function getUserLoginBody
 * @param {string} [playerName='string'] - The registered username of the player
 * @param {string} [playerPassword='stringst'] - The password credential for authentication
 * @returns {Object} The request body for user login
 * @property {string} player_name - The registered username of the player
 * @property {string} player_password - The password credential for authentication
 * @example
 * // Returns default template body
 * const loginBody = getUserLoginBody();
 * console.log(loginBody);
 * // { player_name: 'string', player_password: 'stringst' }
 *
 * @example
 * // Returns customized body with actual data
 * const loginBody = getUserLoginBody('player1', 'securePass123');
 * console.log(loginBody);
 * // { player_name: 'player1', player_password: 'securePass123' }
 */
export function getUserLoginBody(playerName = 'string', playerPassword = 'stringst') {
  return {
    player_name: playerName,
    player_password: playerPassword
  };
}

/**
 * Generates a request body for user information retrieval
 *
 * This function creates the payload structure required for the user information
 * endpoint. It contains the player's identification details needed to fetch
 * the associated account information.
 *
 * @function getUserInfoBody
 * @param {string} [playerName='string'] - The username of the player to look up
 * @param {string} [playerId='string'] - The unique identifier of the player account
 * @returns {Object} The request body for user information
 * @property {string} player_name - The username of the player to look up
 * @property {string} player_id - The unique identifier of the player account
 * @example
 * // Returns default template body
 * const infoBody = getUserInfoBody();
 * console.log(infoBody);
 * // { player_name: 'string', player_id: 'string' }
 *
 * @example
 * // Returns customized body with actual data
 * const infoBody = getUserInfoBody('player1', 'uuid-12345');
 * console.log(infoBody);
 * // { player_name: 'player1', player_id: 'uuid-12345' }
 */
export function getUserInfoBody(playerName = 'string', playerId = 'string') {
  return {
    player_name: playerName,
    player_id: playerId
  };
}

/**
 * All request body generation functions organized by endpoint name
 *
 * This aggregated object provides a convenient way to access all request body
 * generation functions through a single import. It groups all endpoint payload
 * creators for easier consumption by other modules.
 *
 * @type {Object}
 * @property {Function} getUserRegisterBody - Function to generate user registration request body
 * @property {Function} getUserLoginBody - Function to generate user login request body
 * @property {Function} getUserInfoBody - Function to generate user information request body
 */
const requestBodies = {
  getUserRegisterBody,
  getUserLoginBody,
  getUserInfoBody
};

export default requestBodies;

// Support CommonJS imports for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    getUserRegisterBody,
    getUserLoginBody,
    getUserInfoBody
  };
  module.exports.default = requestBodies;
  module.exports.__esModule = true;
}
