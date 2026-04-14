# NumGame Frontend - Coding Standards and Documentation

## Overview

NumGame is a number-based strategy game frontend application built with Vue.js 3. This document outlines the coding standards, documentation requirements, and development workflow for the NumGame frontend project.

## Project Structure

```
numgame-frontend/
├── public/                    # Static assets and HTML template
├── src/                      # Source code
│   ├── assets/              # Images and static resources
│   ├── components/          # Vue components
│   │   └── HelloWorld.vue   # Demo component (to be replaced)
│   ├── App.vue              # Root application component
│   └── main.js             # Application entry point
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

#### StartScreen Component (`src/components/StartScreen.vue`)
**Purpose**: Displays the welcome screen for the NumGame application with red and black color theme.

**Component Properties**:
- `name` (string): 'StartScreen' - Component identifier
- `mounted()`: Lifecycle hook that logs when component is mounted

**Template Structure**: 
- Main container with black background
- Red X-mark icon using Font Awesome
- Welcome title with red gradient text
- Subtitle for game description
- Responsive design for different screen sizes

**Styling Features**:
- Red and black color theme
- Cascadia Code font family
- Responsive layout with content positioned higher for future functionality
- Red X-mark icon without background decoration
- Gradient text effects for welcome message

**Integration**: Used as the main welcome screen, mounted by the root App component.

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
- `getAutoLoginEndpoint()`: Retrieves the user auto-login endpoint path from VUE_APP_LOGOUT_ENDPOINT
  - Returns: {string} The user auto-login endpoint path (default: '/api/user/autoLogin')
  - Note: Despite environment variable name, used for auto-login functionality
- `getUserEndpoint()`: Retrieves the user information endpoint path from VUE_APP_USER_ENDPOINT
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

---

*Last Updated: April 14, 2026*  
*Version: 1.0.0*  
*All documentation must be maintained in English as per project requirements.*
