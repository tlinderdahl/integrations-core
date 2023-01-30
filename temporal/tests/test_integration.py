# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.temporal import TemporalCheck

from .common import METRICS, TAGS

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures("dd_environment")]


def test_check(dd_run_check, aggregator, check):
    dd_run_check(check)

    for expected_metric in METRICS:
        aggregator.assert_metric(
            name=f"temporal.server.{expected_metric['name']}",
            metric_type=expected_metric.get("type", aggregator.GAUGE),
            tags=expected_metric.get("tags", TAGS),
        )

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_service_checks(dd_run_check, aggregator, check):
    dd_run_check(check)
    aggregator.assert_service_check('temporal.server.openmetrics.health', TemporalCheck.OK, tags=TAGS)
