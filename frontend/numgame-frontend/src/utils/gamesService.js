/**
 * gamesService.js - Games Information Service Module
 *
 * This module provides functions for fetching and processing game history data
 * from the backend GamesInfoEndpoint. It handles request construction, response
 * parsing, and data normalization for the games listing feature.
 *
 * @module GamesService
 * @author System
 * @created June 11, 2026
 * @updated June 11, 2026
 */

import apiClient from './api.js';
import config from './config.js';
import { getGamesInfoBody, getGenerateUserNameResponse } from './requestBodies.js';

/**
 * Generates a random username via the backend API
 *
 * This function sends a GET request to the user name generation endpoint.
 * On success, it returns a normalized response with the generated username.
 * On failure, it returns a normalized failure response.
 *
 * @async
 * @function generateUserName
 * @returns {Promise<Object>} The normalized API response object
 * @property {boolean} success - Whether the request was successful
 * @property {string} username - The generated username (e.g., "Rilan Aide"), empty string on failure
 * @throws {Error} If the API request fails
 * @example
 * const response = await generateUserName();
 * console.log(response); // { success: true, username: 'Rilan Aide' }
 */
export async function generateUserName() {
  const endpoint = config.getUserNameGenerationEndpoint();
  const response = await apiClient.get(endpoint);

  if (response.success && response.username) {
    return getGenerateUserNameResponse(true, response.username);
  }

  return getGenerateUserNameResponse(false, '');
}

/**
 * Fetches all games associated with a player from the backend
 *
 * This function sends a POST request to the games information endpoint with
 * the player's credentials (name and ID) and returns the parsed response
 * containing the list of all games, appeared users mapping, and success status.
 *
 * @async
 * @function fetchGamesInfo
 * @param {string} playerName - The username of the player
 * @param {string} playerId - The unique identifier of the player account
 * @returns {Promise<Object>} The API response object
 * @property {boolean} success - Whether the request was successful
 * @property {Array<Object>} data - Array of game objects
 * @property {Object} appeared_users - Mapping of user IDs to display names
 * @throws {Error} If the API request fails or validation checks fail
 * @example
 * // Fetch games for a specific player
 * const response = await fetchGamesInfo('114514', '0581c1ea-db4d-44a1-89eb-816ab1e75fe9');
 * console.log(response.success); // true
 * console.log(response.data);    // Array of game records
 * console.log(response.appeared_users); // { 'uuid': 'playerName', ... }
 */
export async function fetchGamesInfo(playerName, playerId) {
  // Build the request body using the template function
  const requestBody = getGamesInfoBody(playerName, playerId);

  // Send POST request to the games info endpoint
  const response = await apiClient.post(
    config.getGamesInfoEndpoint(),
    requestBody
  );

  return response;
}

/**
 * Parses and normalizes a single game record from the API response
 *
 * This function transforms a raw game record from the backend into a
 * normalized JavaScript object with consistent property names and types.
 * Timestamps are converted from Unix timestamps (seconds since epoch)
 * to JavaScript Date objects for easier use in the frontend.
 *
 * @function parseGameRecord
 * @param {Object} rawGame - The raw game record from the API response
 * @param {string} rawGame.id - The unique game identifier (e.g., "game:uuid")
 * @param {string} rawGame.first_move - The user ID of the player who moved first
 * @param {string} rawGame.second_move - The user ID of the player who moved second
 * @param {string} rawGame.winner - The user ID of the winner
 * @param {number} rawGame.rounds - The number of rounds played
 * @param {number} rawGame.started_time - Unix timestamp (seconds) when the game started
 * @param {number} rawGame.ended_time - Unix timestamp (seconds) when the game ended
 * @param {number|null} rawGame.first_move_score - Score of the first-moving player (null if not available)
 * @param {number|null} rawGame.second_move_score - Score of the second-moving player (null if not available)
 * @returns {Object} The normalized game record
 * @property {string} id - The unique game identifier
 * @property {string} firstMove - User ID of the first-moving player
 * @property {string} secondMove - User ID of the second-moving player
 * @property {string} winner - User ID of the winner
 * @property {number} rounds - Number of rounds played
 * @property {Date} startedTime - JavaScript Date object for game start time
 * @property {Date} endedTime - JavaScript Date object for game end time
 * @property {number|null} firstMoveScore - Score of the first-moving player
 * @property {number|null} secondMoveScore - Score of the second-moving player
 * @example
 * const raw = {
 *   id: 'game:abc123',
 *   first_move: 'uuid-1',
 *   second_move: 'uuid-2',
 *   winner: 'uuid-1',
 *   rounds: 10,
 *   started_time: 1780836863.413575,
 *   ended_time: 1780836945.810039,
 *   first_move_score: null,
 *   second_move_score: null
 * };
 * const parsed = parseGameRecord(raw);
 * console.log(parsed.startedTime instanceof Date); // true
 */
export function parseGameRecord(rawGame) {
  return {
    id: rawGame.id,
    firstMove: rawGame.first_move,
    secondMove: rawGame.second_move,
    winner: rawGame.winner,
    rounds: rawGame.rounds,
    startedTime: new Date(rawGame.started_time * 1000),
    endedTime: new Date(rawGame.ended_time * 1000),
    firstMoveScore: rawGame.first_move_score,
    secondMoveScore: rawGame.second_move_score
  };
}

/**
 * Determines the result of a game for a specific player
 *
 * This function checks whether the specified player won, lost, or played
 * against a bot based on the game record and the appeared users mapping.
 *
 * @function getGameResultForPlayer
 * @param {Object} game - A parsed game record (from parseGameRecord)
 * @param {string} playerId - The user ID of the player to check
 * @returns {string} The result: 'win', 'lose', or 'unknown'
 * @example
 * const result = getGameResultForPlayer(parsedGame, '0581c1ea-...');
 * // Returns 'win' if the player is the winner
 */
export function getGameResultForPlayer(game, playerId) {

  if (game.winner === playerId) {
    return 'win';
  } else if (game.winner && game.winner !== playerId) {
    return 'lose';
  }
  return 'unknown';
}

/**
 * Determines the opponent's display name for a game
 *
 * This function finds the opponent's user ID (the player who is NOT the
 * specified player) and looks up their display name in the appeared users map.
 *
 * @function getOpponentName
 * @param {Object} game - A parsed game record (from parseGameRecord)
 * @param {string} playerId - The user ID of the current player
 * @param {Object} appearedUsers - Mapping of user IDs to display names (from API response)
 * @returns {string} The display name of the opponent, or 'Unknown' if not found
 * @example
 * const opponent = getOpponentName(parsedGame, '0581c1ea-...', appearedUsers);
 * // Returns '<bot>' or the opponent's username
 */
export function getOpponentName(game, playerId, appearedUsers) {
  const opponentId = game.firstMove === playerId ? game.secondMove : game.firstMove;
  return appearedUsers[opponentId] || 'Unknown';
}

export default {
  generateUserName,
  fetchGamesInfo,
  parseGameRecord,
  getGameResultForPlayer,
  getOpponentName
};
