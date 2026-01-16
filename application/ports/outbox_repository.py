from abc import ABC, abstractmethod
from application.events.application_event import ApplicationEvent


class OutboxRepository(ABC):
    @abstractmethod
    async def save(self, event: ApplicationEvent) -> None:
        pass