from abc import ABC
from datetime import datetime
from typing import Any

class ApplicationEvent(ABC):
    name: str
    occurred_at: datetime
    payload: Any