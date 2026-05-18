<!--
SuccessNotification.vue - Reusable Success Notification Toast Component

This component displays a toast notification for success messages.
It features a checkmark icon (fa-solid fa-check) on the left side
and customizable content on the right side using a default slot.
The notification auto-dismisses after 1 second and emits a 'close' event.
The styling is consistent with the ErrorNotification component but with
green color accents to indicate success.
This component is designed to be reusable across all Vue components in the application.

@module SuccessNotification
-->
<template>
  <!-- Success notification overlay -->
  <div v-if="visible" class="success-notification-overlay">
    <div class="success-notification">
      <!-- Left side: Checkmark icon -->
      <div class="success-notification-icon">
        <i class="fa-solid fa-check"></i>
      </div>
      <!-- Right side: Customizable content via slot -->
      <div class="success-notification-content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * SuccessNotification Component - Reusable success toast notification
 * 
 * This component displays a toast notification with a checkmark icon and
 * customizable content via a default slot. It automatically dismisses
 * after 1 second and emits a 'close' event to notify the parent component.
 * The styling is consistent with ErrorNotification but uses green color
 * accents to indicate success. Using a slot instead of a simple message prop
 * allows for rich content such as formatted text or additional elements.
 * 
 * @module SuccessNotification
 */
export default {
  name: 'SuccessNotification',

  /**
   * Component props
   * 
   * @property {boolean} visible - Controls whether the notification is shown
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

<style scoped>
/* Success notification overlay - covers the screen to center the toast */
.success-notification-overlay {
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

/* Success notification toast container */
.success-notification {
  display: flex;
  align-items: center;
  background-color: #1a1a1a;
  border: 1px solid #33cc33;
  border-radius: 8px;
  padding: 12px 20px;
  min-width: 300px;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 204, 0, 0.3);
  animation: slideIn 0.3s ease-out;
}

/* Checkmark icon styling */
.success-notification-icon {
  flex-shrink: 0;
  margin-right: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.success-notification-icon i {
  color: #33cc33;
  font-size: 1.8rem;
  text-shadow: 0 0 8px rgba(0, 204, 0, 0.6);
}

/* Customizable content area styling */
.success-notification-content {
  flex: 1;
  color: #ccffcc;
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
