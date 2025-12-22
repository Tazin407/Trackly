# Trackly API Documentation

## Overview
Trackly is a task management API built with Django REST Framework. It provides comprehensive project and task management capabilities with user authentication.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses JWT (JSON Web Token) authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <your-access-token-here>
```

Tokens are obtained through login and can be refreshed using the refresh token.

## API Endpoints

### Authentication Endpoints (`/api/auth/`)

#### Register User
- **POST** `/api/auth/register/`
- **Body:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "password_confirm": "string",
    "first_name": "string",
    "last_name": "string"
}
```

#### Login
- **POST** `/api/auth/login/`
- **Body:**
```json
{
    "username": "string",
    "password": "string"
}
```
- **Response:**
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "user": {...},
        "access": "access_token_here",
        "refresh": "refresh_token_here"
    }
}
```

#### Logout
- **POST** `/api/auth/logout/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
    "refresh": "refresh_token_here"
}
```

#### Refresh Token
- **POST** `/api/auth/refresh_token/`
- **Body:**
```json
{
    "refresh": "refresh_token_here"
}
```
- **Response:**
```json
{
    "success": true,
    "message": "Token refreshed successfully",
    "data": {
        "access": "new_access_token_here"
    }
}
```

#### Get Profile
- **GET** `/api/auth/profile/`
- **Headers:** `Authorization: Bearer <access_token>`

#### Update Profile
- **PUT/PATCH** `/api/auth/update_profile/`
- **Headers:** `Authorization: Bearer <access_token>`

### Project Endpoints (`/api/projects/`)

#### List Projects
- **GET** `/api/projects/`
- **Headers:** `Authorization: Bearer <access_token>`

#### Create Project
- **POST** `/api/projects/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
    "title": "string",
    "description": "string",
    "status": "active|completed|archived",
    "due_date": "YYYY-MM-DD"
}
```

#### Get Project
- **GET** `/api/projects/{id}/`
- **Headers:** `Authorization: Bearer <access_token>`

#### Update Project
- **PUT/PATCH** `/api/projects/{id}/`
- **Headers:** `Authorization: Bearer <access_token>`

#### Delete Project
- **DELETE** `/api/projects/{id}/`
- **Headers:** `Authorization: Bearer <access_token>`

#### Update Project Status
- **PATCH** `/api/projects/{id}/update_status/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
    "status": "active|completed|archived"
}
```

### Task Endpoints (`/api/tasks/`)

#### List Tasks
- **GET** `/api/tasks/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Query Parameters:**
  - `project`: Filter by project ID
  - `status`: Filter by status (todo|in_progress|completed)
  - `priority`: Filter by priority (low|medium|high)

#### Create Task
- **POST** `/api/tasks/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
    "title": "string",
    "description": "string",
    "project": "integer",
    "status": "todo|in_progress|completed",
    "priority": "low|medium|high",
    "due_date": "YYYY-MM-DD"
}
```

#### Get Task
- **GET** `/api/tasks/{id}/`
- **Headers:** `Authorization: Bearer <access_token>`

#### Update Task
- **PUT/PATCH** `/api/tasks/{id}/`
- **Headers:** `Authorization: Bearer <access_token>`

#### Delete Task
- **DELETE** `/api/tasks/{id}/`
- **Headers:** `Authorization: Bearer <access_token>`

#### Update Task Status
- **PATCH** `/api/tasks/{id}/update_status/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
    "status": "todo|in_progress|completed"
}
```

#### Get Overdue Tasks
- **GET** `/api/tasks/overdue/`
- **Headers:** `Authorization: Bearer <access_token>`

## Response Format

All API responses follow a consistent format:

### Success Response
```json
{
    "success": true,
    "message": "Operation completed successfully",
    "data": {
        // Response data here
    },
    "count": 10  // For list endpoints
}
```

### Error Response
```json
{
    "success": false,
    "message": "Error description",
    "errors": {
        // Detailed error information
    }
}
```

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Resource deleted successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Pagination

List endpoints support pagination with the following parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

## Error Handling

The API provides comprehensive error handling with detailed error messages and appropriate HTTP status codes. All validation errors are returned with specific field-level error information.

## Security Features

- JWT-based authentication with access and refresh tokens
- Token blacklisting for secure logout
- Access tokens expire in 60 minutes
- Refresh tokens expire in 1 day
- User authorization checks
- Input validation and sanitization
- CORS configuration for cross-origin requests
- Proper error handling without sensitive information exposure