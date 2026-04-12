/**
 * vue.config.js - Vue CLI Configuration
 * 
 * This file contains custom configuration for Vue CLI in the NumGame application.
 * It allows customization of build settings, dev server options, and other
 * project-specific configurations beyond the Vue CLI defaults.
 */

// Import the defineConfig function from Vue CLI service
const { defineConfig } = require('@vue/cli-service')

/**
 * Vue CLI configuration object
 * 
 * @module VueConfig
 * @property {boolean} transpileDependencies - Enable transpilation of dependencies
 *   When set to true, dependencies in node_modules will also be transpiled by Babel.
 *   This ensures compatibility with older browsers for third-party packages.
 */
module.exports = defineConfig({
  transpileDependencies: true
})
