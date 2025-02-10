from .buffer_local import BufferLocal
from threading import Lock, Semaphore

class BufferWithSemaphore(BufferLocal):
    def __init__(self, size, timeout = 0):
        super().__init__(size)

        self._timeout = timeout if timeout > 0 else None

        self._mutex = Lock()
        self._empty = Semaphore(self.size)
        self._full = Semaphore(0)

    def insert(self, data):
        self._empty.acquire(timeout=self._timeout)
        with self._mutex:
            super().insert(data)
        self._full.release()

    def remove(self):
        self._full.acquire(timeout=self._timeout)
        with self._mutex:
            data = super().remove()
        self._empty.release()
        return data
