from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class DomainEventHandler(ABC, Generic[T]):
    @abstractmethod
    async def handle(self, event: T) -> None:
        pass