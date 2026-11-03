# ITL704 syllabus mapping

This mapping describes capabilities and evidence present in the repository.
It is not a claim of course approval or of external contribution.

| ITL704 topic | Project evidence | Limits / evidence to add |
| --- | --- | --- |
| Basic open-source concepts | Project-level MIT license, dependency notes, contribution workflow, tests, and version-control documentation. | Confirm project ownership and repository publication choices before public distribution. |
| GPL and open-source licensing | [`open-source-licenses.md`](open-source-licenses.md) explains copyleft, GPL, MIT, Apache 2.0, and dependency-license review. The project itself uses MIT, not GPL. | Review exact versions and notices of all dependencies before release. |
| Contribution to open source | Git-based branch, testing, and pull-request workflow is documented. | No external issue, contribution, pull request, review, or merge evidence is claimed; add actual links if completed. |
| Different operating systems | Windows PowerShell development/setup instructions are provided. A Gunicorn startup script exists for a Linux-style deployment environment. | Windows is the verified local environment for this workspace. The presence of a startup script does not prove deployment testing on Linux, macOS, or other systems. |
| Different technologies | Python, Flask, Flask-SQLAlchemy/SQLAlchemy, SQLite, scikit-learn, Pytest, Prometheus, and Grafana configuration are present. | Prometheus and Grafana executables must be installed separately; their configuration files alone do not prove a running deployment. |
| Network management | Prometheus scrapes HTTP metrics and Grafana configuration visualizes request rate, latency, and errors. | These are application monitoring signals, not a full network-management or SLA-monitoring system. |
| Applications and services | Flask web application supports role-based IT ticket reporting and lifecycle management. | Production operation and service-level claims need deployment and operational evidence. Demo account seeding is disabled by default in the startup module. |

For assessment evidence, capture actual test output, screenshots from a
working local setup, and genuine repository/contribution links. Do not
fabricate any of these artifacts.
