from src.producer_consumer_sync.buffer_local import BufferLocal
from threading import Lock, Semaphore

class BufferWithSemaphore(BufferLocal):
    def __init__(self, size):
        super().__init__(size)

        self._mutex = Lock()
        self.empty = Semaphore(self.size)
        self.full = Semaphore(0)

    def insert(self, data):
        self.empty.acquire()
        with self._mutex:
            super().insert(data)
        self.full.release()

    def remove(self):
        self.full.acquire()
        with self._mutex:
            data = super().remove()
        self.empty.release()
        return data
