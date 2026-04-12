/**
 * config.js - Environment Configuration Module
 * 
 * This module provides centralized access to environment variables loaded from .env files.
 * It serves as a configuration manager for the NumGame frontend application, allowing
 * other modules to access configuration values in a consistent and type-safe manner.
 * 
 * @module Config
 * @author System
 * @created April 12, 2026
 * @updated April 12, 2026
 */

/**
 * Configuration class for managing environment variables
 * 
 * This class encapsulates access to environment configuration values,
 * providing a clean interface for retrieving backend URLs and other
 * application settings defined in .env files.
 * 
 * @class Config
 */
class Config {
  /**
   * Creates a new Config instance
   * 
   * The constructor initializes configuration values from environment variables.
   * Environment variables prefixed with VUE_APP_ are automatically loaded
   * by Vue CLI during the build process.
   * 
   * @constructor
   */
  constructor() {
    /**
     * Backend API base URL
     * 
     * @type {string}
     * @private
     */
    this._backendUrl = process.env.VUE_APP_BACKEND_URL || 'http://localhost:7111';
  }

  /**
   * Gets the backend API base URL
   * 
   * This method returns the backend server URL for API requests.
   * The value is read from the VUE_APP_BACKEND_URL environment variable.
   * If the environment variable is not set, a default localhost URL is returned.
   * 
   * @method getBackendUrl
   * @returns {string} The backend API base URL
   * @example
   * // Returns 'http://localhost:7111' if VUE_APP_BACKEND_URL is not set
   * const backendUrl = config.getBackendUrl();
   */
  getBackendUrl() {
    return this._backendUrl;
  }

  /**
   * Gets all configuration values as an object
   * 
   * This method returns a plain object containing all configuration values.
   * Useful for debugging or when multiple configuration values are needed at once.
   * 
   * @method getAllConfig
   * @returns {Object} Object containing all configuration values
   * @example
   * // Returns { backendUrl: 'http://localhost:7111' }
   * const allConfig = config.getAllConfig();
   */
  getAllConfig() {
    return {
      backendUrl: this._backendUrl
    };
  }

  /**
   * Validates that required configuration values are present
   * 
   * This method checks if all required configuration values are available.
   * Throws an error if any required configuration is missing.
   * 
   * @method validateConfig
   * @throws {Error} If required configuration values are missing or invalid
   * @returns {boolean} True if all required configuration values are valid
   * @example
   * // Validates configuration and throws error if backend URL is missing
   * config.validateConfig();
   */
  validateConfig() {
    if (!this._backendUrl || this._backendUrl.trim() === '') {
      throw new Error('Backend URL configuration is missing or empty');
    }
    
    // Validate URL format
    try {
      new URL(this._backendUrl);
    } catch (error) {
      throw new Error(`Invalid backend URL format: ${this._backendUrl}`);
    }
    
    return true;
  }
}

/**
 * Singleton instance of the Config class
 * 
 * This exported instance provides a shared configuration object
 * for use throughout the application. Using a singleton ensures
 * consistent configuration access across all modules.
 * 
 * @type {Config}
 */
const config = new Config();

// Export the singleton instance
export default config;

// Support CommonJS imports for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
  // For CommonJS, directly export the config instance
  module.exports = config;
}
