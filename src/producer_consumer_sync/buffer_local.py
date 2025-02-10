from .producer_consumer import Buffer
from multiprocessing import Manager

class BufferLocal(Buffer):
    def __init__(self, size):
        super().__init__(size)

        self._invalid_access = Manager().Value('i', 0)
        self._skipped_insert = Manager().Value('i', 0)

    def insert(self, data):
        hasAnyEmptySlot = self._pointer.value < self._size

        if hasAnyEmptySlot:
            self._slots[self._pointer.value] = data
            self._pointer.value += 1
            self.increment_produced()
        else:
            self._skipped_insert.value += 1

    def remove(self):
        hasAnySlotFulfilled = self._pointer.value > 0

        if hasAnySlotFulfilled:
            data = self._slots[self._pointer.value - 1]
            self._pointer.value -= 1
            self.increment_consumed()
            return data
        else:
            self._invalid_access.value += 1
            return -1

    # @property
    # def size(self):
    #     return self._size

    # @property
    # def slots(self):
    #     return self._slots

    # @property
    # def pointer(self):
    #     return self._pointer

    # @property
    # def invalid_access(self):
    #     return self._invalid_access.value

    # @property
    # def skipped_insert(self):
    #     return self._skipped_insert

    # def __setattr__(self, name, value):
    #     static_values = [
    #         "_size",
    #         "_slots",
    #         # "_pointer",
    #         # "_invalid_access",
    #         # "_skipped_insert"
    #     ]
    #     if name in static_values:
    #         raise AttributeError(f"Attribute '{name}' cannot be modified!")
    #     super().__setattr__(name, value)
