<!--
AppInput.vue - Reusable White Input Field Component

This component provides a reusable white-themed input field for the NumGame application.
It features a white background with dark text, a placeholder, and a label.
The component supports v-model for two-way data binding, making it easy to integrate
with form data in any parent component. The styling is self-contained for reuse.

@module AppInput
-->
<template>
  <!-- Input field container -->
  <div class="app-input-container">
    <!-- Optional label displayed above the input -->
    <label v-if="label" class="app-input-label" :for="inputId">{{ label }}</label>
    <!-- White input field -->
    <input
      :id="inputId"
      class="app-input"
      :type="type"
      :placeholder="placeholder"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      @keyup.enter="$emit('enter')"
    />
  </div>
</template>

<script>
/**
 * AppInput Component - Reusable white input field
 * 
 * This component renders a styled input field with a white background,
 * designed for the NumGame application's red and black color theme.
 * It supports v-model two-way data binding via Vue 3's modelValue/update:modelValue pattern,
 * and emits an 'enter' event when the Enter key is pressed.
 * The component is fully reusable across any Vue component in the application.
 * 
 * @module AppInput
 */
export default {
  name: 'AppInput',

  /**
   * Component props
   * 
   * @property {string} modelValue - The current input value (for v-model binding)
   * @property {string} type - The HTML input type attribute (default: 'text')
   * @property {string} placeholder - Placeholder text for the input
   * @property {string} label - Optional label text displayed above the input
   * @property {string} inputId - Unique ID for the input element (used for label association)
   */
  props: {
    /**
     * The current value of the input field
     * 
     * This prop enables v-model two-way data binding with the parent component.
     * The parent component passes the initial value and listens for updates
     * via the 'update:modelValue' event.
     * 
     * @property {String|Number} modelValue
     */
    modelValue: {
      type: [String, Number],
      default: ''
    },

    /**
     * The HTML input type attribute
     * 
     * Determines the type of input (e.g., 'text', 'password', 'email').
     * Defaults to 'text' for general text input.
     * 
     * @property {String} type
     */
    type: {
      type: String,
      default: 'text'
    },

    /**
     * Placeholder text displayed inside the input when empty
     * 
     * Provides a hint to the user about what to enter in the field.
     * 
     * @property {String} placeholder
     */
    placeholder: {
      type: String,
      default: ''
    },

    /**
     * Optional label text displayed above the input field
     * 
     * When provided, a label element is rendered above the input for
     * better accessibility and user guidance.
     * 
     * @property {String} label
     */
    label: {
      type: String,
      default: ''
    },

    /**
     * Unique identifier for the input element
     * 
     * Used to associate the label with the input via the 'for' attribute.
     * A default ID is generated if not provided.
     * 
     * @property {String} inputId
     */
    inputId: {
      type: String,
      default: ''
    }
  },

  /**
   * Emitted events
   * 
   * @event update:modelValue - Emitted when the input value changes (for v-model binding)
   * @event enter - Emitted when the Enter key is pressed while the input is focused
   */
  emits: ['update:modelValue', 'enter']
}
</script>

<style scoped src="../assets/styles/app-input.css"></style>
