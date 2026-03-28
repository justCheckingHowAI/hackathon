from __future__ import annotations

import os

from taskiq_redis import ListQueueBroker


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

broker = ListQueueBroker(url=REDIS_URL)
