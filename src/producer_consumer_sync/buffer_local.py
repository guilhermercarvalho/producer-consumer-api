from .producer_consumer import Buffer

class BufferLocal(Buffer):
    def __init__(self, size):
        super().__setattr__("_size", size)
        super().__setattr__("_slots", [None] * size)
        super().__setattr__("_pointer", 0)

        super().__setattr__("_invalid_access", 0)
        super().__setattr__("_skipped_insert", 0)

    def insert(self, data):
        hasAnyEmptySlot = self.pointer < self.size

        if hasAnyEmptySlot:
            self.slots[self.pointer] = data
            self._pointer += 1
        else:
            self._skipped_insert += 1

    def remove(self):
        hasAnySlotFulfilled = self.pointer > 0

        if hasAnySlotFulfilled:
            data = self.slots[self.pointer - 1]
            self._pointer -= 1
            return data
        else:
            self._invalid_access += 1
            return -1

    @property
    def size(self):
        return self._size

    @property
    def slots(self):
        return self._slots

    @property
    def pointer(self):
        return self._pointer

    @property
    def invalid_access(self):
        return self._invalid_access

    @property
    def skipped_insert(self):
        return self._skipped_insert

    def __setattr__(self, name, value):
        static_values = [
            "_size",
            "_slots",
            # "_pointer",
            # "_invalid_access",
            # "_skipped_insert"
        ]
        if name in static_values:
            raise AttributeError(f"Attribute '{name}' cannot be modified!")
        super().__setattr__(name, value)
