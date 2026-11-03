from app import HTTP_ERRORS, HTTP_REQUESTS, HTTP_REQUEST_DURATION


def test_metrics_endpoint_returns_prometheus_text_and_does_not_count_itself(client):
    before = HTTP_REQUESTS.labels("GET", "metrics", "200")._value.get()

    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.content_type.startswith("text/plain")
    assert b"helpdesk_http_requests_total" in response.data
    assert HTTP_REQUESTS.labels("GET", "metrics", "200")._value.get() == before


def test_request_count_and_error_count_include_http_status(client):
    success_before = HTTP_REQUESTS.labels("GET", "login", "200")._value.get()
    missing_before = HTTP_REQUESTS.labels("GET", "unknown", "404")._value.get()
    errors_before = HTTP_ERRORS.labels("GET", "unknown", "404")._value.get()

    success = client.get("/login")
    missing = client.get("/this-route-does-not-exist")

    assert success.status_code == 200
    assert missing.status_code == 404
    assert HTTP_REQUESTS.labels("GET", "login", "200")._value.get() == success_before + 1
    assert HTTP_REQUESTS.labels("GET", "unknown", "404")._value.get() == missing_before + 1
    assert HTTP_ERRORS.labels("GET", "unknown", "404")._value.get() == errors_before + 1


def test_csrf_error_response_is_counted_without_breaking_protection(client):
    errors_before = HTTP_ERRORS.labels("POST", "register", "400")._value.get()

    response = client.post("/register", data={"name": "No token"})

    assert response.status_code == 400
    assert HTTP_ERRORS.labels("POST", "register", "400")._value.get() == errors_before + 1


def test_request_duration_is_observed(client):
    duration = HTTP_REQUEST_DURATION.labels("GET", "login")
    sum_before = duration._sum.get()

    response = client.get("/login")

    assert response.status_code == 200
    assert duration._sum.get() > sum_before
