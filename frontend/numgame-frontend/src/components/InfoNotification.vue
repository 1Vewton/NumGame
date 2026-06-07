<!--
InfoNotification.vue - Reusable Info Notification Toast Component

This component displays a toast notification for informational messages.
It features an info icon (fa-solid fa-circle-info) on the left side
and the info message text on the right side.
The notification auto-dismisses after 1 second and emits a 'close' event.
The styling is consistent with ErrorNotification and SuccessNotification
but with yellow color accents to indicate informational content.
This component is designed to be reusable across all Vue components in the application.

@module InfoNotification
-->
<template>
  <!-- Info notification overlay -->
  <div v-if="visible" class="info-notification-overlay">
    <div class="info-notification">
      <!-- Left side: Info icon -->
      <div class="info-notification-icon">
        <i class="fa-solid fa-circle-info"></i>
      </div>
      <!-- Right side: Info message -->
      <div class="info-notification-message">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
/**
 * InfoNotification Component - Reusable info toast notification
 * 
 * This component displays a toast notification with an info icon and message text.
 * It automatically dismisses after 1 second and emits a 'close' event to notify
 * the parent component. The component uses a fade transition for smooth animations.
 * The styling is self-contained, making it reusable by any Vue component.
 * 
 * @module InfoNotification
 */
export default {
  name: 'InfoNotification',

  /**
   * Component props
   * 
   * @property {boolean} visible - Controls whether the notification is shown
   * @property {string} message - The info message text to display
   */
  props: {
    /**
     * Controls the visibility of the notification toast
     * 
     * When set to true, the notification appears and starts a 1-second auto-dismiss timer.
     * When the timer expires, a 'close' event is emitted.
     * 
     * @property {Boolean} visible
     */
    visible: {
      type: Boolean,
      default: false
    },

    /**
     * The info message text to display in the notification
     * 
     * This text appears on the right side of the notification,
     * next to the info icon on the left.
     * 
     * @property {String} message
     */
    message: {
      type: String,
      default: ''
    }
  },

  /**
   * Emitted events
   * 
   * @event close - Emitted after 1 second auto-dismiss timer expires
   */
  emits: ['close'],

  /**
   * Watch handlers to react to prop changes
   */
  watch: {
    /**
     * Watches the visible prop for changes
     * 
     * When visible becomes true, starts a 1-second timer.
     * After the timer expires, emits a 'close' event to notify
     * the parent component that the notification should be hidden.
     * 
     * @method watch.visible
     * @param {boolean} newVal - The new value of the visible prop
     */
    visible(newVal) {
      if (newVal) {
        // Auto-dismiss after 1 second
        setTimeout(() => {
          this.$emit('close');
        }, 1000);
      }
    }
  }
}
</script>

<style scoped src="../assets/styles/info-notification.css"></style>
