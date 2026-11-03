# Testing

## Strategy

The project uses Pytest with an in-memory SQLite database. The shared fixtures
create a small deterministic set of users and tickets for each test, then
remove that test database. Tests do not require or intentionally modify the
local `instance/helpdesk.db`.

Run the complete tracked test suite from the directory containing `app.py`:

```powershell
python -m pytest -q -p no:cacheprovider tests
```

If the machine's default temporary directory is inaccessible, select a
writable temporary directory with Pytest's `--basetemp` option.

## Coverage areas

- **Authentication:** login success/failure, registration, CSRF-protected
  POST-only logout, and safe post-login redirects.
- **Authorization:** employee ticket ownership, engineer-only actions,
  administrator reports and role management.
- **CSRF:** POST requests without a valid token are rejected.
- **Ticket workflow:** create, assign, change status, add troubleshooting and
  comments, resolve, close, and reopen tickets.
- **Search and filters:** ticket query, category, priority, and engineer queue
  scope.
- **Metrics:** Prometheus output, request/error counts, response durations,
  and counting CSRF errors without bypassing protection.
- **ML:** category labels match supported application values, example
  predictions map to supported categories, and evaluation metrics are
  calculated from cross-validated predictions.
- **Configuration:** local secret persistence.
- **Session cookies:** HTTP-only and same-site defaults; secure cookies can
  be enabled for HTTPS deployments with `SESSION_COOKIE_SECURE=1`.
- **Startup:** `render_start.py` does not seed predictable demo accounts
  unless `SEED_DEMO_DATA=1` is explicitly enabled.

These automated tests cover application behavior but are not a substitute for
manual browser/accessibility checks, deployment testing, or a security audit.
