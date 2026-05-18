<!--
ErrorNotification.vue - Reusable Error Notification Toast Component

This component displays a toast notification for error messages.
It features a warning icon (fa-triangle-exclamation) on the left side
and the error message text on the right side.
The notification auto-dismisses after 1 second and emits a 'close' event.
This component is designed to be reusable across all Vue components in the application.

@module ErrorNotification
-->
<template>
  <!-- Error notification overlay -->
  <div v-if="visible" class="error-notification-overlay">
    <div class="error-notification">
      <!-- Left side: Warning icon -->
      <div class="error-notification-icon">
        <i class="fa-solid fa-triangle-exclamation"></i>
      </div>
      <!-- Right side: Error message -->
      <div class="error-notification-message">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
/**
 * ErrorNotification Component - Reusable error toast notification
 * 
 * This component displays a toast notification with a warning icon and error message.
 * It automatically dismisses after 1 second and emits a 'close' event to notify
 * the parent component. The component uses a fade transition for smooth animations.
 * The styling is self-contained, making it reusable by any Vue component.
 * 
 * @module ErrorNotification
 */
export default {
  name: 'ErrorNotification',

  /**
   * Component props
   * 
   * @property {boolean} visible - Controls whether the notification is shown
   * @property {string} message - The error message text to display
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
     * The error message text to display in the notification
     * 
     * This text appears on the right side of the notification,
     * next to the warning icon on the left.
     * 
     * @property {String} message
     */
    message: {
      type: String,
      default: ''
    }
  },

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

<style scoped>
/* Error notification overlay - covers the screen to center the toast */
.error-notification-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 10vh;
  pointer-events: none;
  z-index: 9999;
}

/* Error notification toast container */
.error-notification {
  display: flex;
  align-items: center;
  background-color: #1a1a1a;
  border: 1px solid #ff3333;
  border-radius: 8px;
  padding: 12px 20px;
  min-width: 300px;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(255, 0, 0, 0.3);
  animation: slideIn 0.3s ease-out;
}

/* Warning icon styling */
.error-notification-icon {
  flex-shrink: 0;
  margin-right: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-notification-icon i {
  color: #ff4444;
  font-size: 1.8rem;
  text-shadow: 0 0 8px rgba(255, 0, 0, 0.6);
}

/* Error message text styling */
.error-notification-message {
  flex: 1;
  color: #ffcccc;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.4;
  letter-spacing: 0.5px;
}

/* Slide-in animation for the notification */
@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Slide-out animation for the notification */
@keyframes slideOut {
  from {
    transform: translateY(0);
    opacity: 1;
  }
  to {
    transform: translateY(-20px);
    opacity: 0;
  }
}
</style>
