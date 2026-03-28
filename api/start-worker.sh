#!/bin/sh
set -e

exec taskiq worker taskiq_broker:broker tasks
