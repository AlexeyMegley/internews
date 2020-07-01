#!/bin/bash
set -e

celery -A internews_web worker -l info & celery -A internews_web beat -l info -s /tmp/celery --pidfile /tmp/celerybeat.pid & tail -f /dev/null