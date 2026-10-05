# SIWES Placement & Organization Management

Placement Management module for the Group 29 SIWES Management System.

## Features

- Add and view SIWES organizations/companies
- Store organization address and contact details
- Create student placement records
- Assign organization to a student
- Store supervisor ID
- Store placement start/end dates
- Track placement status:
  - Pending
  - Active
  - Completed
  - Cancelled
- Update placement status
- Delete placement records

## Files

```text
placement/
└── placement_module.py
```

## Temporary database connection

The module currently contains a small compatibility `get_connection()` function
so it can be tested independently.

When the group leader provides the central `database.py`, replace the temporary
connection with the team's shared function:

```python
from database import get_connection
```

Do NOT keep a separate permanent database in the final integrated project.

## Integration

From the main application:

```python
from placement.placement_module import open_placement

# Example:
open_placement(root, student_id=current_user_id)
```

The exact dashboard command should be adapted to the team's existing
authentication/session variables.

## Important

The final integrated version must use the team's central `SIWES.db`
connection and existing student/supervisor table structures.
