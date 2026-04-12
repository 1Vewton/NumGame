# NumGame Backend

## API Functionality Explanation

This document describes the RESTful API endpoints provided by the NumGame backend server.

### User Management

The User Management API handles user registration, authentication, and information retrieval. All user-related endpoints are prefixed with `/user`.

#### Endpoints Overview

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| POST | `/user/userRegister` | Register a new user account | 5 requests per minute |
| POST | `/user/userLogin` | Login and obtain session token | None |
| GET | `/user/autoLogin` | Auto-login using cookie token | None |
| POST | `/user/userInfo` | Get detailed user information | None |

---

### POST /user/userRegister

**Description**: Register a new user account with a unique username.

**Request Body**:
```json
{
  "player_name": "username"
}
```

**Constraints**:
- `player_name` must be between 3 and 100 characters

**Success Response (201 Created)**:
```json
{
  "success": true,
  "user_name": "username",
  "user_id": "generated-uuid-string"
}
```

**Error Responses**:
- **409 Conflict**: Username already exists
```json
{
  "success": false,
  "reason": "Username already exists"
}
```

- **500 Internal Server Error**: Server error during registration
```json
{
  "success": false,
  "reason": "error message"
}
```

**Notes**:
- Rate limited to 5 requests per minute per IP address
- Usernames are case-sensitive and must be unique

---

### POST /user/userLogin

**Description**: Authenticate a user and establish a login session.

**Request Body**:
```json
{
  "player_name": "username"
}
```

**Constraints**:
- `player_name` must be between 3 and 100 characters
- Cannot login with bot accounts (system restriction)

**Success Response (200 OK)**:
```json
{
  "success": true,
  "user_name": "username",
  "user_id": "user-uuid-string"
}
```

**Response Headers**:
- Sets HTTP-only cookie: `login_token=session-token-value`

**Error Responses**:
- **401 Unauthorized**: Username does not exist
```json
{
  "success": false,
  "reason": "Username does not exist"
}
```

- **403 Forbidden**: Attempt to login with bot account
```json
{
  "success": false,
  "reason": "You cannot log in the system with bot account!"
}
```

- **500 Internal Server Error**: Server error during login
```json
{
  "success": false,
  "reason": "error message"
}
```

**Notes**:
- Successful login generates a session token stored in Redis
- Token is returned as an HTTP-only cookie for security
- Token is used for subsequent authenticated requests

---

### GET /user/autoLogin

**Description**: Automatically authenticate user using existing session token from cookies.

**Request Headers**:
- Cookie: `login_token=session-token-value` (required)

**Success Response (200 OK)**:
```json
{
  "success": true,
  "user_name": "username",
  "user_id": "user-uuid-string"
}
```

**Response Headers**:
- Refreshes cookie with same `login_token` value

**Error Responses**:
- **401 Unauthorized**: Session expired, invalid token, or user not found
```json
{
  "success": false,
  "reason": "Session expired or invalid"
}
```
```json
{
  "success": false,
  "reason": "User id not found"
}
```

- **403 Forbidden**: Attempt to auto-login with bot account
```json
{
  "success": false,
  "reason": "You cannot log in the system with bot account!"
}
```

- **500 Internal Server Error**: Server error during auto-login
```json
{
  "success": false,
  "reason": "error message"
}
```

**Notes**:
- Requires `login_token` cookie from previous successful login
- Validates token against Redis store
- Refreshes cookie to extend session

---

### POST /user/userInfo

**Description**: Retrieve detailed information about the authenticated user.

**Request Headers**:
- Cookie: `login_token=session-token-value` (required)

**Request Body**:
```json
{
  "player_name": "username",
  "player_id": "user-uuid-string"
}
```

**Constraints**:
- Both `player_name` and `player_id` must match the authenticated user
- Token must be valid and not expired

**Success Response (200 OK)**:
```json
{
  "success": true,
  "result": {
    "id": "user-uuid-string",
    "user_name": "username",
    "registered_at": 1672531200.0,
    "wins": 5,
    "total_games": 10,
    "is_bot": false
  }
}
```

**Error Responses**:
- **401 Unauthorized**: Not logged in, session expired, or user mismatch
```json
{
  "success": false,
  "reason": "Please login first"
}
```
```json
{
  "success": false,
  "reason": "Session expired or invalid"
}
```
```json
{
  "success": false,
  "reason": "User not found or conflict with your cookie"
}
```

- **500 Internal Server Error**: Server error during info retrieval
```json
{
  "success": false,
  "reason": "error message"
}
```

**Notes**:
- Requires valid authentication token
- Returns full user record including statistics
- `registered_at` field is Unix timestamp (seconds since epoch)
- `is_bot` indicates whether the account is a bot account

---

## Data Models

### Player Data Model

The `players` table in the database contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | String(100) | Unique UUID identifier (primary key) |
| `user_name` | String(100) | Unique username |
| `registered_at` | DateTime | Registration timestamp |
| `wins` | Integer | Number of games won (default: 0) |
| `total_games` | Integer | Total games played (default: 0) |
| `is_bot` | Boolean | Whether account is a bot (default: false) |

### Request Body Schemas

All request bodies use Pydantic models with validation:

**NewPlayerData** (for registration):
```python
{
  "player_name": str  # 3-100 characters
}
```

**LoginPlayerData** (for login):
```python
{
  "player_name": str  # 3-100 characters
}
```

**PlayerData** (for user info):
```python
{
  "player_name": str,  # 3-100 characters
  "player_id": str     # 3-100 characters
}
```

---

## Authentication Flow

1. **Registration**: User creates account → receives user_id
2. **Login**: User provides username → receives session token cookie
3. **Auto-login**: Browser sends token cookie → server validates → returns user info
4. **Authenticated requests**: Include token cookie → server validates → processes request

## Session Management

- Session tokens are stored in Redis with user_id mapping
- Tokens are HTTP-only cookies for security
- No explicit logout endpoint (token expiration managed by Redis TTL)
- All authenticated endpoints validate token against Redis

## Error Handling

All API endpoints follow a consistent error response pattern:
- `success`: boolean indicating operation status
- `reason`: string describing error (present only when `success` is false)
- Appropriate HTTP status codes (4xx for client errors, 5xx for server errors)

## Rate Limiting

- Registration endpoint limited to 5 requests per minute per IP
- Other endpoints currently have no rate limits