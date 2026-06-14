# NumGame Frontend - Coding Standards and Documentation

## ⚠️ Agent Instructions (Read First)

This file defines coding standards for the NumGame frontend project. As an AI agent working on this project, you **MUST** adhere to the following rules:

### 1. Scope Constraints
- **Only implement the specific features I explicitly ask for.** Do not add extra functionality, refactor existing code, or make improvements beyond what I request.
- If you think something needs to be added or improved, ask me first before implementing it.
- **After finishing any new feature, module, or API integration, you must immediately update DOCUMENT.md with the corresponding documentation.** This includes documenting new enums, utility functions, components, services, stores, and any changes to existing module interfaces. Do not mark the task as complete without ensuring DOCUMENT.md is up to date.

### 2. Data Structure & Design Questions
- If you have any questions about **third-party libraries or frameworks** (e.g., Vue.js, axios, Font Awesome), **use DeepWiki's MCP tools** (`cdNP410mcp0ask_question`, `cdNP410mcp0read_wiki_structure`, `cdNP410mcp0read_wiki_contents`) to look up the official repository documentation first.
- If you have any questions about **this project's backend** (e.g., NumGame backend data structures, API endpoints, business logic, component designs), **ask me directly using the `ask_followup_question` tool** — do not use DeepWiki for this project's own backend.
- **Do not make assumptions** about data formats, API contracts, or business logic. Always verify.

### 3. Need Module Documentation?
- **If you need to understand a component, utility module, or configuration file**, read **[DOCUMENT.md](./DOCUMENT.md)** first — it contains detailed documentation for every module in the project.
- When creating a new module, add its documentation to **DOCUMENT.md**, not AGENTS.md.

### 4. Language Standard
- **All game user-facing copy/text must be in English.** This includes UI labels, button text, subtitles, tooltips, error messages, notifications, and any other text displayed to the user within the game interface.
- Comments and code documentation in source files should also be in English.

### Let's keep the project clean, focused, and exactly what I ask for. Thank you!

---

## Overview

NumGame is a number-based strategy game frontend application built with Vue.js 3. This document outlines the coding standards, documentation requirements, and development workflow for the NumGame frontend project.

### Button Variant Design Principle
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
│   │   ├── StartBotGame.vue # Bot game setup screen
│   │   └── UserInfo.vue     # User information modal overlay component
│   ├── App.vue              # Root application component
│   ├── main.js             # Application entry point
│   ├── router/             # Vue Router configuration
│   │   └── index.js        # Router setup with route definitions
│   └── utils/              # Utility modules
│       ├── api.js           # API client (axios)
│       ├── config.js        # Environment configuration
│       ├── enums.js         # Application enumeration constants
│       └── requestBodies.js # API request body templates
├── DOCUMENT.md              # Detailed module documentation (see this for component/util docs)
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

> 📖 For detailed documentation of each module (components, utilities, configs, stores, etc.), see **[DOCUMENT.md](./DOCUMENT.md)**.

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
2. **Update DOCUMENT.md** with the module documentation
3. **Include** the following in DOCUMENT.md:
   - Module name and purpose
   - Key functions and their parameters
   - Integration points with other modules
   - Any special considerations

#### 5.2 DOCUMENT.md Update Template
For each new module, add to DOCUMENT.md:

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
- Router: `src/router/` (for Vue Router configuration)
  - `index.js`: Vue Router setup with route definitions
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
- DOCUMENT.md is updated with new module information
- Documentation matches actual implementation

### 9. Quality Assurance

#### 9.1 Documentation Review
All code changes must undergo documentation review:
- Verify all functions have @param documentation
- Check module headers include @module tags
- Ensure DOCUMENT.md is updated with new modules
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
3. Update DOCUMENT.md if module interfaces change
4. Add @updated tag with date

#### 10.2 Deprecation
When deprecating functions or modules:
1. Add @deprecated tag with explanation
2. Specify alternative to use
3. Update DOCUMENT.md with deprecation notice
4. Remove in next major version

---

*Last Updated: May 26, 2026*

*Version: 1.1.0*  
*All documentation must be maintained in English as per project requirements.*
