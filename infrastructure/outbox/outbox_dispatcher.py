from abc import ABC, abstractmethod


class OutboxDispatcher(ABC):
    @abstractmethod
    async def dispatch(self) -> None:
        pass
