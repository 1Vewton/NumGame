/**
 * babel.config.js - Babel Configuration
 * 
 * This file configures Babel for JavaScript transpilation in the NumGame application.
 * It ensures compatibility with target browsers by transforming modern JavaScript
 * syntax to versions supported by the browsers defined in package.json's browserslist.
 */

module.exports = {
  /**
   * Babel presets - Collections of Babel plugins for specific use cases
   * 
   * @property {Array} presets - Array of Babel preset configurations
   *   - '@vue/cli-plugin-babel/preset': Vue CLI's default Babel preset
   */
  presets: [
    '@vue/cli-plugin-babel/preset'
  ]
}
