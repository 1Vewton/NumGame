# NumGame Frontend - Coding Standards and Documentation

## ⚠️ Agent Instructions (Read First)

This file defines coding standards for the NumGame frontend project. As an AI agent working on this project, you **MUST** adhere to the following rules:

### 1. Scope Constraints
- **Only implement the specific features I explicitly ask for.** Do not add extra functionality, refactor existing code, or make improvements beyond what I request.
- If you think something needs to be added or improved, ask me first before implementing it.

### 2. Data Structure & Design Questions
- If you have any questions about **third-party libraries or frameworks** (e.g., Vue.js, axios, Font Awesome), **use DeepWiki's MCP tools** (`cdNP410mcp0ask_question`, `cdNP410mcp0read_wiki_structure`, `cdNP410mcp0read_wiki_contents`) to look up the official repository documentation first.
- If you have any questions about **this project's backend** (e.g., NumGame backend data structures, API endpoints, business logic, component designs), **ask me directly using the `ask_followup_question` tool** — do not use DeepWiki for this project's own backend.
- **Do not make assumptions** about data formats, API contracts, or business logic. Always verify.

### Let's keep the project clean, focused, and exactly what I ask for. Thank you!

---

## Overview

NumGame is a number-based strategy game frontend application built with Vue.js 3. This document outlines the coding standards, documentation requirements, and development workflow for the NumGame frontend project.

### 3. Button Variant Design Principle
- **When a user is allowed to press a button (action is enabled/valid), the button's variant must be `"primary"` (red).**
- **When a user is not allowed to press a button (action is disabled/invalid), the button's variant must be `"secondary"` (gray).**
- This rule applies to all buttons throughout the application where the enabled/disabled state depends on validation or conditions.

---

## Project Structure

```
numgame-frontend/
├── public/                    # Static assets and HTML template
├── src/                      # Source code
│   ├── assets/              # Images and static resources
│   ├── components/          # Vue components
│   │   ├── HelloWorld.vue   # Demo component (to be replaced)
│   │   ├── AppInput.vue     # Reusable white input field component
│   │   ├── AppButton.vue    # Reusable styled button component
│   │   ├── ErrorNotification.vue  # Reusable error toast notification component
│   │   ├── SuccessNotification.vue  # Reusable success toast notification component
│   │   ├── StartScreen.vue  # Welcome screen with login functionality
│   │   └── UserInfo.vue     # User information modal overlay component
│   ├── App.vue              # Root application component
│   ├── main.js             # Application entry point
│   └── utils/              # Utility modules
│       ├── api.js           # API client (axios)
│       ├── config.js        # Environment configuration
│       └── requestBodies.js # API request body templates
├── package.json             # Project configuration and dependencies
├── vue.config.js           # Vue CLI configuration
├── babel.config.js         # Babel configuration
├── jsconfig.json           # JavaScript configuration
├── README.md               # Project setup instructions
└── AGENTS.md              # Coding standards and documentation (this file)
```

## Coding Standards

### 1. Documentation Requirements

#### 1.1 Function Documentation
Every function in the codebase must include comprehensive documentation comments in English. The documentation must follow this format:

```javascript
/**
 * Function description - What this function does
 * 
 * This function [brief description of purpose and behavior].
 * 
 * @function functionName
 * @param {type} paramName - Description of the parameter
 * @param {type} paramName2 - Description of the second parameter
 * @returns {type} Description of the return value
 * @throws {ErrorType} Description of potential errors
 * @example
 * // Example usage
 * const result = functionName(param1, param2);
 */
```

#### 1.2 Module Documentation
Every module must include a header comment explaining its purpose and role in the application:

```javascript
/**
 * Module Name - Module Purpose
 * 
 * This module [description of module's responsibility].
 * It handles [specific functionality] and integrates with [other modules].
 * 
 * @module ModuleName
 */
```

#### 1.3 Component Documentation (Vue.js)
Vue components must include documentation in the script section:

```vue
<script>
/**
 * ComponentName - Component Purpose
 * 
 * This component handles [specific UI/functionality].
 * It displays [content] and responds to [user interactions].
 * 
 * @module ComponentName
 */
export default {
  name: 'ComponentName',
  
  /**
   * Component props - External data passed to the component
   * 
   * @property {type} propName - Description of the prop
   * @property {type} propName2 - Description of the second prop
   */
  props: {
    propName: type,
    propName2: type
  },
  
  // Additional component options with documentation
}
</script>
```

### 2. Code Commenting Standards

#### 2.1 Inline Comments
- Use `//` for single-line comments
- Use `/* */` for multi-line comments
- Comment complex logic and non-obvious code sections
- Avoid commenting obvious code

#### 2.2 File Header Comments
Every source file must start with a header comment:

```javascript
/**
 * filename.js - File Purpose
 * 
 * This file contains [description of file contents].
 * It is responsible for [specific functionality].
 * 
 * @author [Developer Name]
 * @created [Date]
 * @updated [Date]
 */
```

### 3. Function Documentation Examples

#### 3.1 JavaScript Functions

```javascript
/**
 * calculateScore - Calculates the player's score based on game performance
 * 
 * This function computes the final score by combining time remaining,
 * correct answers, and difficulty multiplier.
 * 
 * @function calculateScore
 * @param {number} timeRemaining - Time remaining in seconds
 * @param {number} correctAnswers - Number of correct answers
 * @param {number} difficulty - Difficulty multiplier (1-3)
 * @returns {number} Final calculated score
 * @throws {RangeError} If difficulty is not between 1 and 3
 * @example
 * // Returns 450
 * const score = calculateScore(30, 10, 1.5);
 */
function calculateScore(timeRemaining, correctAnswers, difficulty) {
  if (difficulty < 1 || difficulty > 3) {
    throw new RangeError('Difficulty must be between 1 and 3');
  }
  return timeRemaining * correctAnswers * difficulty;
}
```

#### 3.2 Vue Component Methods

```javascript
methods: {
  /**
   * handleGuess - Processes user's number guess
   * 
   * This method validates the user's guess, checks against the target number,
   * updates game state, and provides feedback to the user.
   * 
   * @method handleGuess
   * @param {number} guessedNumber - The number guessed by the user
   * @returns {boolean} True if guess is correct, false otherwise
   */
  handleGuess(guessedNumber) {
    // Implementation details
  }
}
```

### 4. Module Documentation Requirements

#### 4.1 Core Application Modules

##### Application Entry Point (`src/main.js`)
```javascript
/**
 * main.js - Application Entry Point
 * 
 * This module initializes and mounts the Vue.js application.
 * It serves as the bootstrap point for the entire NumGame frontend.
 * 
 * @module ApplicationEntry
 */
```

##### Root Application Component (`src/App.vue`)
```javascript
/**
 * App.vue - Root Application Component
 * 
 * This component serves as the container for all game components.
 * It manages global layout, routing, and application state.
 * 
 * @module App
 */
```

### 5. Documentation Workflow

#### 5.1 Documenting New Modules
When creating a new module, developers must:

1. **Write the code** with proper function and module documentation
2. **Update AGENTS.md** with the module documentation
3. **Include** the following in AGENTS.md:
   - Module name and purpose
   - Key functions and their parameters
   - Integration points with other modules
   - Any special considerations

#### 5.2 AGENTS.md Update Template
For each new module, add to AGENTS.md:

```
### [Module Name] (`path/to/module.js`)

**Purpose**: Brief description of the module's purpose.

**Functions**:
- `functionName(param1, param2)`: Description of what this function does
  - `param1` (type): Description of parameter 1
  - `param2` (type): Description of parameter 2
  - Returns: Description of return value

**Integration**: How this module integrates with other parts of the application.

**Notes**: Any additional notes or considerations.
```

### 6. File Structure and Naming Conventions

#### 6.1 File Naming
- Vue components: `ComponentName.vue` (PascalCase)
- JavaScript modules: `moduleName.js` (camelCase)
- Utility functions: `utility-name.js` (kebab-case)
- Configuration files: `config-name.js` (kebab-case)

#### 6.2 Directory Structure
- Components: `src/components/`
- Views/Pages: `src/views/`
- Utilities: `src/utils/`
- Services: `src/services/`
- Stores: `src/stores/` (for state management)
  - `userStore.js`: Reactive in-memory user session store

### 7. Development Requirements

#### 7.1 Comment Compliance
All code must include:
- English comments only
- Function documentation with @param tags
- Module headers with @module tags
- Clear descriptions of purpose and behavior

#### 7.2 Documentation Validation
Before committing code, developers must verify:
- All functions have proper documentation
- All modules have header comments
- AGENTS.md is updated with new module information
- Documentation matches actual implementation

### 9. Quality Assurance

#### 9.1 Documentation Review
All code changes must undergo documentation review:
- Verify all functions have @param documentation
- Check module headers include @module tags
- Ensure AGENTS.md is updated with new modules
- Validate examples match actual usage

#### 9.2 Automated Checks
The project includes:
- ESLint rules for JSDoc compliance
- Pre-commit hooks to check documentation
- CI/CD pipeline validation

### 10. Maintenance and Updates

#### 10.1 Documenting Changes
When modifying existing code:
1. Update function documentation if behavior changes
2. Update module documentation if responsibilities change
3. Update AGENTS.md if module interfaces change
4. Add @updated tag with date

#### 10.2 Deprecation
When deprecating functions or modules:
1. Add @deprecated tag with explanation
2. Specify alternative to use
3. Update AGENTS.md with deprecation notice
4. Remove in next major version

---

## AGENTS.md Documentation Entries

### Current Module Documentation

#### Application Entry Point (`src/main.js`)
**Purpose**: Initializes and mounts the Vue.js application.

**Functions**:
- `createApp(App)`: Creates a new Vue application instance with the root App component
  - `App` (Component): The root App component to bootstrap the application
  - Returns: Vue application instance
- `.mount('#app')`: Mounts the application to the DOM
  - `selector` (string): CSS selector for the DOM element ('#app')

**Integration**: Called by the browser to start the application.

#### Root Application Component (`src/App.vue`)
**Purpose**: Serves as the container for all game components.

**Component Properties**:
- `name` (string): 'App' - Component identifier
- `components` (object): Child components registered in this component

**Template Structure**: Main container with logo and HelloWorld component.

**Integration**: Root of the component hierarchy.

#### HelloWorld Component (`src/components/HelloWorld.vue`)
**Purpose**: Demo component that will be replaced with actual game components.

**Component Properties**:
- `name` (string): 'HelloWorld' - Component identifier
- `props.msg` (string): Message to display (passed from parent)

**Template Structure**: Displays message and Vue.js documentation links.

**Notes**: Placeholder for game-specific components.

#### AppInput Component (`src/components/AppInput.vue`)
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

#### AppButton Component (`src/components/AppButton.vue`)
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

#### ErrorNotification Component (`src/components/ErrorNotification.vue`)

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

#### SuccessNotification Component (`src/components/SuccessNotification.vue`)
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

#### StartScreen Component (`src/components/StartScreen.vue`)

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
- User info icon button (fa-circle-user) at the top-right corner (only visible when logged in)
- UserInfo modal overlay (shown when showUserInfo is true)
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

**Integration**: Uses AppInput for login/registration form fields and AppButton for buttons. Uses UserInfo for the user information modal. Uses apiClient and config modules to send login and registration requests. Stores user credentials in the reactive in-memory userStore for the current browser session.

#### UserInfo Component (`src/components/UserInfo.vue`)
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

#### User Store Module (`src/stores/userStore.js`)
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

#### Babel Configuration (`babel.config.js`)

**Purpose**: Configures Babel for JavaScript transpilation.

**Properties**:
- `presets` (Array): Babel preset configurations
  - `'@vue/cli-plugin-babel/preset'`: Vue CLI's default Babel preset

**Integration**: Used during build process for browser compatibility.

#### Vue CLI Configuration (`vue.config.js`)
**Purpose**: Customizes Vue CLI build settings and dev server options.

**Properties**:
- `transpileDependencies` (boolean): Enable transpilation of dependencies

**Integration**: Configures the Vue CLI build system.

#### Configuration Module (`src/utils/config.js`)
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
- `getRegisterUrl()`: Returns complete URL for user registration (backend URL + endpoint path)
  - Returns: {string} Complete URL for user registration
- `getLoginUrl()`: Returns complete URL for user login (backend URL + endpoint path)
  - Returns: {string} Complete URL for user login
- `getAutoLoginUrl()`: Returns complete URL for user auto-login (backend URL + endpoint path)
  - Returns: {string} Complete URL for user auto-login
- `getUserUrl()`: Returns complete URL for user information (backend URL + endpoint path)
  - Returns: {string} Complete URL for user information
- `getAllConfig()`: Returns all configuration values as a plain object including endpoints and full URLs
  - Returns: {Object} Object containing all configuration values (backendUrl, registerEndpoint, loginEndpoint, autoLoginEndpoint, userEndpoint, registerUrl, loginUrl, autoLoginUrl, userUrl)
- `validateConfig()`: Validates that all required configuration values are present and valid, including backend URL format and endpoint path validation
  - Throws: {Error} If required configuration values are missing or invalid
  - Returns: {boolean} True if all configuration values are valid

**Integration**: Used by other modules to access configuration values including backend URL and user authentication endpoints.

#### API Client Module (`src/utils/api.js`)
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

#### Request Bodies Module (`src/utils/requestBodies.js`)
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

#### Error Handler Module (`src/utils/errorHandler.js`)
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

*Last Updated: May 24, 2026*

*Version: 1.0.0*  
*All documentation must be maintained in English as per project requirements.*
