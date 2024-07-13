import logging
import os
from typing import Any, Callable

TRACE = 5
logging.addLevelName(TRACE, "TRACE")


def trace(self: logging.Logger, message: str, *args: Any, **kws: Any) -> None:
    if self.isEnabledFor(TRACE):
        self._log(TRACE, message, args, **kws)


logging.Logger.trace = trace  # type: ignore[attr-defined]

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
