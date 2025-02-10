from time import sleep
from random import uniform
from abc import ABC, abstractmethod
from typing import Callable, Any


class Buffer(ABC):
    @abstractmethod
    def insert(self, data: Any) -> None:
        pass

    @abstractmethod
    def remove(self) -> Any:
        pass


class Producer():
    def __init__(self, buffer: Buffer, produce: Callable[[], Any], delay_range: tuple[int, int] = (0, 1)):
        self._buffer = buffer
        self._produce = produce
        self._delay_range = delay_range

    def run(self) -> None:
        sleep(uniform(*self._delay_range))
        self._buffer.insert(self._produce())


class Consumer():
    def __init__(self, buffer: Buffer, consume: Callable[[Any], None], delay_range: tuple[int, int] = (0, 1)):
        self._buffer = buffer
        self._consume = consume
        self._delay_range = delay_range

    def run(self) -> Any:
        sleep(uniform(*self._delay_range))
        self._consume(self._buffer.remove())
