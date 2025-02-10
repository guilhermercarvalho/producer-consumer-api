from time import sleep, time
from random import uniform
from abc import ABC, abstractmethod
from typing import Callable, Any
from multiprocessing import Manager


class Buffer(ABC):
    def __init__(self, size):
        self._size = size
        self._slots = Manager().list([None] * size)

        self._pointer = Manager().Value('i', 0)

        self._produced = Manager().Value('i', 0)
        self._consumed = Manager().Value('i', 0)

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
            'production': {
                'quantity': self._produced.value,
                'rate': production_rate,
            },
            'consumption': {
                'quantity': self._consumed.value,
                'rate': consumption_rate
            }
        }


class Producer():
    def __init__(self, buffer: Buffer, produce: Callable[[], Any], delay_range: tuple[int, int] = (0, 1)):
        self._buffer = buffer
        self._produce = produce
        self._delay_range = delay_range

    def run(self) -> None:
        while True:
            sleep(uniform(*self._delay_range))
            self._buffer.insert(self._produce())


class Consumer():
    def __init__(self, buffer: Buffer, consume: Callable[[Any], None], delay_range: tuple[int, int] = (0, 1)):
        self._buffer = buffer
        self._consume = consume
        self._delay_range = delay_range

    def run(self) -> Any:
        while True:
            sleep(uniform(*self._delay_range))
            self._consume(self._buffer.remove())
