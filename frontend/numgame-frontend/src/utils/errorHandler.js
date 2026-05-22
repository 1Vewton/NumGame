/**
 * errorHandler.js - Unified Error Message Extraction Module
 * 
 * This module provides a reusable function for extracting error messages
 * from API call failures. It standardizes error handling across all
 * components that make backend API requests.
 * 
 * Error resolution order:
 * 1. If response body exists and has a "reason" key, use that value
 * 2. If response body exists but has no "reason" key, use the entire body
 * 3. If no response body exists, use the request error message
 * 
 * @module errorHandler
 */

/**
 * Extracts a human-readable error message from an API call error object
 * 
 * This function examines the error object to extract the most meaningful
 * error message, following the standardized backend error response format.
 * It handles three scenarios:
 * - Error has response data with a "reason" key (preferred)
 * - Error has response data without a "reason" key (uses the data itself)
 * - Error has no response data (uses the error message)
 * 
 * @function extractErrorMessage
 * @param {Error} error - The error object from an API call
 * @param {string} [fallbackMessage='Request failed'] - Default message if nothing else can be extracted
 * @returns {string} A human-readable error message string
 * @example
 * // Error with response data containing reason
 * const error1 = { responseData: { reason: 'Username does not exist' } };
 * extractErrorMessage(error1, 'Login failed');
 * // Returns: 'Username does not exist'
 * 
 * @example
 * // Error with response data but no reason key
 * const error2 = { responseData: 'Server error' };
 * extractErrorMessage(error2, 'Login failed');
 * // Returns: 'Server error'
 * 
 * @example
 * // Error with object response data but no reason key
 * const error3 = { responseData: { message: 'Server error' } };
 * extractErrorMessage(error3, 'Login failed');
 * // Returns: '{"message":"Server error"}'
 * 
 * @example
 * // Error with no response data
 * const error4 = { message: 'Network Error' };
 * extractErrorMessage(error4, 'Login failed');
 * // Returns: 'Network Error'
 * 
 * @example
 * // Error with null/undefined responseData
 * const error5 = { responseData: null };
 * extractErrorMessage(error5, 'Login failed');
 * // Returns: 'Login failed'
 */
export function extractErrorMessage(error, fallbackMessage = 'Request failed') {
  // Check if the error has response data from the server
  if (error.responseData !== null && error.responseData !== undefined) {
    const responseData = error.responseData;

    // Case 1: Response data is a non-null object
    if (typeof responseData === 'object' && responseData !== null) {
      // Prefer the "reason" key if it exists
      if (responseData.reason && typeof responseData.reason === 'string') {
        return responseData.reason;
      }
      // Fallback: stringify the entire response data object
      try {
        const stringified = JSON.stringify(responseData);
        // Avoid returning empty object "{}" as the message
        if (stringified && stringified !== '{}') {
          return stringified;
        }
      } catch (e) {
        // If JSON.stringify fails, fall through to the return below
      }
    }

    // Case 2: Response data is a string - use it directly
    if (typeof responseData === 'string' && responseData.trim()) {
      return responseData.trim();
    }
  }

  // Case 3: No response data available - use the error's own message
  if (error.message && typeof error.message === 'string' && error.message.trim()) {
    return error.message.trim();
  }

  // Final fallback: return the provided fallback message
  return fallbackMessage;
}

export default extractErrorMessage;
