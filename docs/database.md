# Database

The schema is defined in `models.py`. SQLAlchemy's `db.create_all()` is used
to create missing tables; it is not a schema migration system. The project
does not automatically drop tables or reset existing rows. The default local
database is `instance/helpdesk.db`, while tests use in-memory SQLite.

## Entity relationships

```mermaid
erDiagram
    USER ||--o{ TICKET : reports
    USER o|--o{ TICKET : assigned_to
    TICKET ||--o{ ACTIVITY_LOG : records
    USER ||--o{ ACTIVITY_LOG : performs
    USER {
        int id PK
        string name
        string email UK
        string password_hash
        string role
        string department
        string employee_code UK
        datetime created_at
    }
    TICKET {
        int id PK
        string ticket_number UK
        string title
        text description
        string category
        string priority
        string status
        int reported_by_id FK
        int assigned_to_id FK
        datetime created_at
        datetime updated_at
        datetime assigned_at
        datetime resolved_at
        datetime closed_at
        text troubleshooting
        text resolution_notes
    }
    ACTIVITY_LOG {
        int id PK
        int ticket_id FK
        int user_id FK
        string action
        text details
        datetime timestamp
    }
```

## Models and values

- **User (`ticket_user`):** account identity, unique email, Werkzeug password
  hash, department, optional unique employee code, and role.
- **Ticket (`ticket`):** unique human-readable ticket number, subject and
  description, category, priority, lifecycle status, reporter and optional
  engineer foreign keys, lifecycle timestamps, and optional troubleshooting
  and resolution notes.
- **ActivityLog (`activity_log`):** ticket and actor foreign keys, action,
  optional details, and timestamp. Ticket activity is ordered chronologically
  by the model relationship; the detail page renders it newest first.

Allowed roles: `employee`, `engineer`, `admin`.

Allowed categories: `Hardware`, `Software`, `Network`, `Printer`,
`Account/Login`, `Security`, `Other`.

Allowed priorities: `Low`, `Medium`, `High`, `Critical`.

Allowed statuses: `Open`, `Assigned`, `In Progress`, `Resolved`, `Closed`.
`Open`, `Assigned`, and `In Progress` are treated as active statuses.

The application does not currently have a dedicated migration tool. Back up
data before manually changing a deployed schema.
