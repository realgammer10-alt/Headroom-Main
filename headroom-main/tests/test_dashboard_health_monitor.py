from __future__ import annotations

from headroom.dashboard import get_dashboard_html


def test_dashboard_polls_readiness_separately_from_savings_stats() -> None:
    html = get_dashboard_html()

    assert "fetch('/readyz', { cache: 'no-store' })" in html
    assert "fetch('/health')" not in html
    assert "Promise.all([this.fetchStats(), this.fetchHealth()])" in html
    assert "this.healthStatus = 'unavailable'" in html
    assert "this.healthFetchInFlight = true;" in html
    assert "this.healthFetchInFlight = false;" in html
    assert "response.status === 503 || health.status === 'unhealthy'" in html
    stats_fetch = html.split("async fetchStats()", 1)[1].split(
        "async fetchHealth()", 1
    )[0]
    assert "healthStatus" not in stats_fetch


def test_dashboard_shows_component_readiness_and_probe_freshness() -> None:
    html = get_dashboard_html()

    assert "Service Health" in html
    assert "Object.entries(healthChecks)" in html
    assert "healthCheckLabel(check)" in html
    assert "healthUpdatedAt" in html
    assert "formatUptime()" in html
    assert "Health details are unavailable. The dashboard will retry automatically." in html
