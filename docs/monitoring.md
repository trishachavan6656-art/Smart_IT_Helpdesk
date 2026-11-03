# Monitoring

## Components and workflow

The Flask application exposes Prometheus-format HTTP metrics at `GET /metrics`.
The included `monitoring/prometheus.yml` scrapes `localhost:5000` every
15 seconds under the `smart-it-helpdesk` job. Prometheus stores its own time
series; it does not write monitoring data into the helpdesk database.

Configure Grafana with the Prometheus server as a data source, then import
[`monitoring/grafana/smart-it-helpdesk-dashboard.json`](../monitoring/grafana/smart-it-helpdesk-dashboard.json).
The dashboard visualizes HTTP error rate, 95th-percentile request duration,
and request rate by method, route endpoint, and status.

## Local Windows setup

1. Start the helpdesk from the project directory with `python app.py`, then
   check <http://127.0.0.1:5000/metrics> for Prometheus text output.
2. Download and extract the Windows Prometheus release from
   <https://prometheus.io/download/>. From the project directory, point it at
   the included configuration (adjust the executable path if needed):

   ```powershell
   $prometheus = "C:\tools\prometheus\prometheus.exe"
   & $prometheus --config.file="$PWD\monitoring\prometheus.yml"
   ```

3. Open <http://localhost:9090/targets> and confirm the `smart-it-helpdesk`
   target is **UP**. The target uses `localhost:5000`, so Prometheus must be
   able to reach the application at that address.
4. Install and start Grafana using its
   [Windows installation guide](https://grafana.com/docs/grafana/latest/setup-grafana/installation/windows/),
   then open <http://localhost:3000/>.
5. Add a Prometheus data source with URL `http://localhost:9090`, save it,
   and import
   [`monitoring/grafana/smart-it-helpdesk-dashboard.json`](../monitoring/grafana/smart-it-helpdesk-dashboard.json).
   Select the created Prometheus data source when prompted.
6. Generate application traffic and wait for multiple 15-second scrapes before
   expecting rate graphs to show data. Prometheus and Grafana must be installed
   and run separately; the repository only supplies their configuration.

## Application metrics

- `helpdesk_http_requests_total`: responses counted by method, Flask endpoint,
  and HTTP status.
- `helpdesk_http_errors_total`: responses with status 400 or above, using the
  same bounded labels.
- `helpdesk_http_request_duration_seconds`: request-duration histogram by
  method and endpoint.

Scraping `/metrics` does not count the scrape itself. Labels use Flask route
names rather than raw paths or ticket IDs, avoiding unbounded
user-controlled label values. The metrics do not measure ticket SLA
compliance or business outcomes.

## Security and operations

The endpoint is intentionally unauthenticated for Prometheus scraping. Keep
it on a trusted network or restrict access through deployment networking,
firewalls, or a suitably configured reverse proxy. The supplied target is for
local development; update it to a reachable application host when the
components run on different machines. Metrics are useful for noticing
availability, latency, and error-rate changes, but do not replace application
logs, alerting rules, or incident response.
