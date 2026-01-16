from abc import ABC, abstractmethod
from typing import Callable, TypeVar, Awaitable

T = TypeVar('T')

class TransactionManager(ABC):
    @abstractmethod
    async def run_in_transaction(self, fn: Callable[[], Awaitable[T]]) -> T:
        pass