# Smart IT Helpdesk

A role-based Flask application for reporting and managing IT support tickets.
Employees submit and track requests, engineers triage and resolve them, and
administrators review activity and manage account roles.

## Problem statement

IT requests can be difficult to track when they arrive through informal
channels. This project provides a shared ticket workflow with ownership,
prioritization, status history, troubleshooting notes, and response-time
visibility.

## Objectives

- Demonstrate a practical open-source web application using Python and Flask.
- Preserve a complete ticket lifecycle and role-based access.
- Practice relational data modeling, input validation, testing, and monitoring.
- Explore a small machine-learning category suggestion without hiding its
  limitations.

## Features

- Employee, engineer, and administrator dashboards and access boundaries.
- Ticket creation, assignment, comments, troubleshooting, resolution, closure,
  reopening, and an activity timeline.
- Search, category/priority/status filters, engineer scope filters, and sorting.
- Response and resolution timing plus priority-based response targets.
- Responsive interface, keyboard-accessible navigation, accessible labels,
  and empty states.
- Optional TF-IDF / Logistic Regression category suggestions, which users can
  review or override.
- Prometheus request, error, and latency metrics with a Grafana dashboard
  configuration.

## User roles

| Role | Main capabilities |
| --- | --- |
| Employee | Create tickets and view, search, comment on, and reopen their own requests. |
| Engineer | View and filter the shared queue; assign, update, troubleshoot, resolve, close, and reopen tickets. |
| Admin | View system-wide tickets, dashboards, reports, and users; manage other users' roles. |

Authorization is enforced by Flask routes, not just by navigation visibility.
Public registration creates employee accounts; administrator provisioning is
performed locally with `create_admin.py`.

## Technology stack

| Technology | Purpose | Open-source role / use in this project |
| --- | --- | --- |
| Flask | Web framework and routes | Open-source application framework. |
| Flask-SQLAlchemy / SQLAlchemy | ORM and database access | Open-source persistence layer. |
| SQLite | Default local relational database | Open-source, embedded storage; no server needed locally. |
| scikit-learn | Ticket category suggestion | Open-source TF-IDF and Logistic Regression implementation. |
| Pytest | Automated tests | Open-source test framework. |
| `prometheus-client` | Application instrumentation | Exposes request metrics for Prometheus. |
| Prometheus | Metrics collection | External service configured in `monitoring/prometheus.yml`. |
| Grafana | Metrics visualization | External service; dashboard JSON is included. |
| Git | Version control | The repository contains Git history and supports branch-based work. |
| GitHub workflow | Collaboration | Pull-request process is documented; hosting and external contribution evidence must be verified separately. |
| Bootstrap 5, Jinja, CSS, JavaScript | Presentation | Bootstrap is loaded from a CDN; Jinja is Flask's template engine; custom styles and progressive enhancements are local. |

The requirements also include Gunicorn and the Psycopg PostgreSQL driver for
deployment scenarios. Prometheus, Grafana, and their data are not Python
dependencies.

### Third-party dependency licensing

This project's MIT license applies to project code, not to third-party
dependencies. Each direct and transitive dependency, CDN asset, and external
service remains governed by its own license and terms. Review package
metadata, upstream license files, and required notices for the exact versions
before redistribution; this README does not claim that all dependencies use
MIT.

## Architecture

The browser uses Flask-rendered Jinja templates. Flask routes authenticate
users, validate input, enforce roles, and use Flask-SQLAlchemy to access the
database. The ticket suggestion endpoint calls the local classifier. The
Prometheus client exposes HTTP metrics for Prometheus to scrape; Grafana reads
those measurements from Prometheus.

See [architecture](docs/architecture.md) and [database](docs/database.md) for
diagrams and implementation details.

## Machine-learning classifier

The classifier uses TF-IDF features and Logistic Regression trained on 19
short, hand-written examples across seven categories. It only suggests a
category; users retain the manual selection. The checked-in data is
illustrative, very small, and not a production training or validation set.

Run its reproducible two-fold stratified evaluation with:

```powershell
python ml_classifier.py
```

On the current 19 examples, the script reports **0.000 accuracy and 0.000
macro precision, recall, and F1**. This poor result is reported as measured,
not hidden; it shows that this sample model should not be relied on for
automatic routing. See [ML classifier notes](docs/ml-classifier.md) for
preprocessing, dataset, method, and limitations.

## Monitoring

`GET /metrics` exposes request totals, HTTP error totals, and request-duration
histograms. The supplied Prometheus config scrapes the local app every
15 seconds. The Grafana dashboard visualizes error rate, 95th-percentile
latency, and request rate. These are HTTP service metrics, not ticket SLA
measurements. See [monitoring documentation](docs/monitoring.md) for setup and
network safety guidance.

## Testing

The Pytest suite uses in-memory SQLite fixtures and covers authentication,
authorization, CSRF, ticket workflows, search and filters, metrics,
configuration, and ML category/evaluation behavior.

From the project directory:

```powershell
python -m pytest -q -p no:cacheprovider tests
```

See [testing documentation](docs/testing.md) for the strategy and coverage
areas.

## Installation

The verified local setup instructions are for Windows PowerShell. From the
directory containing `app.py`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python init_db.py
```

`init_db.py` creates missing tables and adds sample records only when there
are no users or tickets. It does **not** reset or replace existing records.
For an empty schema without sample data:

```powershell
python init_db.py --no-seed
```

Provision an administrator interactively; the password is not echoed:

```powershell
python create_admin.py
```

Do not use demo/sample accounts or their passwords in a public deployment.
Create unique credentials and replace any sample data before exposing an
instance. Existing databases are not changed automatically; rotate or
disable any sample-account passwords already present before public exposure.

## Configuration

- `SECRET_KEY`: set a long, random value for deployments. Local runs create a
  persistent ignored secret in `instance/.flask_secret` if this variable is
  not set. Protect the deployment secret and use HTTPS in production.
- `SESSION_COOKIE_SECURE`: set to `1` for HTTPS deployments. It defaults to
  disabled for local HTTP development; HTTP-only and `SameSite=Lax` are
  enabled.
- `SEED_DEMO_DATA`: only set to `1` when starting an isolated local demo
  through `render_start.py`. The startup module creates missing tables but
  does not seed predictable demo accounts by default. Never enable demo
  seeding for a public or production database.
- `DATABASE_URL`: optional SQLAlchemy database URL. The default is
  `instance/helpdesk.db`; PostgreSQL support is available through the
  included Psycopg driver.
- `FLASK_DEBUG`: debug mode is disabled by default. Set to `1`, `true`, or
  `yes` only for local development; never expose the debugger in production.

For detailed Prometheus/Grafana setup, see [monitoring documentation](docs/monitoring.md).

## Run locally

With the virtual environment active and the database initialized:

```powershell
python app.py
```

Open <http://127.0.0.1:5000>. To try the metrics endpoint, visit
<http://127.0.0.1:5000/metrics>. The metrics endpoint is unauthenticated for
scraping; restrict its network exposure in deployed environments.

## Project structure

```text
app.py                 Flask routes, validation, authorization, metrics
models.py              User, Ticket, and ActivityLog models
config.py              Database and runtime configuration
init_db.py             Additive schema creation and optional empty-DB seed
create_admin.py        Interactive administrator provisioning
ml_classifier.py       Category prediction and reproducible evaluation
render_start.py        Gunicorn/PaaS startup initialization
templates/             Jinja pages and reusable UI components
static/css/style.css   Responsive application design system
static/js/main.js      Navigation and progressive enhancements
monitoring/            Prometheus and Grafana configuration
tests/                 Pytest application, configuration, metrics, and ML tests
docs/                  Project, contribution, testing, and syllabus documentation
LICENSE                MIT license for the project code
```

## Open-source contribution workflow

Contributions should use a focused branch, include or update tests, and be
submitted as a reviewable Pull Request. The documented workflow is a plan;
this repository does not claim any external issue, contribution, review, or
merge unless actual links are recorded.

See [open-source contribution guide](docs/open-source-contribution.md).

## License

Project code is distributed under the MIT License; see [LICENSE](LICENSE).
The generic copyright-holder wording should be confirmed by the project owner
before public release. Third-party dependencies retain their own licenses.
See [open-source license notes](docs/open-source-licenses.md).

## ITL704 syllabus mapping

The project documents its evidence for open-source concepts, license study,
Git workflow, tested operating-system scope, technologies, application
monitoring, and IT service functionality. See
[ITL704 syllabus mapping](docs/itl704-mapping.md). It does not claim a GPL
project license or an external open-source contribution.

## Future scope

- Grow and independently validate the classifier dataset before relying on
  model predictions.
- Add database migrations and paginated ticket lists.
- Add deployment-specific monitoring targets, alerting, and operational
  runbooks.
- Collect genuine screenshots, deployment evidence, and external contribution
  links where applicable.
