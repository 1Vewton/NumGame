/**
 * api.js - API Client Module (Axios-based)
 * 
 * This module provides a generic API client for making HTTP requests to the backend server.
 * It handles request/response formatting, error handling, and authentication integration.
 * The module uses the centralized configuration to determine the backend URL.
 * Uses axios as the HTTP client library for better features and error handling.
 * 
 * @module APIClient
 * @author System
 * @created April 14, 2026
 * @updated April 14, 2026
 */

import config from './config.js';
import axios from 'axios';

/**
 * API Client class for making HTTP requests to the backend
 * 
 * This class provides methods to interact with the backend API endpoints.
 * It handles request construction, error management, and response parsing.
 * Uses axios for HTTP requests which provides better error handling,
 * request/response interceptors, and automatic JSON parsing.
 * 
 * @class APIClient
 */
class APIClient {
  /**
   * Creates a new APIClient instance
   * 
   * The constructor initializes the base URL from configuration and sets up
   * default headers for JSON communication. Creates an axios instance with
   * default configuration for making API requests.
   * 
   * @constructor
   */
  constructor() {
    /**
     * Base URL for backend API requests
     * 
     * @type {string}
     * @private
     */
    this._baseUrl = config.getBackendUrl();
    
    /**
     * Default headers for API requests
     * 
     * @type {Object}
     * @private
     */
    this._defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };
    
    /**
     * Axios instance configured for API requests
     * 
     * @type {axios.AxiosInstance}
     * @private
     */
    this._axiosInstance = axios.create({
      baseURL: this._baseUrl,
      headers: this._defaultHeaders,
      timeout: 10000 // 10 seconds timeout
    });
  }

  /**
   * Sends a POST request to the backend API
   * 
   * This method sends a JSON request body to a specified endpoint and returns
   * the parsed JSON response. It handles HTTP errors and network failures.
   * 
   * @method post
   * @param {string} endpoint - The API endpoint path (relative to base URL)
   * @param {Object} body - The request body to send as JSON
   * @param {Object} [headers={}] - Additional headers to include with the request
   * @returns {Promise<Object>} Parsed JSON response from the server
   * @throws {Error} If the request fails or returns a non-2xx status code
   * @example
   * // Send a POST request to /api/game endpoint
   * const response = await apiClient.post('/api/game', { 
   *   action: 'start',
   *   difficulty: 'medium' 
   * });
   * console.log(response); // { success: true, gameId: 'abc123' }
   */
  async post(endpoint, body, headers = {}) {
    try {
      const response = await this._axiosInstance.post(endpoint, body, {
        headers: { ...headers }
      });
      return response.data;
    } catch (error) {
      this._handleAxiosError(error, endpoint, 'POST');
    }
  }

  /**
   * Sends a GET request to the backend API
   * 
   * This method retrieves data from a specified endpoint and returns
   * the parsed JSON response. It handles HTTP errors and network failures.
   * 
   * @method get
   * @param {string} endpoint - The API endpoint path (relative to base URL)
   * @param {Object} [headers={}] - Additional headers to include with the request
   * @returns {Promise<Object>} Parsed JSON response from the server
   * @throws {Error} If the request fails or returns a non-2xx status code
   * @example
   * // Send a GET request to /api/status endpoint
   * const status = await apiClient.get('/api/status');
   * console.log(status); // { status: 'online', players: 42 }
   */
  async get(endpoint, headers = {}) {
    try {
      const response = await this._axiosInstance.get(endpoint, {
        headers: { ...headers }
      });
      return response.data;
    } catch (error) {
      this._handleAxiosError(error, endpoint, 'GET');
    }
  }

  /**
   * Sends a PUT request to the backend API
   * 
   * This method sends a JSON request body to update a resource at the
   * specified endpoint and returns the parsed JSON response.
   * 
   * @method put
   * @param {string} endpoint - The API endpoint path (relative to base URL)
   * @param {Object} body - The request body to send as JSON
   * @param {Object} [headers={}] - Additional headers to include with the request
   * @returns {Promise<Object>} Parsed JSON response from the server
   * @throws {Error} If the request fails or returns a non-2xx status code
   * @example
   * // Send a PUT request to /api/game/abc123 endpoint
   * const response = await apiClient.put('/api/game/abc123', { 
   *   score: 1000,
   *   completed: true 
   * });
   * console.log(response); // { success: true, updated: true }
   */
  async put(endpoint, body, headers = {}) {
    try {
      const response = await this._axiosInstance.put(endpoint, body, {
        headers: { ...headers }
      });
      return response.data;
    } catch (error) {
      this._handleAxiosError(error, endpoint, 'PUT');
    }
  }

  /**
   * Sends a DELETE request to the backend API
   * 
   * This method sends a request to delete a resource at the specified
   * endpoint and returns the parsed JSON response.
   * 
   * @method delete
   * @param {string} endpoint - The API endpoint path (relative to base URL)
   * @param {Object} [body=null] - Optional request body to send as JSON
   * @param {Object} [headers={}] - Additional headers to include with the request
   * @returns {Promise<Object>} Parsed JSON response from the server
   * @throws {Error} If the request fails or returns a non-2xx status code
   * @example
   * // Send a DELETE request to /api/game/abc123 endpoint
   * const response = await apiClient.delete('/api/game/abc123');
   * console.log(response); // { success: true, deleted: true }
   */
  async delete(endpoint, body = null, headers = {}) {
    try {
      const config = {
        headers: { ...headers }
      };
      
      // For DELETE requests with body, axios requires data parameter
      if (body !== null && body !== undefined) {
        config.data = body;
      }
      
      const response = await this._axiosInstance.delete(endpoint, config);
      return response.data;
    } catch (error) {
      this._handleAxiosError(error, endpoint, 'DELETE');
    }
  }

  /**
   * Handles axios errors
   * 
   * This internal method standardizes error handling for failed requests,
   * providing detailed error messages for debugging. It extracts useful
   * information from axios error objects.
   * 
   * @method _handleAxiosError
   * @param {Error} error - The caught axios error
   * @param {string} endpoint - The endpoint that was requested
   * @param {string} method - The HTTP method used
   * @throws {Error} Re-throws error with additional context
   * @private
   */
  _handleAxiosError(error, endpoint, method) {
    let errorMessage = `API request failed: ${method} ${endpoint}`;
    const fullUrl = this._baseUrl + (endpoint.startsWith('/') ? endpoint : '/' + endpoint);
    
    // Extract error details from axios response
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      const status = error.response.status;
      const statusText = error.response.statusText || '';
      let responseData = '';
      
      try {
        if (error.response.data) {
          if (typeof error.response.data === 'object') {
            responseData = JSON.stringify(error.response.data);
          } else {
            responseData = error.response.data.toString();
          }
        }
      } catch (e) {
        responseData = 'Unable to parse response data';
      }
      
      errorMessage = `HTTP ${status} ${statusText}: ${method} ${fullUrl}`;
      if (responseData) {
        errorMessage += ` - ${responseData}`;
      }
    } else if (error.request) {
      // The request was made but no response was received
      errorMessage += ` (${fullUrl}) - No response received from server`;
    } else {
      // Something happened in setting up the request that triggered an Error
      errorMessage += ` (${fullUrl}) - ${error.message}`;
    }
    
    // Create a new error with the enhanced message
    const enhancedError = new Error(errorMessage);
    
    // Preserve the original error stack
    enhancedError.stack = error.stack;
    enhancedError.originalError = error;
    
    // Add additional context
    enhancedError.url = fullUrl;
    enhancedError.endpoint = endpoint;
    enhancedError.method = method;
    if (error.response) {
      enhancedError.status = error.response.status;
      enhancedError.statusText = error.response.statusText;
      enhancedError.responseData = error.response.data;
    }
    
    throw enhancedError;
  }
}

/**
 * Singleton instance of the APIClient class
 * 
 * This exported instance provides a shared API client object
 * for use throughout the application. Using a singleton ensures
 * consistent API access and configuration across all modules.
 * 
 * @type {APIClient}
 */
const apiClient = new APIClient();

// Export the singleton instance
export default apiClient;

// Support CommonJS imports for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
  // For CommonJS, directly export the apiClient instance
  module.exports = apiClient;
}