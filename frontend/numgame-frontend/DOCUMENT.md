# NumGame Frontend - Module Documentation

> **This file contains detailed documentation for all modules in the NumGame frontend project.**
> Agents: When you need to understand a component, utility module, or configuration file, consult this document first.

---

## Application Entry Point (`src/main.js`)

**Purpose**: Initializes and mounts the Vue.js application.

**Functions**:
- `createApp(App)`: Creates a new Vue application instance with the root App component
  - `App` (Component): The root App component to bootstrap the application
  - Returns: Vue application instance
- `.mount('#app')`: Mounts the application to the DOM
  - `selector` (string): CSS selector for the DOM element ('#app')

**Integration**: Called by the browser to start the application.

---

## Root Application Component (`src/App.vue`)

**Purpose**: Serves as the container for all game components.

**Component Properties**:
- `name` (string): 'App' - Component identifier
- `components` (object): Child components registered in this component

**Template Structure**: Main container with logo and HelloWorld component.

**Integration**: Root of the component hierarchy.

---

## HelloWorld Component (`src/components/HelloWorld.vue`)

**Purpose**: Demo component that will be replaced with actual game components.

**Component Properties**:
- `name` (string): 'HelloWorld' - Component identifier
- `props.msg` (string): Message to display (passed from parent)

**Template Structure**: Displays message and Vue.js documentation links.

**Notes**: Placeholder for game-specific components.

---

## AppInput Component (`src/components/AppInput.vue`)

**Purpose**: Reusable white-themed input field component with label support and v-model binding.

**Component Properties**:
- `name` (string): 'AppInput' - Component identifier
- `props.modelValue` (String|Number): The current input value for v-model two-way binding
- `props.type` (String, default: 'text'): HTML input type attribute (e.g., 'text', 'password')
- `props.placeholder` (String): Placeholder text displayed inside the input when empty
- `props.label` (String): Optional label text displayed above the input field
- `props.inputId` (String): Unique identifier for the input element for label association

**Events**:
- `update:modelValue`: Emitted when the input value changes (for v-model binding)
- `enter`: Emitted when the Enter key is pressed while the input is focused

**Template Structure**: 
- Optional label element above the input field
- White-themed input field with dark text
- Placeholder text for user guidance
- Red focus border matching the app color theme

**Styling Features**:
- White background with dark (#333333) text for contrast
- Red border focus state to match NumGame's color theme
- Smooth transitions for focus and hover states
- Hover effect with lighter red border

**Integration**: Used by any Vue component that needs styled input fields, particularly the StartScreen login form.

---

## AppButton Component (`src/components/AppButton.vue`)

**Purpose**: Reusable styled button component with loading state, multiple sizes, color variants, and custom width support.

**Component Properties**:
- `name` (string): 'AppButton' - Component identifier
- `props.label` (String, default: 'Button'): Button text displayed when no slot content is provided
- `props.loadingLabel` (String, default: 'Loading...'): Text displayed next to spinner during loading state
- `props.isLoading` (Boolean, default: false): Controls loading spinner and disabled state
- `props.disabled` (Boolean, default: false): Controls whether the button is disabled
- `props.size` (String, default: 'medium'): Button size variant ('small', 'medium', 'large')
- `props.variant` (String, default: 'primary'): Visual style variant ('primary'=red, 'secondary'=gray, 'success'=green)
- `props.width` (String, default: ''): Custom CSS width value (e.g., '100%', '200px', 'auto')
- `props.type` (String, default: 'button'): HTML button type ('button' or 'submit')

**Events**:
- `click`: Emitted when the button is clicked (only fires when not loading/disabled)

**Slots**:
- `default`: Custom button content (replaces label prop when provided)

**Template Structure**: 
- Styled button element with dynamic class bindings for variant, size, and loading state
- Loading state shows a spinning circle animation with loading label
- Normal state displays slot content or label text

**Styling Features**:
- Three size variants (small/medium/large) with appropriate padding and font sizes
- Three color variants (primary red, secondary gray, success green) with hover/active/disabled states
- Loading spinner animation using CSS keyframes
- Custom width support via inline style binding
- Disabled state with reduced opacity and cursor change

**Integration**: Used by any Vue component that needs styled buttons. Currently used in StartScreen for the login button with primary red variant and full width.

---

## ErrorNotification Component (`src/components/ErrorNotification.vue`)

**Purpose**: Reusable error toast notification component with warning icon and auto-dismiss.

**Component Properties**:
- `name` (string): 'ErrorNotification' - Component identifier
- `props.visible` (Boolean, default: false): Controls whether the notification is shown
- `props.message` (String, default: ''): The error message text to display

**Events**:
- `close`: Emitted after 1 second auto-dismiss timer expires

**Template Structure**: 
- Centered overlay notification at the top of the viewport
- Left section with fa-solid fa-triangle-exclamation warning icon
- Right section displaying error message text

**Styling Features**:
- Dark background (#1a1a1a) with red border and shadow for visibility
- Red warning icon with glow effect
- Slide-in animation for smooth appearance
- Fixed positioning for global overlay display
- Min/max width constraints for consistent sizing

**Integration**: Used by any Vue component to display error messages. Currently used in StartScreen for login error feedback.

---

## SuccessNotification Component (`src/components/SuccessNotification.vue`)

**Purpose**: Reusable success toast notification component with checkmark icon and slot-based customizable content.

**Component Properties**:
- `name` (string): 'SuccessNotification' - Component identifier
- `props.visible` (Boolean, default: false): Controls whether the notification is shown

**Events**:
- `close`: Emitted after 1 second auto-dismiss timer expires

**Slots**:
- `default`: Customizable content area on the right side of the notification

**Template Structure**: 
- Centered overlay notification at the top of the viewport
- Left section with fa-solid fa-check checkmark icon
- Right section with customizable content via default slot

**Styling Features**:
- Dark background (#1a1a1a) with green border and shadow for visibility
- Green checkmark icon with glow effect
- Consistent layout and animation with ErrorNotification component
- Fixed positioning for global overlay display
- Min/max width constraints for consistent sizing

**Integration**: Used by any Vue component to display success messages. Currently used in StartScreen to display "Login Successful" message after successful authentication.

---

## StartBotGame Component (`src/components/StartBotGame.vue`)

**Purpose**: Displays the Bot game setup screen with a red and black color theme, a crosshairs icon (fa-crosshairs), and a single input field for entering the game target number.

**Component Properties**:
- `name` (string): 'StartBotGame' - Component identifier
- `components` (Object): Registered child components - AppInput, AppButton, ErrorNotification, SuccessNotification

**Data Properties**:
- `data.targetNumber` (number): The target number for the Bot game (default: 10), bound to the input field via v-model
- `data.decisionTime` (number): The decision time limit in seconds (default: 30), bound to the input field via v-model
- `data.showError` (boolean): Flag controlling error notification visibility
- `data.errorMessage` (string): Error message to display in the notification
- `data.showSuccess` (boolean): Flag controlling success notification visibility
- `data.successMessage` (string): Success message to display in the notification

**Template Structure**: 
- Main container with black background
- Red crosshairs icon (fa-crosshairs) using Font Awesome
- Welcome title with red gradient text ("Bot Game")
- Subtitle "Set a target number and decision time to challenge the Bot"
- Single input field for "Game Target" number (using AppInput component)
- Single input field for "Decision Time (s)" number (using AppInput component)
- Error notification toast (using ErrorNotification component)
- Success notification toast (using SuccessNotification component)
- Responsive design for different screen sizes

**Styling Features**:
- Red and black color theme matching StartScreen
- Cascadia Code font family
- Responsive layout with content positioned higher
- Red crosshairs icon with glow effect
- Gradient text effects for welcome message
- White input field with red focus state

**Integration**: New Vue Router route at `/startBotGame`. Uses AppInput for the target number input field and AppButton, ErrorNotification, SuccessNotification for UI elements. No internal game logic implemented yet.

---

## StartScreen Component (`src/components/StartScreen.vue`)

**Purpose**: Displays the welcome screen for the NumGame application with red and black color theme and login functionality.

**Component Properties**:
- `name` (string): 'StartScreen' - Component identifier
- `components` (Object): Registered child components - AppInput, AppButton, ErrorNotification, SuccessNotification, UserInfo

- `mounted()`: Lifecycle hook that logs when component is mounted
- `data.username` (string): Username entered by the user in the login form
- `data.password` (string): Password entered by the user in the login form
- `data.isLoggingIn` (boolean): Flag indicating if a login request is in progress
- `data.isRegistering` (boolean): Flag indicating if a registration request is in progress
- `data.showLogin` (boolean): Flag indicating whether to show login or registration form
- `data.registerUsername` (string): Username entered in the registration form
- `data.registerPassword` (string): Password entered in the registration form
- `data.registerConfirmPassword` (string): Confirm password entered in the registration form
- `data.showError` (boolean): Flag controlling error notification visibility
- `data.errorMessage` (string): Error message to display in the notification
- `data.showSuccess` (boolean): Flag controlling success notification visibility
- `data.successMessage` (string): Success message to display in the notification
- `data.showUserInfo` (boolean): Flag controlling the UserInfo modal visibility
- `data.showGameRules` (boolean): Flag controlling the Game Rules modal visibility
- `computed.canRegister` (boolean): True when password meets format requirements and confirm password matches
- `computed.loggedIn` (boolean): Returns `userStore.isUserLoggedIn()`. When true, the login/registration forms are hidden via `v-if="!loggedIn"` in the template

**Methods**:
- `switchToRegister()`: Sets showLogin to false to display the registration form
- `switchToLogin()`: Sets showLogin to true to display the login form
- `handleAutoLogin()`: Sends a GET request to the auto-login endpoint (no request body) when the component mounts. If `response.success` is truthy, the user's session data (`user_id`, `user_name`) is stored in userStore silently — no notification shown regardless of success or failure.
- `handleLogin()`: Validates credentials and sends login request to backend API. On success (`response.success === true`), stores `user_id` and `user_name` in the reactive in-memory userStore. Shows error notification on failure.
- `showErrorMessage(message)`: Sets error message and shows the error notification toast.
- `handleRegister()`: Sends registration request to backend API with username and password. Shows success notification on success or error notification on failure.

**Login Status Determination Logic**:
The component determines login status through three mechanisms:

1. **Manual Login** (`handleLogin()`): After the user submits the login form, the method sends a POST request to the login endpoint. The response is checked for `response.success`. If truthy, `userStore.setUser(response.user_id, response.user_name)` is called, which sets `state.isLoggedIn = true` and makes the `loggedIn` computed property return `true`, causing the forms to disappear via `v-if="!loggedIn"`.

2. **Auto Login** (`handleAutoLogin()`): On component mount (`mounted()`), a silent GET request is sent to the auto-login endpoint with cookies (`withCredentials: true` in axios). If `response.success` is truthy, `userStore.setUser(response.user_id, response.user_name)` is called, and the forms disappear automatically — no notification displayed.

3. **Reactive Computed Property** (`loggedIn`): This computed property reads `userStore.isUserLoggedIn()`, which checks `state.isLoggedIn`. Since userStore uses Vue.observable (reactive state), any change (from either manual or auto login) immediately triggers re-rendering. In the template, `<div v-if="!loggedIn">` wraps the entire form block, so forms are hidden when `loggedIn` is `true`.

**Template Structure**: 
- Main container with black background
- Game rules icon button (fa-circle-info) at the top-left corner (always visible)
- User info icon button (fa-circle-user) at the top-right corner (only visible when logged in)
- UserInfo modal overlay (shown when showUserInfo is true)
- Game Rules modal overlay (shown when showGameRules is true), containing:
  - **Objective**: Defeat opponent by having a higher score and reaching the target number
  - **Action Points**: Consume 10 AP to perform an operation
  - **Operations list** — 5 operations each with a Font Awesome icon:
    - `fas fa-plus-circle` — Produce: Add your Productivity value to your own score
    - `fas fa-minus-circle` — Destruct: Subtract your Destructivity value from the opponent's score
    - `fas fa-arrow-up` — Enhance Productivity: Permanently increase Productivity by 1
    - `fas fa-arrow-down` — Enhance Destructivity: Permanently increase Destructivity by 1
    - `fas fa-bolt` — Enhance Action Points: Permanently increase AP gained per turn by 1
  - **Winning Condition**: Score exceeds opponent AND reaches/passes the target number
  - "Got it!" button to dismiss the modal
- Red X-mark icon using Font Awesome
- Welcome title with red gradient text
- Subtitle for game description
- Login form with username and password fields (using AppInput component) and Login/Register buttons
- Registration form with username, password, confirm password fields (using AppInput component) and Register/Back to Login buttons
- Password format hint text
- Error notification toast (using ErrorNotification component)
- Success notification toast (using SuccessNotification component)
- Responsive design for different screen sizes

**Styling Features**:
- Red and black color theme
- Cascadia Code font family
- Responsive layout with content positioned higher
- Red X-mark icon without background decoration
- Gradient text effects for welcome message
- White input fields with red focus states
- Red Login button with hover/active/disabled states
- Register button follows variant design principle (primary when valid, secondary when disabled)
- User icon button positioned absolutely at top-right with red color and hover glow effect
- Game rules icon button positioned absolutely at top-left with red color and hover glow effect

**Integration**: Uses AppInput for login/registration form fields and AppButton for buttons. Uses UserInfo for the user information modal. Uses apiClient and config modules to send login and registration requests. Stores user credentials in the reactive in-memory userStore for the current browser session.

---

## GameRulesModal Component (`src/components/GameRulesModal.vue`)

**Purpose**: A reusable game rules modal component that can be used across multiple screens (StartScreen, GameScreen, etc.). Displays the NumGame rules including Objective, Action Points, Operations, and Winning Condition.

**Component Properties**:
- `name` (string): 'GameRulesModal' - Component identifier
- `components` (Object): Registered child components - AppButton

**Props**:
- `visible` (Boolean, default: false): Controls whether the rules modal is visible

**Emits**:
- `close`: Emitted when the user dismisses the modal (via close button or "Got it!" button)

**Template Structure**:
- Modal overlay with dark backdrop and scrollable content area
- Header with "Game Rules" title and close (X) button
- **Objective**: Defeat opponent by having a higher score and reaching the target number
- **Action Points**: Consume 10 AP to perform an operation
- **Operations list** — 5 operations each with a Font Awesome icon:
  - `fas fa-plus-circle` — Produce: Add your Productivity value to your own score
  - `fas fa-minus-circle` — Destruct: Subtract your Destructivity value from the opponent's score
  - `fas fa-arrow-up` — Enhance Productivity: Permanently increase Productivity by 1
  - `fas fa-arrow-down` — Enhance Destructivity: Permanently increase Destructivity by 1
  - `fas fa-bolt` — Enhance Action Points: Permanently increase AP gained per turn by 1
- **Winning Condition**: Score exceeds opponent AND reaches/passes the target number
- "Got it!" button (AppButton, primary variant) to dismiss the modal

**Styling**: Modal pattern styles inherited from globally imported `modal-pattern.css` (overlay, container, header, close button), content styles inherited from globally imported `game-rules-content.css` (sections, text, operation entries, button container). The component uses `custom-scrollbar` from the globally imported `scrollbar.css`.

**Usage**:
```vue
<GameRulesModal
  :visible="showRules"
  @close="showRules = false"
/>
```

**Integration**: Imported and registered by StartScreen and GameScreen components. Provides a single source of truth for game rules content, eliminating duplication.

---

## UserInfo Component (`src/components/UserInfo.vue`)

**Purpose**: Displays the logged-in user's profile information in a modal overlay with red and black theme.

**Component Properties**:
- `name` (string): 'UserInfo' - Component identifier
- `components` (Object): Registered child components - AppButton

**Events**:
- `close`: Emitted when the user clicks the close button or the Back button to dismiss the modal

**Data Properties**:
- `userInfo` (Object|null): The fetched user information object from the backend API response
- `isLoading` (boolean): Flag indicating if the API request to fetch user info is in progress
- `errorMessage` (string): Error message to display if the API request fails

**Computed Properties**:
- `formattedDate` (string): Converts the `registered_at` Unix timestamp (seconds since epoch) to a human-readable YYYY-MM-DD date string. Returns 'N/A' if no timestamp is available.
- `winRate` (string): Calculates win rate as `(wins / total_games) * 100`, formatted to one decimal place (e.g., '75.0%'). Returns 'N/A' if `total_games` is 0.

**Methods**:
- `fetchUserInfo()`: Sends a POST request to the user info endpoint (`/api/user/userInfo`) with `player_name` and `player_id` from the userStore. On success, stores the `result` field in `userInfo`. On failure, sets `errorMessage` using the unified error handler.

**Template Structure**:
- Full-screen dark overlay with centered modal container
- Header with "User Information" title and close (X) button
- Loading state with spinning icon when fetching data
- Error state with warning icon and error message
- User info content showing: User ID, Username, Registered At (YYYY-MM-DD format), Wins, Total Games, Win Rate (percentage or N/A if no games)
- Back button using AppButton component (primary variant)

**Styling Features**:
- Dark modal (#1a1a1a) with red border and red glow shadow
- Fade-in slide-down animation on open
- Red title with text glow
- Info rows with dark background (#2a2a2a), left red border accent, and label/value layout
- Loading spinner in red
- Error text in red
- Close button with hover effect turning red
- Responsive layout for mobile (stacks info rows vertically)

**Notes**: Password field and Bot status are intentionally excluded from display. The component fetches data via API call on mount and shows loading/error states accordingly. Only visible when the user is logged in (controlled by parent StartScreen). Uses the `getUserInfoBody` function from requestBodies utility for the request payload.

**Integration**: Used by StartScreen component as a modal overlay. Imported and registered in StartScreen, shown conditionally via `v-if="showUserInfo"`. Communicates back to parent via `$emit('close')` event. Uses the existing userStore, config, apiClient, requestBodies, and errorHandler utilities.

---

## User Store Module (`src/stores/userStore.js`)

**Purpose**: Provides a reactive in-memory store for the current user's session data. Data is not persisted and will be lost when the browser tab is closed.

**State Properties**:
- `state.userId` (string|null): The unique identifier of the logged-in user
- `state.userName` (string|null): The display name of the logged-in user
- `state.isLoggedIn` (boolean): Flag indicating whether a user is currently logged in

**Methods**:
- `getState()`: Returns the reactive state object for direct property binding in components
  - Returns: {Object} The reactive state object
- `getUserId()`: Gets the current user's unique identifier
  - Returns: {string|null} The user ID or null
- `getUserName()`: Gets the current user's display name
  - Returns: {string|null} The user name or null
- `isUserLoggedIn()`: Checks if a user is currently logged in
  - Returns: {boolean} True if logged in, false otherwise
- `setUser(userId, userName)`: Sets the current user's session data after successful login
  - `userId` (string): The unique identifier of the user
  - `userName` (string): The display name of the user
- `clearUser()`: Clears the current user's session data on logout

**Integration**: Imported by components to access and modify user session data. Currently used by StartScreen to store user info after successful login.

---

## Router Module (`src/router/index.js`)

**Purpose**: Configures Vue Router for the NumGame frontend application, defining routing rules for navigating between different views/pages.

**Routes**:
- `path: '/'`: Maps to `StartScreen` component — renders the welcome/login screen when accessing `http://localhost:8080/` (no specific endpoint)
  - `name` (string): 'StartScreen' — Route identifier for programmatic navigation
  - `component` (Component): StartScreen — The welcome screen component to render
- `path: '/startBotGame'`: Maps to `StartBotGame` component — renders the Bot game setup screen when accessing `http://localhost:8080/startBotGame`
  - `name` (string): 'StartBotGame' — Route identifier for programmatic navigation
  - `component` (Component): StartBotGame — The Bot game setup screen component to render
  - `beforeEnter`: Navigation guard that checks if the user is logged in via `userStore.isUserLoggedIn()`. If not logged in, redirects to StartScreen.
- `path: '/botGame'`: Maps to `BotGame` component — renders the Bot game mode interface when accessing `http://localhost:8080/botGame`
  - `name` (string): 'BotGame' — Route identifier for programmatic navigation
  - `component` (Component): BotGame — The Bot game mode component (wraps the shared GameScreen template)
  - `beforeEnter`: Navigation guard that checks if the user is logged in via `userStore.isUserLoggedIn()`. If not logged in, redirects to StartScreen.

**Functions**:
- `createRouter(options)`: Creates a new Vue Router instance with HTML5 history mode
  - `options.history` — Uses `createWebHistory()` for clean URLs without hash marks
  - `options.routes` — Array of route definition objects

**Integration**: Imported by `main.js` and registered via `app.use(router)`. The root `App.vue` component renders the current route's component using `<router-view />` instead of directly importing and rendering components.

**Notes**: Uses HTML5 history mode (`createWebHistory`) for clean, hash-free URLs. Additional routes can be added to the `routes` array to support more views/pages as the application grows.

---

## Babel Configuration (`babel.config.js`)

**Purpose**: Configures Babel for JavaScript transpilation.

**Properties**:
- `presets` (Array): Babel preset configurations
  - `'@vue/cli-plugin-babel/preset'`: Vue CLI's default Babel preset

**Integration**: Used during build process for browser compatibility.

---

## Vue CLI Configuration (`vue.config.js`)

**Purpose**: Customizes Vue CLI build settings and dev server options.

**Properties**:
- `transpileDependencies` (boolean): Enable transpilation of dependencies

**Integration**: Configures the Vue CLI build system.

---

## Configuration Module (`src/utils/config.js`)

**Purpose**: Provides centralized access to environment variables from .env files.

**Functions**:
- `getBackendUrl()`: Retrieves the backend API base URL from VUE_APP_BACKEND_URL environment variable
  - Returns: {string} The backend API base URL (default: 'http://localhost:7111')
- `getRegisterEndpoint()`: Retrieves the user registration endpoint path from VUE_APP_REGISTER_ENDPOINT
  - Returns: {string} The user registration endpoint path (default: '/api/user/userRegister')
- `getLoginEndpoint()`: Retrieves the user login endpoint path from VUE_APP_LOGIN_ENDPOINT
  - Returns: {string} The user login endpoint path (default: '/api/user/userLogin')
- `getAutoLoginEndpoint()`: Retrieves the user auto-login endpoint path from VUE_APP_AUTO_LOGIN_ENDPOINT
  - Returns: {string} The user auto-login endpoint path (default: '/api/user/autoLogin')
- `getUserEndpoint()`: Retrieves the user information endpoint path from VUE_APP_USER_INFO_ENDPOINT
  - Returns: {string} The user information endpoint path (default: '/api/user/userInfo')
- `getWsBackendUrl()`: Retrieves the WebSocket backend URL from VUE_APP_WS_BACKEND_URL environment variable
  - Returns: {string} The WebSocket backend URL (default: 'ws://localhost:7111')
- `getRegisterUrl()`: Returns complete URL for user registration (backend URL + endpoint path)
  - Returns: {string} Complete URL for user registration
- `getLoginUrl()`: Returns complete URL for user login (backend URL + endpoint path)
  - Returns: {string} Complete URL for user login
- `getAutoLoginUrl()`: Returns complete URL for user auto-login (backend URL + endpoint path)
  - Returns: {string} Complete URL for user auto-login
- `getUserUrl()`: Returns complete URL for user information (backend URL + endpoint path)
  - Returns: {string} Complete URL for user information
- `getAllConfig()`: Returns all configuration values as a plain object including endpoints and full URLs
  - Returns: {Object} Object containing all configuration values (backendUrl, wsBackendUrl, registerEndpoint, loginEndpoint, autoLoginEndpoint, userEndpoint, registerUrl, loginUrl, autoLoginUrl, userUrl)
- `validateConfig()`: Validates that all required configuration values are present and valid, including backend URL format, WebSocket URL format, and endpoint path validation
  - Throws: {Error} If required configuration values are missing or invalid
  - Returns: {boolean} True if all configuration values are valid

**Integration**: Used by other modules to access configuration values including backend URL, WebSocket URL, and user authentication endpoints.

---

## API Client Module (`src/utils/api.js`)

**Purpose**: Provides a generic API client for making HTTP requests to the backend server using axios.

**Functions**:
- `post(endpoint, body, headers)`: Sends a POST request with JSON body to the specified endpoint
  - `endpoint` (string): The API endpoint path (relative to base URL)
  - `body` (Object): The request body to send as JSON
  - `headers` (Object, optional): Additional headers to include with the request
  - Returns: {Promise<Object>} Parsed JSON response from the server
  - Throws: {Error} If the request fails or returns a non-2xx status code
- `get(endpoint, headers)`: Sends a GET request to retrieve data from the specified endpoint
  - `endpoint` (string): The API endpoint path (relative to base URL)
  - `headers` (Object, optional): Additional headers to include with the request
  - Returns: {Promise<Object>} Parsed JSON response from the server
  - Throws: {Error} If the request fails or returns a non-2xx status code
- `put(endpoint, body, headers)`: Sends a PUT request to update a resource at the specified endpoint
  - `endpoint` (string): The API endpoint path (relative to base URL)
  - `body` (Object): The request body to send as JSON
  - `headers` (Object, optional): Additional headers to include with the request
  - Returns: {Promise<Object>} Parsed JSON response from the server
  - Throws: {Error} If the request fails or returns a non-2xx status code
- `delete(endpoint, body, headers)`: Sends a DELETE request to delete a resource at the specified endpoint
  - `endpoint` (string): The API endpoint path (relative to base URL)
  - `body` (Object, optional): Optional request body to send as JSON
  - `headers` (Object, optional): Additional headers to include with the request
  - Returns: {Promise<Object>} Parsed JSON response from the server
  - Throws: {Error} If the request fails or returns a non-2xx status code

**Internal Methods**:
- `_handleAxiosError(error, endpoint, method)`: Handles axios errors and provides detailed error messages with context
- Uses axios instance with pre-configured base URL, headers, and timeout settings

**Integration**: Uses the Configuration Module to get the backend URL. Uses axios library for HTTP requests with automatic JSON parsing, request/response interceptors, and comprehensive error handling. Provides HTTP client functionality for other application modules to communicate with the backend API.

---

## Request Bodies Module (`src/utils/requestBodies.js`)

**Purpose**: Provides centralized request body generation functions for API endpoints used in user authentication and information retrieval.

**Functions**:
- `getUserRegisterBody(playerName, playerPassword)`: Creates a request body for user registration
  - `playerName` (string, default: 'string'): The username for the new player account
  - `playerPassword` (string, default: 'stringst'): The password for the new player account
  - Returns: {Object} Request body with `player_name` and `player_password` properties
- `getUserLoginBody(playerName, playerPassword)`: Creates a request body for user login
  - `playerName` (string, default: 'string'): The registered username of the player
  - `playerPassword` (string, default: 'stringst'): The password credential for authentication
  - Returns: {Object} Request body with `player_name` and `player_password` properties
- `getUserInfoBody(playerName, playerId)`: Creates a request body for user information retrieval
  - `playerName` (string, default: 'string'): The username of the player to look up
  - `playerId` (string, default: 'string'): The unique identifier of the player account
  - Returns: {Object} Request body with `player_name` and `player_id` properties

**Integration**: Provides request body generation functions used by application modules when making API calls to backend endpoints for registration, login, and user information retrieval.

---

## Error Handler Module (`src/utils/errorHandler.js`)

**Purpose**: Provides a unified `extractErrorMessage` function for extracting human-readable error messages from failed API calls, following the standardized backend error response format.

**Functions**:
- `extractErrorMessage(error, fallbackMessage)`: Extracts the most meaningful error message from an API error object
  - `error` (Error): The error object from an API call (expected to have `responseData` and `message` properties)
  - `fallbackMessage` (string, default: 'Request failed'): Default message if nothing else can be extracted
  - Returns: {string} A human-readable error message
  - **Resolution order**:
    1. If `error.responseData` is an object with a `reason` string property → returns `reason`
    2. If `error.responseData` is an object without `reason` → returns JSON.stringify of the object (if not empty)
    3. If `error.responseData` is a non-empty string → returns it directly
    4. If `error.message` is a non-empty string → returns `error.message`
    5. Otherwise → returns `fallbackMessage`

**Examples**:
```javascript
// Response has "reason" key: returns "Username does not exist"
extractErrorMessage({ responseData: { reason: 'Username does not exist' } }, 'Login failed')

// Response data is a string: returns "Server error"
extractErrorMessage({ responseData: 'Server error' }, 'Login failed')

// No response data: returns "Network Error"
extractErrorMessage({ message: 'Network Error' }, 'Login failed')
```

**Integration**: Used by any component that makes API calls to handle errors consistently. Currently used in StartScreen's `handleLogin` catch block to replace manual error parsing. Future components can simply call `extractErrorMessage(error, fallback)` for standardized error display.

---

## Enums Module (`src/utils/enums.js`)

**Purpose**: Provides a centralized repository for all enumeration constants used throughout the NumGame frontend application, serving as a single source of truth for shared constant values.

**Enums**:
- `WSResponseTypes` (Object.freeze): WebSocket response type identifiers mapped to numeric values (1-11)
  - `HEARTBEAT` (1): Server heartbeat/ping to maintain connection
  - `PLAYER_OPERATION` (2): General player operation message
  - `OPERATION_EXECUTION_RESULT` (3): Result of an operation execution
  - `MOVE_DIVISION` (4): Division movement event
  - `DATA_UPDATE` (5): General data update notification
  - `BOT_TURN_START` (6): Notification that the bot's turn has started
  - `PLAYER_TURN_START` (7): Notification that the player's turn has started
  - `TURN_FINISH` (8): Notification that a turn has finished
  - `BOT_TURN_FINISH` (9): Notification that the bot's turn has finished
  - `PLAYER_WIN` (10): Notification that the player has won
  - `BOT_WIN` (11): Notification that the bot has won

**Exports**:
- Named export: `WSResponseTypes` — Individual enum import via `import { WSResponseTypes } from '@/utils/enums'`
- Default export: `enums` — Aggregate object for single-import access via `import enums from '@/utils/enums'`

**Integration**: Used by any component that needs to interpret WebSocket message types from the backend server. Provides standardized numeric type identifiers for type-safe message handling in switch statements and conditional logic.

---

---

## Scrollbar Styles (`src/assets/styles/scrollbar.css`)

**Purpose**: Provides a reusable `.custom-scrollbar` CSS class for styling scrollbars with a red and black color theme matching the NumGame application design.

**Class**:
- `.custom-scrollbar`: Apply this class to any scrollable container to style its scrollbar
  - **Firefox**: Uses `scrollbar-width: thin` and `scrollbar-color: #ff0000 #2a2a2a` (red thumb on dark track)
  - **WebKit (Chrome, Safari, Edge)**: 8px-wide red (`#ff0000`) thumb with rounded corners, dark (`#2a2a2a`) track, and a lighter red (`#ff4444`) hover state on the thumb

**Usage**:
```html
<!-- Add the class to any scrollable container -->
<div class="custom-scrollbar" style="overflow-y: auto; max-height: 300px;">
  <!-- scrollable content -->
</div>

<!-- Combine with existing classes -->
<div class="my-modal custom-scrollbar">
  <!-- scrollable content -->
</div>
```

**Integration**: Imported globally in `src/main.js` so the `.custom-scrollbar` class is available across all components without additional imports.

**Notes**: Currently used by the Game Rules modal in the StartScreen component. Can be reused by any component that needs a custom-styled scrollbar.

---

## App Styles (`src/assets/styles/app.css`)

**Purpose**: Provides global layout styles for the root App component, defining the base application container and typography.

**Selectors**:
- `#app`: Sets margin/padding to 0, `min-height: 100vh`, and the Cascadia Code monospace font family as the application default.

**Integration**: Imported globally in `src/main.js` to apply base application layout styles.

---

## AppInput Styles (`src/assets/styles/app-input.css`)

**Purpose**: Contains styles for the reusable white input field component (AppInput) with red focus/hover states.

**Key Classes**:
- `.app-input-container`: Flex column container with full width
- `.app-input-label`: White label text with spacing
- `.app-input`: White background input with dark text, red focus border (#ff0000), and red hover border (#ff6666)
- `.app-input::placeholder`: Light gray (#999999) placeholder text

**Integration**: Imported by `AppInput.vue` via `<style scoped src="...">`.

---

## AppButton Styles (`src/assets/styles/app-button.css`)

**Purpose**: Contains styles for the reusable button component (AppButton) with loading state, size variants, and color variants.

**Key Classes**:
- `.app-button`: Base button styling with flex layout, font, and transitions
- `.app-button--small/medium/large`: Size variants with appropriate padding and font sizes
- `.app-button--primary`: Red theme with hover/active/disabled states
- `.app-button--secondary`: Gray/neutral theme with hover/active/disabled states
- `.app-button--success`: Green theme with hover/active/disabled states
- `.app-button__spinner`: Loading spinner animation via `@keyframes app-button-spin`

**Integration**: Imported by `AppButton.vue` via `<style scoped src="...">`.

---

## Page Layout Styles (`src/assets/styles/page-layout.css`)

**Purpose**: Defines the base page layout shared by all screen components (StartScreen, StartBotGame, and future game screens). Provides a full-viewport black background with centered content layout and responsive breakpoints.

**Key Selectors**:
- `.start-screen`, `.start-bot-game`, `.game-screen`: Full-viewport black background (`#000000`) with centered flex column layout and box-sizing: border-box
- `.start-screen`, `.start-bot-game`: Additional 15vh top padding and bottom spacer via `::after` (game-screen uses its own internal padding via its specific CSS)

**Integration**: Imported globally in `src/main.js`. All screen components (StartScreen, StartBotGame, GameScreen) inherit the base layout automatically.

---

## Welcome Section Styles (`src/assets/styles/welcome-section.css`)

**Purpose**: Defines the welcome section styles shared across multiple screen components, including game icon styling with red glow effect and gradient welcome titles.

**Key Selectors**:
- `.game-icon-container`: Red icon container with 2.5rem bottom margin
- `.fa-5x`: Red (`#ff0000`) Font Awesome icon with 5rem size and red glow shadow
- `.welcome-container`: Centered text container, 600px max-width
- `.welcome-title`: 3.5rem red gradient text (linear-gradient `#ff0000` to `#ff6666`) with text-shadow glow
- `.welcome-subtitle`: 1.3rem light gray (`#cccccc`) subtitle with light font weight

**Integration**: Imported globally in `src/main.js`. Any screen component using `.game-icon-container`, `.fa-5x`, `.welcome-title`, etc. inherits these styles.

---

## Game Rules Content Styles (`src/assets/styles/game-rules-content.css`)

**Purpose**: Defines the reusable content styles for the Game Rules modal. The modal pattern (overlay, container, header, close button) is provided by the globally imported `modal-pattern.css`, while this file provides the inner content layout (sections, text, operation entries, close button container).

**Key Classes**:
- `.rules-content`: Flex column container for rules sections with gap spacing and bottom margin
- `.rules-section`: Section container with gap between title and content
- `.rules-section-title`: Red (`#ff0000`) section heading with glow text-shadow
- `.rules-text`, `.rules-text strong`: Light gray body text with white bold emphasis
- `.rules-operation`: Operation entry row with dark background (#2a2a2a), left red border accent (#ff0000), and rounded corners
- `.rules-operation-icon`: Red icon container with 1.8rem fixed size
- `.rules-operation-info`, `.rules-operation-name`, `.rules-operation-desc`: Label/value layout with white name and gray description
- `.rules-button-container`: Top margin for the dismiss button

**Integration**: Imported globally in `src/main.js`. Used by the GameRulesModal component for its inner content styling. Available to any component using the `.rules-*` content classes.

---

## Modal Pattern Styles (`src/assets/styles/modal-pattern.css`)

**Purpose**: Defines the reusable modal overlay pattern used by multiple components (e.g., StartScreen's game rules modal, UserInfo modal). Provides a full-screen dark backdrop, modal container with red border and glow, header with title, and close button.

**Key Selectors**:
- `.rules-overlay`, `.user-info-overlay`: Full-screen fixed dark backdrop (rgba 0,0,0,0.85) with centered flex layout
- `.rules-modal`, `.user-info-modal`: Dark modal (`#1a1a1a`) with red border (`#ff0000`), 12px border-radius, red glow shadow, and fadeIn animation
- `.rules-header`, `.user-info-header`: Flex header row with space-between title and close button, bottom border divider
- `.rules-title`, `.user-info-title`: Red title (`#ff0000`) with 1.5rem size and red glow text-shadow
- `.rules-close-button`, `.close-button`: Gray close button with red hover state and background highlight

**Integration**: Imported globally in `src/main.js`. Any component using the modal pattern (overlay + modal + header + close button) inherits these styles automatically.

---

## Animation Styles (`src/assets/styles/animations.css`)

**Purpose**: Defines reusable CSS animation keyframes shared across multiple components.

**Keyframes**:
- `@keyframes fadeIn`: Fade-in slide-down from -20px to 0 (used by modal containers)
- `@keyframes slideIn`: Slide-in from -20px to 0 (used by notification toasts on enter)
- `@keyframes slideOut`: Slide-out from 0 to -20px (used by notification toasts on dismiss)

**Integration**: Imported globally in `src/main.js`. Any component using `animation: fadeIn`, `animation: slideIn`, or `animation: slideOut` inherits these keyframes automatically.

---

## ErrorNotification Styles (`src/assets/styles/error-notification.css`)

**Purpose**: Contains styles for the reusable error notification toast component with red accent colors. The `slideIn`/`slideOut` animations are now defined in `animations.css`.

**Key Classes**:
- `.error-notification-overlay`: Fixed full-screen overlay centered at top
- `.error-notification`: Dark container with red border (#ff3333) and glow shadow
- `.error-notification-icon i`: Red (#ff4444) warning icon with glow effect
- `.error-notification-message`: Light red (#ffcccc) text for error message

**Integration**: Imported by `ErrorNotification.vue` via `<style scoped src="...">`. Animations inherited from globally imported `animations.css`.

---

## SuccessNotification Styles (`src/assets/styles/success-notification.css`)

**Purpose**: Contains styles for the reusable success notification toast component with green accent colors. The `slideIn`/`slideOut` animations are now defined in `animations.css`.

**Key Classes**:
- `.success-notification-overlay`: Fixed full-screen overlay centered at top
- `.success-notification`: Dark container with green border (#33cc33) and glow shadow
- `.success-notification-icon i`: Green (#33cc33) checkmark icon with glow effect
- `.success-notification-content`: Light green (#ccffcc) text for customizable content

**Integration**: Imported by `SuccessNotification.vue` via `<style scoped src="...">`. Animations inherited from globally imported `animations.css`.

---

## HelloWorld Styles (`src/assets/styles/hello-world.css`)

**Purpose**: Contains styles for the demo/placeholder HelloWorld component.

**Key Selectors**:
- `h3`: Top margin for section headings
- `ul`, `li`: Unstyled list with inline-block items
- `a`: Green (#42b983) link color

**Integration**: Imported by `HelloWorld.vue` via `<style scoped src="...">`.

---

## StartScreen Styles (`src/assets/styles/start-screen.css`)

**Purpose**: Contains styles specific to the StartScreen component only. Shared base styles are imported globally from separate files:
- `page-layout.css` — screen base layout, shared responsive breakpoints
- `welcome-section.css` — game icon, welcome title/subtitle
- `modal-pattern.css` — modal overlay, container, header, close button
- `animations.css` — `@keyframes fadeIn`, `slideIn`, `slideOut`

**Key Classes**:
- `.user-icon-container` / `.user-icon-button`: Top-right user icon with red hover glow
- `.rules-icon-container` / `.rules-icon-button`: Top-left rules icon with red hover glow
- `.login-form`: Centered form container with flex column layout
- `.password-hint`: Light gray hint text for password format
- `.rules-modal`: Overrides base modal width (560px) and adds max-height/overflow
- `.rules-content`, `.rules-section`: Content sections with red section titles
- `.rules-operation`: Operation entry with red left border accent
- `.game-mode-container`, `.game-mode-item`: Game mode selection grid with tooltips
- `.game-mode-icon`, `.game-mode-tooltip`: Icon and hover-tooltip styling
- Responsive breakpoints at 768px and 480px (StartScreen-specific overrides only)

**Integration**: Imported by `StartScreen.vue` via `<style scoped src="...">`. Base layout, welcome, icon, modal, and animation styles inherited from globally imported shared CSS files.

---

## StartBotGame Styles (`src/assets/styles/start-bot-game.css`)

**Purpose**: Contains styles specific to the StartBotGame component only. Shared base styles are imported globally from separate files:
- `page-layout.css` — screen base layout, shared responsive breakpoints
- `welcome-section.css` — game icon, welcome title/subtitle
- `animations.css` — `@keyframes fadeIn`, `slideIn`, `slideOut`

**Key Classes**:
- `.setup-form`: Form container with flex column layout
- `.start-button-container`: Button container with max-width
- Responsive breakpoints at 768px and 480px (StartBotGame-specific overrides only)

**Integration**: Imported by `StartBotGame.vue` via `<style scoped src="...">`. Base layout, welcome, icon, and animation styles inherited from globally imported shared CSS files.

---

## UserInfo Styles (`src/assets/styles/user-info.css`)

**Purpose**: Contains styles specific to the UserInfo component only. Shared base styles are imported globally from:
- `modal-pattern.css` — modal overlay, container, header, close button
- `animations.css` — `@keyframes fadeIn`, `slideIn`, `slideOut`

**Key Classes**:
- `.loading-state`, `.loading-spinner`: Loading state with red spinner
- `.error-state`: Error state with red (#ff4444) text and icon
- `.user-info-content`: Content area with gap spacing
- `.info-row`: Info row with dark background and red left border accent
- `.info-label`, `.info-value`: Label and value text styling
- `.back-button-container`: Button container
- `.user-info-modal`: Overrides base modal max-width to 480px
- Responsive breakpoint at 480px (stacks rows vertically)

**Integration**: Imported by `UserInfo.vue` via `<style scoped src="...">`. Base overlay, modal, header, title, close button, and animation styles inherited from globally imported shared CSS files.

---

## BotGame Component (`src/components/BotGame.vue`)

**Purpose**: Implements the Bot (PVE) game mode. Wraps the shared GameScreen template component and manages Bot-specific game logic, WebSocket connection handling, and server communication. Upon mounting, establishes a WebSocket connection to the backend bot game endpoint, sends game initialization parameters (player credentials, target number, decision time), and processes incoming messages for turn management, score updates, and game results.

**Component Properties**:
- `name` (string): 'BotGame' - Component identifier

**Dependencies**:
- `GameScreen` (Component): Imported from `./GameScreen.vue` — the shared game UI template
- `config` (Module): Imported from `../utils/config.js` — provides WebSocket URL and bot game endpoint
- `userStore` (Module): Imported from `../stores/userStore.js` — provides player credentials (userName, userId)
- `WSResponseTypes` (Enum): Imported from `../utils/enums.js` — WebSocket message type identifiers

**Data Properties**:
- `data.enemyScore` (number): The Bot's current score (default: 0)
- `data.playerScore` (number): The player's current score (default: 0)
- `data.productivity` (number): The player's current productivity value (default: 1)
- `data.destructivity` (number): The player's current destructivity value (default: 1)
- `data.actionPoints` (number): The player's available action points (default: 10)
- `data.ws` (WebSocket|null): The WebSocket connection instance (default: null)
- `data.wsConnected` (boolean): Flag indicating WebSocket connection status (default: false)
- `data.heartbeatTimer` (number|null): Interval timer ID for heartbeat ping/pong (default: null)

**Lifecycle Hooks**:
- `mounted()`: Reads `targetNumber` and `decisionTime` from `$route.query` (passed from StartBotGame), then calls `connectWebSocket(targetNumber, decisionTime)`.
- `beforeUnmount()`: Calls `disconnectWebSocket()` to clean up the WebSocket connection and heartbeat timer.

**Methods**:
- `connectWebSocket(targetNumber, decisionTime)`: Builds the WebSocket URL (`ws://localhost:7111/api/game/botPlay`), creates a new WebSocket connection, and sets up event handlers:
  - `onopen`: Sends an initialization message with `player_name`, `player_id`, `target_number`, and `decision_time`; starts a 10-second heartbeat interval.
  - `onmessage`: Parses JSON messages and dispatches them to `handleGameMessage()`. Ignores heartbeat/pong responses.
  - `onerror`: Logs WebSocket errors.
  - `onclose`: Cleans up connection state and clears the heartbeat timer.
- `disconnectWebSocket()`: Closes the WebSocket (code 1000) and clears the heartbeat timer.
- `handleGameMessage(message)`: Processes incoming WebSocket messages based on their `type` (WSResponseTypes enum):
  - `DATA_UPDATE (5)`: Updates game state (`enemy_score`, `player_score`, `action_points`, `productivity`, `destructivity`) from message payload.
  - `PLAYER_TURN_START (7)`, `BOT_TURN_START (6)`, `BOT_TURN_FINISH (9)`, `PLAYER_WIN (10)`, `BOT_WIN (11)`: Logs the event (placeholder handlers for future implementation).
- `handleOperation(operation)`: Sends the player's operation to the backend via WebSocket as a `PLAYER_OPERATION` message. Warns if WebSocket is not connected.

**Template Structure**:
- Renders the `<GameScreen>` component with props (`enemyScore`, `playerScore`, `productivity`, `destructivity`, `actionPoints`) bound to local data
- Listens for the `@operate` event and delegates to `handleOperation()`

**Data Flow**:
1. StartBotGame passes `targetNumber` and `decisionTime` as route query params when navigating to `/botGame`
2. BotGame reads these params in `mounted()` and establishes a WebSocket connection
3. Server sends game state updates via WebSocket messages → BotGame updates reactive data → GameScreen re-renders
4. User clicks an operation button in GameScreen → `@operate` event emitted → BotGame sends operation to server via WebSocket

**Design Principle**: BotGame is the **controller** for Bot game mode. It owns the game state and logic, while GameScreen is a **pure template** that only renders UI. This separation allows GameScreen to be reused by other game modes (PvP, etc.) with completely different logic implementations.

**Integration**: Registered in the Vue Router at `/botGame` route with authentication guard. Uses GameScreen for visual rendering, config for endpoint URLs, userStore for player credentials, and enums for message type constants. Uses `game-screen.css` for styling.

---

## GameScreen Component (`src/components/GameScreen.vue`)

**Purpose**: A pure presentational UI shell shared by multiple game modes (Bot, PvP, etc.). Displays enemy/player scores, action points, a center gamepad icon (fa-solid fa-gamepad), and four operation buttons arranged on the left and right sides. **Has NO internal game logic or state management** — it is a stateless template component.

**Component Properties**:
- `name` (string): 'GameScreen' - Component identifier

**Props**:
- `enemyScore` (Number, default: 0): The current score of the enemy/opponent
- `playerScore` (Number, default: 0): The current score of the player
- `actionPoints` (Number, default: 10): The current action points available

**Emits**:
- `operate(operation)`: Emitted when a game operation button is clicked
  - `operation` (string): The operation identifier ('produce', 'destruct', 'enhanceProductivity', 'enhanceDestructivity')

**Usage Example** (by game mode components like BotGame, PvPGame):
```vue
<GameScreen
  :enemyScore="myEnemyScore"
  :playerScore="myPlayerScore"
  :actionPoints="myActionPoints"
  @operate="handleOperation"
/>
```

**Template Structure**:
- Score section with enemy score (red tint) above, center gamepad icon (fa-solid fa-gamepad), player score below, and AP display
- Operations section with two columns:
  - **Left column**: Produce (fa-solid fa-plus-circle) and Enhance Productivity (fa-solid fa-arrow-up)
  - **Right column**: Destruct (fa-solid fa-minus-circle) and Enhance Destructivity (fa-solid fa-arrow-down)
- Each operation button shows the icon, operation name, and a short description
- Responsive design for desktop, tablet, and mobile layouts

**Styling Features**:
- Black background matching NumGame's color theme
- Cascadia Code monospace font family
- Red gamepad icon with red glow shadow
- Enemy score in red (#ff4444) with glow, player score in white with subtle glow
- AP display with yellow bolt icon (#ffaa00)
- Operation buttons with red border, semi-transparent red background, and hover/active/disabled states
- Hover effect with upward lift (translateY -2px) and red glow box-shadow
- Icon scaling animation on hover
- Responsive breakpoints at 768px and 480px
- On mobile (480px), operations stack vertically in a single column

**Design Principle**: GameScreen is a **pure template** — it manages no data, contains no game logic, and makes no API calls. All data flows in via props, all user actions are emitted as events. Each game mode (Bot, PvP, etc.) creates its own parent component that wraps GameScreen and implements its own independent logic, WebSocket handling, and API calls.

**Integration**: Used by BotGame component (and future game mode components) which passes props and handles the `@operate` event. Routed via `/botGame` through the BotGame component. Uses self-contained CSS module (`game-screen.css`) for styling.

---

## GameScreen Styles (`src/assets/styles/game-screen.css`)

**Purpose**: Defines game-specific UI styles for the GameScreen component. Shared base layout (`.game-screen` full-viewport black background, flex column) is provided by the globally imported `page-layout.css` — this file only contains game-specific styles (score indicators, gamepad icon, AP display, operation buttons).

**Key Classes**:
- `.score-section`: Flex column container for score items, gamepad icon, and AP display
- `.score-row`: Flex row aligning score items horizontally
- `.score-item`: Flex column for label and value pairs
- `.score-label`: Uppercase gray (#aaaaaa) label text for score titles
- `.score-value`: Large (2.5rem) bold score number
- `.score-item--enemy .score-value`: Red (#ff4444) enemy score with red glow
- `.score-item--player .score-value`: White score with subtle white glow
- `.ap-display`: Flex row for action points display with yellow (#ffaa00) bolt icon
- `.gamepad-container .fa-gamepad`: Red (#ff0000) gamepad icon at 4.5rem with red glow shadow
- `.operations-section`: Flex row container for the two operation columns (max-width 700px)
- `.operation-column`: Flex column (50% width, max 250px) for grouping operations
- `.operation-column--left`: Right-aligned column for left-side buttons
- `.operation-column--right`: Left-aligned column for right-side buttons
- `.operation-button`: Custom button (not AppButton) with red border, semi-transparent red background, white text, and hover/active/disabled states
- `.operation-button i`: Red icon inside the operation button with scale animation on hover
- `.operation-label`: Flex column for operation name and description
- `.operation-name`: Bold operation name (0.95rem)
- `.operation-desc`: Small (0.7rem) gray (#999999) description text
- Responsive breakpoints at 768px (smaller fonts/icons/padding) and 480px (single column layout for operations)

**Integration**: Imported by `GameScreen.vue` via `<style scoped src="...">`.


*Last Updated: May 31, 2026*
