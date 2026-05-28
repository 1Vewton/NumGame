<!--
AppButton.vue - Reusable Button Component

This component provides a reusable styled button for the NumGame application.
It supports loading state, custom sizing, width control, and various visual variants.
The component uses slots for content customization and emits a 'click' event for
parent component handling. The styling is self-contained for reuse across the app.

@module AppButton
-->
<template>
  <!-- 
    Styled button element
    Disabled when loading or explicitly disabled
  -->
  <button
    class="app-button"
    :class="[
      `app-button--${variant}`,
      `app-button--${size}`,
      {
        'app-button--loading': isLoading,
        'app-button--custom-width': customWidth
      }
    ]"
    :style="buttonStyle"
    :disabled="isLoading || disabled"
    :type="type"
    @click="handleClick"
  >
    <!-- Loading spinner and text -->
    <template v-if="isLoading">
      <span class="app-button__spinner"></span>
      <span class="app-button__text">{{ loadingLabel }}</span>
    </template>
    <!-- Default content (slot or label) -->
    <template v-else>
      <span class="app-button__text">
        <slot>{{ label }}</slot>
      </span>
    </template>
  </button>
</template>

<script>
/**
 * AppButton Component - Reusable styled button
 * 
 * This component renders a styled button with support for loading state,
 * multiple sizes, custom width, and visual variants. It uses a default slot
 * for custom content and emits a 'click' event when the button is pressed.
 * The component is fully reusable across any Vue component in the application.
 * 
 * @module AppButton
 */
export default {
  name: 'AppButton',

  /**
   * Component props
   * 
   * @property {string} label - Button text content (used when no slot content is provided)
   * @property {string} loadingLabel - Text to display when button is in loading state
   * @property {boolean} isLoading - Controls the loading spinner and disabled state
   * @property {boolean} disabled - Controls whether the button is disabled
   * @property {string} size - Button size variant: 'small', 'medium', or 'large'
   * @property {string} variant - Visual style variant: 'primary', 'secondary', or 'success'
   * @property {string} width - Custom CSS width value (e.g., '100%', '200px', 'auto')
   * @property {string} type - HTML button type attribute: 'button' or 'submit'
   */
  props: {
    /**
     * The text content displayed on the button
     * 
     * Used as fallback when no default slot content is provided.
     * 
     * @property {String} label
     */
    label: {
      type: String,
      default: 'Button'
    },

    /**
     * Text displayed when the button is in loading state
     * 
     * Replaces the button text with a spinner and this label
     * when isLoading is true.
     * 
     * @property {String} loadingLabel
     */
    loadingLabel: {
      type: String,
      default: 'Loading...'
    },

    /**
     * Controls the loading state of the button
     * 
     * When true, shows a spinner animation and loading label,
     * and disables the button to prevent multiple submissions.
     * 
     * @property {Boolean} isLoading
     */
    isLoading: {
      type: Boolean,
      default: false
    },

    /**
     * Controls whether the button is disabled
     * 
     * When true, the button cannot be clicked and appears
     * visually dimmed. Also automatically enabled during loading.
     * 
     * @property {Boolean} disabled
     */
    disabled: {
      type: Boolean,
      default: false
    },

    /**
     * The size variant of the button
     * 
     * Controls the padding and font size:
     * - 'small': Compact button for tight spaces
     * - 'medium': Default size for standard use
     * - 'large': Prominent button for primary actions
     * 
     * @property {String} size
     */
    size: {
      type: String,
      default: 'medium',
      validator(value) {
        return ['small', 'medium', 'large'].includes(value);
      }
    },

    /**
     * The visual style variant of the button
     * 
     * Controls the color scheme:
     * - 'primary': Red theme (default, matches NumGame branding)
     * - 'secondary': Gray/neutral theme
     * - 'success': Green theme
     * 
     * @property {String} variant
     */
    variant: {
      type: String,
      default: 'primary',
      validator(value) {
        return ['primary', 'secondary', 'success'].includes(value);
      }
    },

    /**
     * Custom CSS width for the button
     * 
     * Allows overriding the default width behavior.
     * Examples: '100%', '200px', 'auto', '50%'
     * When not provided, the button sizes to its content.
     * 
     * @property {String} width
     */
    width: {
      type: String,
      default: ''
    },

    /**
     * The HTML button type attribute
     * 
     * Determines the behavior when used inside a form:
     * - 'button': Default, does not submit forms
     * - 'submit': Submits the parent form
     * 
     * @property {String} type
     */
    type: {
      type: String,
      default: 'button',
      validator(value) {
        return ['button', 'submit'].includes(value);
      }
    }
  },

  /**
   * Emitted events
   * 
   * @event click - Emitted when the button is clicked (only if not loading/disabled)
   */
  emits: ['click'],

  /**
   * Computed properties
   */
  computed: {
    /**
     * Computes the inline style for custom width
     * 
     * Only applies a width style when the 'width' prop is provided.
     * 
     * @returns {Object} Inline style object with optional width property
     */
    buttonStyle() {
      const style = {};
      if (this.width) {
        style.width = this.width;
      }
      return style;
    },

    /**
     * Determines if the custom width class should be applied
     * 
     * @returns {boolean} True if a custom width is specified
     */
    customWidth() {
      return !!this.width;
    }
  },

  /**
   * Component methods
   */
  methods: {
    /**
     * Handles the button click event
     * 
     * Only emits the 'click' event when the button is not loading
     * and not disabled, preventing accidental multiple submissions.
     * 
     * @method handleClick
     * @param {Event} event - The native click event object
     */
    handleClick(event) {
      if (!this.isLoading && !this.disabled) {
        this.$emit('click', event);
      }
    }
  }
}
</script>

<style scoped src="../assets/styles/app-button.css"></style>
