from .buffer_with_semaphore import BufferWithSemaphore
from .producer_consumer import Consumer, Producer


class BufferFlask(BufferWithSemaphore):
    def __init__(self, app):
        super().__init__(10)
        self._app = app

    def insert(self, data):
        super().insert(data)
        self.update_stats(self._app)  # Passa o app como argumento

    def remove(self):
        data = super().remove()
        self.update_stats(self._app)  # Passa o app como argumento
        return data

    def update_stats(self, app):
        self._app = app
        stats = super().stats()
        app.stats_buffers[len(app.stats_buffers) - 1] = stats


class ProducerFlask:
    def __init__(self, producer: Producer):
        self._producer = producer

    def run(self):
        self._producer.run()


class ConsumerFlask:
    def __init__(self, consumer: Consumer):
        self._consumer = consumer

    def run(self):
        self._consumer.run()
