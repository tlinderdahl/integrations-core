# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os

from datadog_checks.base.utils.common import get_docker_hostname
from datadog_checks.gitlab import GitlabCheck

HERE = os.path.dirname(os.path.abspath(__file__))

# Networking
HOST = get_docker_hostname()

GITLAB_TEST_PASSWORD = 'hdkss33jdijb123'
GITLAB_TEST_API_TOKEN = 'token'
GITLAB_LOCAL_PORT = 8086
GITLAB_LOCAL_PROMETHEUS_PORT = 8088

PROMETHEUS_ENDPOINT = "http://{}:{}/metrics".format(HOST, GITLAB_LOCAL_PROMETHEUS_PORT)
GITLAB_PROMETHEUS_ENDPOINT = "http://{}:{}/-/metrics".format(HOST, GITLAB_LOCAL_PORT)
GITLAB_URL = "http://{}:{}".format(HOST, GITLAB_LOCAL_PORT)
GITLAB_TAGS = ['gitlab_host:{}'.format(HOST), 'gitlab_port:{}'.format(GITLAB_LOCAL_PORT)]

CUSTOM_TAGS = ['optional:tag1']

# Note that this is a subset of the ones defined in GitlabCheck
# When we stand up a clean test infrastructure some of those metrics might not
# be available yet, hence we validate a stable subset
ALLOWED_METRICS = [
    'process_max_fds',
    'process_open_fds',
    'process_resident_memory_bytes',
    'process_start_time_seconds',
    'process_virtual_memory_bytes',
]

METRICS = [
    "banzai.cacheless_render_real_duration_seconds.count",
    "banzai.cacheless_render_real_duration_seconds.sum",
    "cache.misses_total",
    "cache.operation_duration_seconds.count",
    "cache.operation_duration_seconds.sum",
    "cache_operations_total",
    "job.waiter_started_total",
    "job.waiter_timeouts_total",
    "rails_queue_duration_seconds.count",
    "rails_queue_duration_seconds.sum",
    "transaction.allocated_memory_bytes.count",
    "transaction.allocated_memory_bytes.sum",
    "transaction.cache_read_hit_count_total",
    "transaction.cache_read_miss_count_total",
    "transaction.duration_seconds.count",
    "transaction.duration_seconds.sum",
    "transaction.new_redis_connections_total",
    "transaction.view_duration_total",
    "transaction.rails_queue_duration_total",
    "rack.http_requests_total",
    "rack.http_request_duration_seconds.sum",
    "rack.http_request_duration_seconds.count",
    "ruby.file_descriptors",
    "ruby.memory_bytes",
    "ruby.sampler_duration_seconds_total",
    "ruby.process_cpu_seconds_total",
    "ruby.process_max_fds",
    "ruby.process_resident_memory_bytes",
    "ruby.process_start_time_seconds",
    "ruby.gc_duration_seconds.count",
    "ruby.gc_duration_seconds.sum",
    "sql_duration_seconds.count",
    "sql_duration_seconds.sum",
    "ruby.gc_stat.count",
    "ruby.gc_stat.heap_allocated_pages",
    "ruby.gc_stat.heap_sorted_length",
    "ruby.gc_stat.heap_allocatable_pages",
    "ruby.gc_stat.heap_available_slots",
    "ruby.gc_stat.heap_live_slots",
    "ruby.gc_stat.heap_free_slots",
    "ruby.gc_stat.heap_final_slots",
    "ruby.gc_stat.heap_marked_slots",
    "ruby.gc_stat.heap_eden_pages",
    "ruby.gc_stat.heap_tomb_pages",
    "ruby.gc_stat.total_allocated_pages",
    "ruby.gc_stat.total_freed_objects",
    "ruby.gc_stat.total_freed_pages",
    "ruby.gc_stat.total_allocated_objects",
    "ruby.gc_stat.malloc_increase_bytes",
    "ruby.gc_stat.malloc_increase_bytes_limit",
    "ruby.gc_stat.minor_gc_count",
    "ruby.gc_stat.major_gc_count",
    "ruby.gc_stat.remembered_wb_unprotected_objects",
    "ruby.gc_stat.remembered_wb_unprotected_objects_limit",
    "ruby.gc_stat.old_objects",
    "ruby.gc_stat.old_objects_limit",
    "ruby.gc_stat.oldmalloc_increase_bytes",
    "ruby.gc_stat.oldmalloc_increase_bytes_limit",
    "unicorn.active_connections",
    "unicorn.queued_connections",
    "unicorn.workers",
]

METRICS_TO_TEST = [
    "puma.workers",
    "rack.http_requests_total",
    "ruby.process_start_time_seconds",
    "rack.http_request_duration_seconds.sum",
    "sql_duration_seconds.sum",
]


def assert_check(aggregator, metrics):
    """
    Basic Test for gitlab integration.
    """
    # Make sure we're receiving gitlab service checks
    for service_check in GitlabCheck.ALLOWED_SERVICE_CHECKS:
        aggregator.assert_service_check(
            'gitlab.{}'.format(service_check), status=GitlabCheck.OK, tags=GITLAB_TAGS + CUSTOM_TAGS
        )

    # Make sure we're receiving prometheus service checks
    aggregator.assert_service_check(
        GitlabCheck.PROMETHEUS_SERVICE_CHECK_NAME, status=GitlabCheck.OK, tags=GITLAB_TAGS + CUSTOM_TAGS
    )

    for metric in metrics:
        aggregator.assert_metric("gitlab.{}".format(metric))
