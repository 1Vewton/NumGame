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
    
    /**
     * User registration endpoint path
     * 
     * @type {string}
     * @private
     */
    this._registerEndpoint = process.env.VUE_APP_REGISTER_ENDPOINT || '/api/user/userRegister';
    
    /**
     * User login endpoint path
     * 
     * @type {string}
     * @private
     */
    this._loginEndpoint = process.env.VUE_APP_LOGIN_ENDPOINT || '/api/user/userLogin';
    
    /**
     * User auto-login endpoint path
     * 
     * @type {string}
     * @private
     */
    this._autoLoginEndpoint = process.env.VUE_APP_LOGOUT_ENDPOINT || '/api/user/autoLogin';
    
    /**
     * User information endpoint path
     * 
     * @type {string}
     * @private
     */
    this._userEndpoint = process.env.VUE_APP_USER_ENDPOINT || '/api/user/userInfo';
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
   * Gets the user registration endpoint path
   * 
   * This method returns the endpoint path for user registration API.
   * The value is read from the VUE_APP_REGISTER_ENDPOINT environment variable.
   * If the environment variable is not set, a default endpoint path is returned.
   * 
   * @method getRegisterEndpoint
   * @returns {string} The user registration endpoint path
   * @example
   * // Returns '/api/user/userRegister' if VUE_APP_REGISTER_ENDPOINT is not set
   * const registerEndpoint = config.getRegisterEndpoint();
   */
  getRegisterEndpoint() {
    return this._registerEndpoint;
  }

  /**
   * Gets the user login endpoint path
   * 
   * This method returns the endpoint path for user login API.
   * The value is read from the VUE_APP_LOGIN_ENDPOINT environment variable.
   * If the environment variable is not set, a default endpoint path is returned.
   * 
   * @method getLoginEndpoint
   * @returns {string} The user login endpoint path
   * @example
   * // Returns '/api/user/userLogin' if VUE_APP_LOGIN_ENDPOINT is not set
   * const loginEndpoint = config.getLoginEndpoint();
   */
  getLoginEndpoint() {
    return this._loginEndpoint;
  }

  /**
   * Gets the user auto-login endpoint path
   * 
   * This method returns the endpoint path for user auto-login API.
   * The value is read from the VUE_APP_LOGOUT_ENDPOINT environment variable.
   * Note: Despite the environment variable name, this is used for auto-login functionality.
   * If the environment variable is not set, a default endpoint path is returned.
   * 
   * @method getAutoLoginEndpoint
   * @returns {string} The user auto-login endpoint path
   * @example
   * // Returns '/api/user/autoLogin' if VUE_APP_LOGOUT_ENDPOINT is not set
   * const autoLoginEndpoint = config.getAutoLoginEndpoint();
   */
  getAutoLoginEndpoint() {
    return this._autoLoginEndpoint;
  }

  /**
   * Gets the user information endpoint path
   * 
   * This method returns the endpoint path for user information API.
   * The value is read from the VUE_APP_USER_ENDPOINT environment variable.
   * If the environment variable is not set, a default endpoint path is returned.
   * 
   * @method getUserEndpoint
   * @returns {string} The user information endpoint path
   * @example
   * // Returns '/api/user/userInfo' if VUE_APP_USER_ENDPOINT is not set
   * const userEndpoint = config.getUserEndpoint();
   */
  getUserEndpoint() {
    return this._userEndpoint;
  }

  /**
   * Gets the complete URL for user registration endpoint
   * 
   * This method combines the backend base URL with the registration endpoint path
   * to return a complete URL that can be used for API requests.
   * 
   * @method getRegisterUrl
   * @returns {string} Complete URL for user registration
   * @example
   * // Returns 'http://localhost:7111/api/user/userRegister'
   * const registerUrl = config.getRegisterUrl();
   */
  getRegisterUrl() {
    return `${this._backendUrl}${this._registerEndpoint}`;
  }

  /**
   * Gets the complete URL for user login endpoint
   * 
   * This method combines the backend base URL with the login endpoint path
   * to return a complete URL that can be used for API requests.
   * 
   * @method getLoginUrl
   * @returns {string} Complete URL for user login
   * @example
   * // Returns 'http://localhost:7111/api/user/userLogin'
   * const loginUrl = config.getLoginUrl();
   */
  getLoginUrl() {
    return `${this._backendUrl}${this._loginEndpoint}`;
  }

  /**
   * Gets the complete URL for user auto-login endpoint
   * 
   * This method combines the backend base URL with the auto-login endpoint path
   * to return a complete URL that can be used for API requests.
   * 
   * @method getAutoLoginUrl
   * @returns {string} Complete URL for user auto-login
   * @example
   * // Returns 'http://localhost:7111/api/user/autoLogin'
   * const autoLoginUrl = config.getAutoLoginUrl();
   */
  getAutoLoginUrl() {
    return `${this._backendUrl}${this._autoLoginEndpoint}`;
  }

  /**
   * Gets the complete URL for user information endpoint
   * 
   * This method combines the backend base URL with the user information endpoint path
   * to return a complete URL that can be used for API requests.
   * 
   * @method getUserUrl
   * @returns {string} Complete URL for user information
   * @example
   * // Returns 'http://localhost:7111/api/user/userInfo'
   * const userUrl = config.getUserUrl();
   */
  getUserUrl() {
    return `${this._backendUrl}${this._userEndpoint}`;
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
   * // Returns {
   * //   backendUrl: 'http://localhost:7111',
   * //   registerEndpoint: '/api/user/userRegister',
   * //   loginEndpoint: '/api/user/userLogin',
   * //   autoLoginEndpoint: '/api/user/autoLogin',
   * //   userEndpoint: '/api/user/userInfo',
   * //   registerUrl: 'http://localhost:7111/api/user/userRegister',
   * //   loginUrl: 'http://localhost:7111/api/user/userLogin',
   * //   autoLoginUrl: 'http://localhost:7111/api/user/autoLogin',
   * //   userUrl: 'http://localhost:7111/api/user/userInfo'
   * // }
   * const allConfig = config.getAllConfig();
   */
  getAllConfig() {
    return {
      backendUrl: this._backendUrl,
      registerEndpoint: this._registerEndpoint,
      loginEndpoint: this._loginEndpoint,
      autoLoginEndpoint: this._autoLoginEndpoint,
      userEndpoint: this._userEndpoint,
      registerUrl: `${this._backendUrl}${this._registerEndpoint}`,
      loginUrl: `${this._backendUrl}${this._loginEndpoint}`,
      autoLoginUrl: `${this._backendUrl}${this._autoLoginEndpoint}`,
      userUrl: `${this._backendUrl}${this._userEndpoint}`
    };
  }

  /**
   * Validates that required configuration values are present
   * 
   * This method checks if all required configuration values are available.
   * Throws an error if any required configuration is missing or invalid.
   * Validates both backend URL format and all endpoint paths.
   * 
   * @method validateConfig
   * @throws {Error} If required configuration values are missing or invalid
   * @returns {boolean} True if all required configuration values are valid
   * @example
   * // Validates configuration and throws error if any configuration is missing or invalid
   * config.validateConfig();
   */
  validateConfig() {
    // Validate backend URL
    if (!this._backendUrl || this._backendUrl.trim() === '') {
      throw new Error('Backend URL configuration is missing or empty');
    }
    
    // Validate URL format
    try {
      new URL(this._backendUrl);
    } catch (error) {
      throw new Error(`Invalid backend URL format: ${this._backendUrl}`);
    }
    
    // Validate all endpoint paths
    const endpoints = [
      { name: 'register', value: this._registerEndpoint },
      { name: 'login', value: this._loginEndpoint },
      { name: 'auto-login', value: this._autoLoginEndpoint },
      { name: 'user', value: this._userEndpoint }
    ];
    
    for (const endpoint of endpoints) {
      if (!endpoint.value || endpoint.value.trim() === '') {
        throw new Error(`${endpoint.name} endpoint configuration is missing or empty`);
      }
      
      // Validate endpoint path format (should start with /)
      if (!endpoint.value.startsWith('/')) {
        throw new Error(`${endpoint.name} endpoint must start with '/': ${endpoint.value}`);
      }
      
      // Validate endpoint doesn't contain protocol or host
      if (endpoint.value.includes('://')) {
        throw new Error(`${endpoint.name} endpoint should be a path, not a full URL: ${endpoint.value}`);
      }
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
  // Manual export of all public methods for CommonJS compatibility
  const configInstance = config;
  
  // Export all public methods
  module.exports.getBackendUrl = configInstance.getBackendUrl.bind(configInstance);
  module.exports.getRegisterEndpoint = configInstance.getRegisterEndpoint.bind(configInstance);
  module.exports.getLoginEndpoint = configInstance.getLoginEndpoint.bind(configInstance);
  module.exports.getAutoLoginEndpoint = configInstance.getAutoLoginEndpoint.bind(configInstance);
  module.exports.getUserEndpoint = configInstance.getUserEndpoint.bind(configInstance);
  module.exports.getRegisterUrl = configInstance.getRegisterUrl.bind(configInstance);
  module.exports.getLoginUrl = configInstance.getLoginUrl.bind(configInstance);
  module.exports.getAutoLoginUrl = configInstance.getAutoLoginUrl.bind(configInstance);
  module.exports.getUserUrl = configInstance.getUserUrl.bind(configInstance);
  module.exports.getAllConfig = configInstance.getAllConfig.bind(configInstance);
  module.exports.validateConfig = configInstance.validateConfig.bind(configInstance);
  
  // Export the full instance as default for ES module compatibility
  module.exports.default = configInstance;
  module.exports.__esModule = true;
}
