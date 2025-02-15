from abc import ABC, abstractmethod
from multiprocessing import Manager
from random import uniform
from time import sleep, time
from typing import Any, Callable


class Buffer(ABC):
    def __init__(self, size):
        self._size = size
        self._slots = Manager().list([None] * size)

        self._pointer = Manager().Value("i", 0)

        self._produced = Manager().Value("i", 0)
        self._consumed = Manager().Value("i", 0)

        self._start_time = time()

    @abstractmethod
    def insert(self, data: Any) -> None:
        pass

    @abstractmethod
    def remove(self) -> Any:
        pass

    def increment_produced(self) -> None:
        self._produced.value += 1

    def increment_consumed(self) -> None:
        self._consumed.value += 1

    def stats(self) -> dict:
        current_time_execution = time() - self._start_time
        production_rate = self._produced.value / current_time_execution
        consumption_rate = self._consumed.value / current_time_execution
        return {
            "production": {
                "quantity": self._produced.value,
                "rate": production_rate,
            },
            "consumption": {"quantity": self._consumed.value, "rate": consumption_rate},
        }


class Producer:
    def __init__(
        self,
        buffer: Buffer,
        produce: Callable[[], Any],
        interval: tuple[int, int] = (0, 1),
    ):
        self._buffer = buffer
        self._produce = produce
        self._interval = interval

    def run(self) -> None:
        sleep(uniform(*self._interval))
        self._buffer.insert(self._produce())


class Consumer:
    def __init__(
        self,
        buffer: Buffer,
        consume: Callable[[Any], None],
        interval: tuple[int, int] = (0, 1),
    ):
        self._buffer = buffer
        self._consume = consume
        self._interval = interval

    def run(self) -> Any:
        sleep(uniform(*self._interval))
        self._consume(self._buffer.remove())
