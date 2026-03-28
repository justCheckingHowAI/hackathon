#!/bin/sh
set -e

alembic upgrade head
exec taskiq worker taskiq_broker:broker tasks
