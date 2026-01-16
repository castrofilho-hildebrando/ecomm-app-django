from typing import Callable, TypeVar, Awaitable
from django.db import transaction
from application.ports.transaction_manager import TransactionManager

T = TypeVar('T')


class DjangoTransactionManager(TransactionManager):
    async def run_in_transaction(self, fn: Callable[[], Awaitable[T]]) -> T:
        async with transaction.atomic():
            return await fn()