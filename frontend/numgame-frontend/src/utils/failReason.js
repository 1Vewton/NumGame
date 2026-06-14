/**
 * failReason.js - Fail Reason Utility Module
 *
 * This module provides utility functions for converting FailReason enum constants
 * into human-readable, English strings suitable for display to the user. It serves
 * as a single source of truth for fail reason display text, ensuring consistent
 * messaging across the application when operation failures occur.
 *
 * @module FailReasonUtils
 * @created June 14, 2026
 */

import { FailReason } from '@/utils/enums';

/**
 * Map object that associates each FailReason enum value with its corresponding
 * human-readable display string.
 *
 * @type {Object<number, string>}
 * @readonly
 */
const failReasonMessages = Object.freeze({
  [FailReason.NO_ENOUGH_ACTION_POINT]: 'Insufficient action points',
  [FailReason.NO_SUCH_OPERATION]: 'Operation does not exist',
  [FailReason.NOT_YOUR_TURN]: 'Not your turn'
});

/**
 * Default fallback message returned when an unknown or unrecognized fail reason
 * value is provided.
 *
 * @type {string}
 */
const UNKNOWN_REASON_MESSAGE = 'Unknown error';

/**
 * Converts a FailReason enum value into its corresponding human-readable string.
 *
 * This function looks up the provided FailReason value in the internal map and
 * returns a user-friendly English description. If the value is not a recognized
 * FailReason, a default fallback message is returned.
 *
 * @function getFailReasonMessage
 * @param {number} failReason - The FailReason enum value to convert (e.g., 1, 2, 3)
 * @returns {string} A human-readable description of the fail reason in English
 *
 * @example
 * // Returns 'Insufficient action points'
 * const message = getFailReasonMessage(FailReason.NO_ENOUGH_ACTION_POINT);
 *
 * @example
 * // Returns 'Not your turn'
 * const message = getFailReasonMessage(3);
 *
 * @example
 * // Returns 'Unknown error' for unrecognized values
 * const message = getFailReasonMessage(99);
 */
export function getFailReasonMessage(failReason) {
  return failReasonMessages[failReason] || UNKNOWN_REASON_MESSAGE;
}

export default {
  getFailReasonMessage
};

// Support CommonJS exports for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { getFailReasonMessage };
  module.exports.default = { getFailReasonMessage };
  module.exports.__esModule = true;
}