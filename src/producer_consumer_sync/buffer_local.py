from tests import Buffer

class BufferLocal(Buffer):
    def __init__(self, size):
        super().__setattr__("_size", size)
        self.slots = [None] * size
        self.pointer = 0

        self.invalid_access = 0
        self.skipped_insert = 0

    def insert(self, data):
        hasAnyEmptySlot = self.pointer < self._size

        if hasAnyEmptySlot:
            self.slots[self.pointer] = data
            self.pointer += 1
        else:
            self.skipped_insert += 1

    def remove(self):
        hasAnySlotFulfilled = self.pointer > 0

        if hasAnySlotFulfilled:
            data = self.slots[self.pointer - 1]
            self.pointer -= 1
            return data
        else:
            self.invalid_access += 1
            return -1

    @property
    def size(self):
        return self._size

    def __setattr__(self, name, value):
        if name == "_size":
            raise AttributeError("Attribute '_size' cannot be modified!")
        super().__setattr__(name, value)
