/**
 * enums.js - Application Enumeration Constants Module
 *
 * This module serves as a centralized repository for all enumeration constants
 * used throughout the NumGame frontend application. By consolidating all enums
 * into a single file, it provides a single source of truth for shared constant
 * values, reducing duplication and ensuring consistency across the codebase.
 * Each enum is implemented as a frozen object to prevent runtime modifications.
 *
 * @module Enums
 * @author System
 * @created May 26, 2026
 * @updated May 26, 2026
 */

/**
 * WebSocket Response Type Enumeration
 *
 * Defines the numeric type identifiers for WebSocket messages received from the
 * backend server. Each value corresponds to a specific kind of server event or
 * operation result, enabling type-safe handling of incoming WebSocket payloads
 * throughout the application.
 *
 * @enum {Object<string, number>}
 * @readonly
 * @property {number} HEARTBEAT - 1: Server heartbeat/ping to maintain connection
 * @property {number} PLAYER_OPERATION - 2: General player operation message
 * @property {number} OPERATION_EXECUTION_RESULT - 3: Result of an operation execution
 * @property {number} MOVE_DIVISION - 4: Division movement event
 * @property {number} DATA_UPDATE - 5: General data update notification
 * @property {number} BOT_TURN_START - 6: Notification that the bot's turn has started
 * @property {number} PLAYER_TURN_START - 7: Notification that the player's turn has started
 * @property {number} TURN_FINISH - 8: Notification that a turn has finished
 * @property {number} BOT_TURN_FINISH - 9: Notification that the bot's turn has finished
 * @property {number} PLAYER_WIN - 10: Notification that the player has won
 * @property {number} BOT_WIN - 11: Notification that the bot has won
 *
 * @example
 * // Access a specific type
 * console.log(WSResponseTypes.HEARTBEAT); // 1
 *
 * @example
 * // Use in a switch statement for message handling
 * function handleMessage(type, data) {
 *   switch (type) {
 *     case WSResponseTypes.PLAYER_TURN_START:
 *       console.log('Player turn started');
 *       break;
 *     case WSResponseTypes.PLAYER_WIN:
 *       console.log('Player wins!');
 *       break;
 *   }
 * }
 */
export const WSResponseTypes = Object.freeze({
  HEARTBEAT: 1,
  PLAYER_OPERATION: 2,
  OPERATION_EXECUTION_RESULT: 3,
  MOVE_DIVISION: 4,
  DATA_UPDATE: 5,
  BOT_TURN_START: 6,
  PLAYER_TURN_START: 7,
  TURN_FINISH: 8,
  BOT_TURN_FINISH: 9,
  PLAYER_WIN: 10,
  BOT_WIN: 11
});

/**
 * Aggregate object containing all application enums for convenient single-import access.
 *
 * This object groups all enumeration constants defined in this module under a single
 * namespace, allowing consumers to import everything at once when multiple enums
 * are needed.
 *
 * @type {Object}
 * @property {Object} WSResponseTypes - WebSocket response type enum constants
 */
const enums = {
  WSResponseTypes
};

export default enums;

// Support CommonJS exports for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { WSResponseTypes };
  module.exports.default = enums;
  module.exports.__esModule = true;
}
