from abc import ABC, abstractmethod
from typing import Any

class Buffer(ABC):
    @abstractmethod
    def insert(self, data: Any) -> None:
        pass

    @abstractmethod
    def remove(self) -> Any:
        pass
