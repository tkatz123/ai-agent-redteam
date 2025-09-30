# src/utils/retry.py
from __future__ import annotations
import time
from typing import Callable, Type, Iterable, Any, Tuple

def retry(fn: Callable[[], Any],
          attempts: int = 3,
          backoff_sec: float = 0.5,
          retry_on: Tuple[Type[BaseException], ...] = (Exception,)) -> Any:
    last = None
    for i in range(attempts):
        try:
            return fn()
        except retry_on as e:
            last = e
            if i == attempts - 1:
                raise
            time.sleep(backoff_sec * (2 ** i))
    if last:
        raise last
