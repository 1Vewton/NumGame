<!--
GameRulesModal.vue - Reusable Game Rules Modal Component

This component provides a reusable modal that displays the NumGame rules,
including Objective, Action Points, Operations, and Winning Condition.
It can be used across multiple screens (StartScreen, GameScreen, etc.).

The component uses globally imported shared styles:
  - modal-pattern.css    (overlay, container, header, close button)
  - game-rules-content.css (sections, text, operation entries, button container)
  - animations.css       (@keyframes fadeIn)
  - scrollbar.css        (.custom-scrollbar)

@module GameRulesModal
-->
<template>
  <div v-if="visible" class="rules-overlay">
    <div class="rules-modal custom-scrollbar">

      <!-- Header with title and close button -->
      <div class="rules-header">
        <h2 class="rules-title">Game Rules</h2>
        <button class="rules-close-button" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- Rules content -->
      <div class="rules-content">
        <div class="rules-section">
          <h3 class="rules-section-title">Objective</h3>
          <p class="rules-text">
            Defeat your opponent by having a higher score and reaching the target number.
          </p>
        </div>

        <div class="rules-section">
          <h3 class="rules-section-title">Action Points</h3>
          <p class="rules-text">
            Each turn, you have a certain number of <strong>Action Points (AP)</strong>.
            You can consume <strong>10 AP</strong> to perform an operation.
            Choose wisely — every action costs resources.
          </p>
        </div>

        <div class="rules-section">
          <h3 class="rules-section-title">Operations</h3>

          <div class="rules-operation">
            <div class="rules-operation-icon">
              <i class="fas fa-plus-circle"></i>
            </div>
            <div class="rules-operation-info">
              <span class="rules-operation-name">Produce</span>
              <span class="rules-operation-desc">
                Add your <strong>Productivity</strong> value to your own score.
              </span>
            </div>
          </div>

          <div class="rules-operation">
            <div class="rules-operation-icon">
              <i class="fas fa-minus-circle"></i>
            </div>
            <div class="rules-operation-info">
              <span class="rules-operation-name">Destruct</span>
              <span class="rules-operation-desc">
                Subtract your <strong>Destructivity</strong> value from the opponent's score.
              </span>
            </div>
          </div>

          <div class="rules-operation">
            <div class="rules-operation-icon">
              <i class="fas fa-arrow-up"></i>
            </div>
            <div class="rules-operation-info">
              <span class="rules-operation-name">Enhance Productivity</span>
              <span class="rules-operation-desc">
                Permanently increase your <strong>Productivity</strong> by 1.
              </span>
            </div>
          </div>

          <div class="rules-operation">
            <div class="rules-operation-icon">
              <i class="fas fa-arrow-down"></i>
            </div>
            <div class="rules-operation-info">
              <span class="rules-operation-name">Enhance Destructivity</span>
              <span class="rules-operation-desc">
                Permanently increase your <strong>Destructivity</strong> by 1.
              </span>
            </div>
          </div>

          <div class="rules-operation">
            <div class="rules-operation-icon">
              <i class="fas fa-bolt"></i>
            </div>
            <div class="rules-operation-info">
              <span class="rules-operation-name">Enhance Action Points</span>
              <span class="rules-operation-desc">
                Permanently increase the <strong>AP</strong> you gain each turn by 1.
              </span>
            </div>
          </div>
        </div>

        <div class="rules-section">
          <h3 class="rules-section-title">Winning Condition</h3>
          <p class="rules-text">
            You win when your <strong>score exceeds your opponent's</strong> and
            reaches or surpasses the <strong>target number</strong> set at the start of the game.
          </p>
        </div>
      </div>

      <!-- Close button -->
      <div class="rules-button-container">
        <AppButton
          label="Got it!"
          variant="primary"
          size="medium"
          width="100%"
          @click="$emit('close')"
        />
      </div>
    </div>
  </div>
</template>

<script>
/**
 * GameRulesModal Component - Reusable game rules modal
 *
 * This component displays the NumGame rules in a modal overlay.
 * It can be used across multiple screens by passing a `visible` prop
 * and listening for the `close` event.
 *
 * @module GameRulesModal
 */
import AppButton from './AppButton.vue';

export default {
  // Component name used for debugging and Vue devtools
  name: 'GameRulesModal',

  /**
   * Child components registered in this component
   *
   * @property {Component} AppButton - Reusable styled button component
   */
  components: {
    AppButton
  },

  /**
   * Component props - External data passed to the component
   *
   * @property {boolean} visible - Controls whether the rules modal is visible
   */
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },

  /**
   * Component emits - Events emitted to the parent
   *
   * @event close - Emitted when the user dismisses the modal
   */
  emits: ['close']
}
</script>
