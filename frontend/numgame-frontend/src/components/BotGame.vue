<!--
BotGame.vue - Bot Game Mode Component

This component implements the Bot (PVE) game mode. It wraps the shared
GameScreen template component and manages Bot-specific game logic,
WebSocket connection handling, and server communication.

The Bot game mode matches the player against an AI-controlled opponent.
Upon mounting, the component establishes a WebSocket connection to the
backend bot game endpoint, sends game initialization parameters (player
credentials, target number, decision time), and processes incoming messages
for turn management, score updates, and game results.

Game data flows from this component into GameScreen via props, and
user operations from GameScreen bubble back up via the @operate event.

@module BotGame
-->
<template>
  <!--
    Render the shared GameScreen template component.
    Props (enemyScore, playerScore, productivity, destructivity, actionPoints)
    provide display data. The @operate event is emitted when the user clicks
    an operation button.
  -->
  <GameScreen
    :enemyScore="enemyScore"
    :playerScore="playerScore"
    :productivity="productivity"
    :destructivity="destructivity"
    :actionPoints="actionPoints"
    :countdown="countdown"
    :turn="turn"
    @operate="handleOperation"
  />

  <!-- Error notification toast for WebSocket connection errors -->
  <ErrorNotification
    :visible="showError"
    :message="errorMessage"
    @close="showError = false"
  />
</template>

<script>
/**
 * BotGame Component - Bot game mode (PVE)
 *
 * This component serves as the parent/controller for Bot game mode.
 * It establishes a WebSocket connection to the backend upon mounting,
 * sends game initialization parameters (player credentials, target number,
 * decision time), and handles incoming WebSocket messages for turn
 * management, score updates, and game results.
 *
 * The component manages:
 * - enemyScore: The Bot's current score
 * - playerScore: The player's current score
 * - actionPoints: The player's available action points
 * - productivity: The player's current productivity value
 * - destructivity: The player's current destructivity value
 *
 * @module BotGame
 */
import GameScreen from './GameScreen.vue';
import ErrorNotification from './ErrorNotification.vue';
import config from '../utils/config.js';
import { WSResponseTypes, Operations } from '../utils/enums.js';

export default {
  // Component name used for debugging and Vue devtools
  name: 'BotGame',

  /**
   * Child components registered in this component
   *
   * @property {Component} GameScreen - The shared game screen template component
   * @property {Component} ErrorNotification - Reusable error toast notification component
   */
  components: {
    GameScreen,
    ErrorNotification
  },

  /**
   * Component data properties
   *
   * @property {number} enemyScore - The Bot's current score
   * @property {number} playerScore - The player's current score
   * @property {number} productivity - The player's current productivity value
   * @property {number} destructivity - The player's current destructivity value
   * @property {number} actionPoints - The player's available action points
   * @property {number} turn - The current game turn number (starts from 1)
   * @property {number} countdown - The countdown timer value for the player's turn, in seconds (0 = no active timer)
   * @property {WebSocket|null} ws - The WebSocket connection instance
   * @property {boolean} wsConnected - Flag indicating WebSocket connection status
   * @property {number|null} heartbeatTimer - Interval timer ID for heartbeat ping/pong
   * @property {number|null} countdownTimer - Interval timer ID for the player turn countdown
   * @property {number} playerTimeout - The player's decision time limit in seconds, read from route query
   * @property {boolean} showError - Flag controlling error notification visibility
   * @property {string} errorMessage - The error message to display in the notification
   */
  data() {
    return {
      enemyScore: 0,
      playerScore: 0,
      productivity: 1,
      destructivity: 1,
      turn: 1,
      actionPoints: 10,
      countdown: 0,
      ws: null,
      wsConnected: false,
      heartbeatTimer: null,
      countdownTimer: null,
      playerTimeout: 30,
      showError: false,
      errorMessage: ''
    };
  },

  /**
   * Component lifecycle hook - mounted
   *
   * Reads game parameters (target, player_timeout) from the route query,
   * then initiates a WebSocket connection to the backend bot game endpoint.
   */
  mounted() {
    console.log('BotGame component mounted');

    // Read game parameters from route query
    const target = this.$route.query.target;
    const playerTimeout = this.$route.query.player_timeout;

    // Store the player timeout value for countdown usage
    this.playerTimeout = parseInt(playerTimeout, 10) || 30;

    // Establish WebSocket connection
    this.connectWebSocket(target, playerTimeout);
  },

  /**
   * Component lifecycle hook - beforeUnmount
   *
   * Cleans up the WebSocket connection and heartbeat timer
   * when the component is destroyed to prevent memory leaks.
   */
  beforeUnmount() {
    this.disconnectWebSocket();
  },

  /**
   * Component methods
   */
  methods: {
    /**
     * connectWebSocket - Establishes WebSocket connection to the backend
     *
     * Constructs the WebSocket URL by combining the WebSocket backend URL
     * with the bot game endpoint path and appending query parameters
     * target and player_timeout. Sets up message, error, and close
     * event handlers for managing the connection lifecycle.
     *
     * @method connectWebSocket
     * @param {string} target - The game target number from the setup screen
     * @param {string} playerTimeout - The decision time limit in seconds
     */
    connectWebSocket(target, playerTimeout) {
      // Build the WebSocket URL with query parameters: ws://localhost:7111/api/game/botPlay?target=100&player_timeout=30
      const wsUrl = `${config.getWsBackendUrl()}${config.getBotGameEndpoint()}?target=${encodeURIComponent(target)}&player_timeout=${encodeURIComponent(playerTimeout)}`;
      console.log('Connecting to WebSocket:', wsUrl);

      // Create a new WebSocket connection
      this.ws = new WebSocket(wsUrl);

      /**
       * WebSocket onopen event handler
       *
       * Called when the WebSocket connection is successfully established.
       *
       * @event WebSocket#onopen
       */
      this.ws.onopen = () => {
        console.log('WebSocket connection established');
        this.wsConnected = true;
      };

      /**
       * WebSocket onmessage event handler
       *
       * Called when a message is received from the backend server.
       * Parses the JSON payload and dispatches handling based on the
       * message type using the WSResponseTypes enum.
       * If the message type is HEARTBEAT (1), responds with the same
       * type and the original sequence number to maintain the connection.
       *
       * @event WebSocket#onmessage
       * @param {MessageEvent} event - The message event containing server data
       */
      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          console.log('WebSocket message received:', message);

          // Handle heartbeat: respond with { type: 1, sequence: <original sequence> }
          if (message.type === WSResponseTypes.HEARTBEAT) {
            const heartbeatResponse = {
              type: WSResponseTypes.HEARTBEAT,
              sequence: message.sequence
            };
            this.ws.send(JSON.stringify(heartbeatResponse));
            return;
          }

          // Handle game state updates
          this.handleGameMessage(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      /**
       * WebSocket onerror event handler
       *
       * Called when a WebSocket error occurs.
       * Logs the error for debugging purposes.
       *
       * @event WebSocket#onerror
       * @param {Event} error - The error event
       */
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      /**
       * WebSocket onclose event handler
       *
       * Called when the WebSocket connection is closed (either by the server
       * or due to an error). Cleans up the connection state and heartbeat timer,
       * and displays an error notification to inform the user.
       *
       * @event WebSocket#onclose
       * @param {CloseEvent} event - The close event with code and reason
       */
      this.ws.onclose = (event) => {
        console.log('WebSocket connection closed:', event.code, event.reason);
        this.wsConnected = false;
        this.ws = null;

        // Clear heartbeat timer
        if (this.heartbeatTimer) {
          clearInterval(this.heartbeatTimer);
          this.heartbeatTimer = null;
        }

        // Show error notification and navigate back to game setup
        this.showError = true;
        this.errorMessage = 'Connection lost. Returning to game setup...';

        // Navigate back to StartBotGame page after a brief delay
        setTimeout(() => {
          this.$router.push({ name: 'StartBotGame' });
        }, 1500);
      };
    },

    /**
     * disconnectWebSocket - Closes the WebSocket connection
     *
     * Closes the WebSocket if it is currently open and clears
     * the heartbeat timer and countdown timer. Called during
     * component cleanup.
     *
     * @method disconnectWebSocket
     */
    disconnectWebSocket() {
      // Clear heartbeat timer
      if (this.heartbeatTimer) {
        clearInterval(this.heartbeatTimer);
        this.heartbeatTimer = null;
      }

      // Clear countdown timer
      this.stopCountdown();

      // Close WebSocket connection
      if (this.ws) {
        this.ws.close(1000, 'Component unmounted');
        this.ws = null;
      }

      this.wsConnected = false;
      console.log('WebSocket disconnected');
    },

    /**
     * handleGameMessage - Processes incoming game messages from the WebSocket
     *
     * Dispatches handling based on the message type. This method interprets
     * the WSResponseTypes enum to determine the appropriate action for each
     * server message, such as updating game state, handling turn transitions,
     * or detecting win/loss conditions.
     *
     * @method handleGameMessage
     * @param {Object} message - The parsed WebSocket message object
     * @param {number} message.type - The message type identifier from WSResponseTypes
     * @param {Object} [message.data] - The message payload with game state data
     */
    handleGameMessage(message) {
      switch (message.type) {
        case WSResponseTypes.DATA_UPDATE:
          console.log('Data update received:', message.data);
          // Update game state from the data payload
          if (message.data) {
            if (message.data.opponent_point !== undefined) {
              this.enemyScore = message.data.opponent_point;
            }
            if (message.data.point !== undefined) {
              this.playerScore = message.data.point;
            }
            if (message.data.action_point !== undefined) {
              this.actionPoints = message.data.action_point;
            }
            if (message.data.productivity !== undefined) {
              this.productivity = message.data.productivity;
            }
            if (message.data.destructivity !== undefined) {
              this.destructivity = message.data.destructivity;
            }
            if (message.data.turn !== undefined) {
              this.turn = message.data.turn;
            }
          }
          break;

        case WSResponseTypes.PLAYER_TURN_START:
          console.log('Player turn started');
          // Start the countdown timer for the player's turn
          this.startCountdown();
          break;

        case WSResponseTypes.BOT_TURN_START:
          console.log('Bot turn started');
          // Stop the countdown timer when the bot's turn begins
          this.stopCountdown();
          break;

        case WSResponseTypes.BOT_TURN_FINISH:
          console.log('Bot turn finished');
          break;

        case WSResponseTypes.PLAYER_WIN:
          console.log('Player wins!');
          break;

        case WSResponseTypes.BOT_WIN:
          console.log('Bot wins!');
          break;

        default:
          console.log('Unhandled message type:', message.type);
      }
    },

    /**
     * operationToEnum - Maps a string operation name to its Operations enum value
     *
     * Converts the camelCase operation identifiers emitted by GameScreen
     * (e.g., 'enhanceProductivity', 'enhanceDestructivity') to the corresponding
     * numeric enum values from the Operations enum.
     *
     * @method operationToEnum
     * @param {string} operation - The string operation identifier from GameScreen
     * @returns {number|null} The numeric Operations enum value, or null if unknown
     */
    operationToEnum(operation) {
      const operationMap = {
        produce: Operations.PRODUCE,
        destruct: Operations.DESTRUCT,
        enhanceProductivity: Operations.ENHANCE_PRODUCTIVITY,
        enhanceDestructivity: Operations.ENHANCE_DESTRUCTIBILITY,
        enhanceActionPoints: Operations.ENHANCE_ACTION_POINT,
        skip: Operations.SKIP
      };
      return operationMap[operation] || null;
    },

    /**
     * handleOperation - Handles game operation events from GameScreen
     *
     * Converts the string operation identifier from GameScreen to the
     * corresponding Operations enum numeric value, then sends it to the
     * backend via WebSocket as a PLAYER_OPERATION message.
     *
     * @method handleOperation
     * @param {string} operation - The operation identifier from GameScreen
     *   ('produce', 'destruct', 'enhanceProductivity', 'enhanceDestructivity',
     *    'enhanceActionPoints', 'skip')
     */
    handleOperation(operation) {
      console.log('BotGame operation triggered:', operation);

      // Map string operation to numeric Operations enum value
      const operationEnum = this.operationToEnum(operation);

      if (operationEnum === null) {
        console.warn('Unknown operation:', operation);
        return;
      }

      // Only stop the countdown and end the turn when the player explicitly skips
      // Other operations (produce, destruct, enhance) consume AP but keep the turn alive
      if (operationEnum === Operations.SKIP) {
        this.stopCountdown();
      }

      // Send operation to backend via WebSocket
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        const operationMessage = {
          type: WSResponseTypes.PLAYER_OPERATION,
          operation: operationEnum
        };
        this.ws.send(JSON.stringify(operationMessage));
        console.log('Operation sent:', operationEnum);
      } else {
        console.warn('WebSocket is not connected, cannot send operation');
      }
    },

    /**
     * startCountdown - Starts the countdown timer for the player's turn
     *
     * Initializes the countdown to the player's timeout value (in seconds)
     * and sets up an interval that decrements the countdown every second.
     * When the countdown reaches zero, the player's turn is considered
     * forfeited and a SKIP operation is automatically sent to the backend.
     *
     * @method startCountdown
     */
    startCountdown() {
      // Clear any existing countdown timer before starting a new one
      this.stopCountdown();

      // Set the countdown to the player's timeout value
      this.countdown = this.playerTimeout;

      // Set up an interval to decrement the countdown every second
      this.countdownTimer = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        }

        // When the countdown reaches zero, auto-skip the player's turn
        if (this.countdown <= 0) {
          this.stopCountdown();
          console.log('Player turn timeout - auto-sending skip');

          // Auto-send a SKIP operation to the backend
          if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            const skipMessage = {
              type: WSResponseTypes.PLAYER_OPERATION,
              operation: Operations.SKIP
            };
            this.ws.send(JSON.stringify(skipMessage));
            console.log('Auto-skip sent due to timeout');
          }
        }
      }, 1000);
    },

    /**
     * stopCountdown - Stops the countdown timer and resets countdown display
     *
     * Clears the countdown interval timer and resets the countdown
     * value to 0, so the countdown display in GameScreen disappears
     * (since it uses v-if="countdown > 0").
     *
     * @method stopCountdown
     */
    stopCountdown() {
      if (this.countdownTimer) {
        clearInterval(this.countdownTimer);
        this.countdownTimer = null;
      }
      this.countdown = 0;
    }
  }
}
</script>

<style scoped src="../assets/styles/game-screen.css"></style>
