ENDPOINTS = [
    # Authentication Endpoints
    {
        "method": "POST",
        "url": "/api/auth/login/",
        "data": {
            "username": "johndoe",
            "password": "SecurePass123!"
        },
        "expected_status": 200,
    },
    {
        "method": "GET",
        "url": "/api/auth/profile/",
        "expected_status": 200,
    },
    {
        "method": "PUT",
        "url": "/api/auth/update_profile/",
        "data": {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com"
        },
        "expected_status": 200,
    },
    {
        "method": "PATCH",
        "url": "/api/auth/update_profile/",
        "data": {
            "first_name": "Johnny"
        },
        "expected_status": 200,
    },
    
    # Project Endpoints
    {
        "method": "GET",
        "url": "/api/projects/",
        "expected_status": 200,
    },
    {
        "method": "POST",
        "url": "/api/projects/",
        "data": {
            "title": "{timestamp} Website Redesign",
            "description": "Complete redesign of company website with modern UI/UX",
            "status": "active",
            "due_date": "2024-03-15"
        },
        "expected_status": 201,
        "capture_id": "project_id"  # Capture the ID from response
    },
    {
        "method": "GET",
        "url": "/api/projects/{project_id}/",
        "expected_status": 200,
    },
    {
        "method": "PUT",
        "url": "/api/projects/{project_id}/",
        "data": {
            "title": "{timestamp} Website Redesign - Updated",
            "description": "Complete redesign of company website with modern UI/UX and mobile responsiveness",
            "status": "active",
            "due_date": "2024-04-01"
        },
        "expected_status": 200,
    },
    {
        "method": "PATCH",
        "url": "/api/projects/{project_id}/",
        "data": {
            "status": "completed"
        },
        "expected_status": 200,
    },
    {
        "method": "PATCH",
        "url": "/api/projects/{project_id}/update_status/",
        "data": {
            "status": "completed"
        },
        "expected_status": 200,
    },
    
    # Task Endpoints
    {
        "method": "GET",
        "url": "/api/tasks/",
        "expected_status": 200,
    },
    {
        "method": "POST",
        "url": "/api/tasks/",
        "data": {
            "title": "{timestamp} Design Homepage Layout",
            "description": "Create wireframes and mockups for the new homepage design",
            "project": "{project_id}",  # Use captured project ID
            "status": "todo",
            "priority": "high",
            "due_date": "2024-02-20"
        },
        "expected_status": 201,
        "capture_id": "task_id"  # Capture the task ID
    },
    {
        "method": "GET",
        "url": "/api/tasks/{task_id}/",
        "expected_status": 200,
    },
    {
        "method": "PUT",
        "url": "/api/tasks/{task_id}/",
        "data": {
            "title": "{timestamp} Design Homepage Layout - Revised",
            "description": "Create wireframes and mockups for the new homepage design with client feedback",
            "project": "{project_id}",
            "status": "in_progress",
            "priority": "high",
            "due_date": "2024-02-25"
        },
        "expected_status": 200,
    },
    {
        "method": "PATCH",
        "url": "/api/tasks/{task_id}/",
        "data": {
            "status": "completed",
            "priority": "medium"
        },
        "expected_status": 200,
    },
    {
        "method": "PATCH",
        "url": "/api/tasks/{task_id}/update_status/",
        "data": {
            "status": "in_progress"
        },
        "expected_status": 200,
    },
    {
        "method": "GET",
        "url": "/api/tasks/overdue/",
        "expected_status": 200,
    },
    {
        "method": "DELETE",
        "url": "/api/tasks/{task_id}/",
        "expected_status": 204,
    },
    {
        "method": "DELETE",
        "url": "/api/projects/{project_id}/",
        "expected_status": 204,
    },
]
