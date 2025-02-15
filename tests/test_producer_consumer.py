import random

import pytest

from src.producer_consumer_sync.buffer_local import BufferLocal
from src.producer_consumer_sync.buffer_with_semaphore import BufferWithSemaphore
from src.producer_consumer_sync.producer_consumer import Consumer, Producer


@pytest.fixture
def create_buffer_local(request):
    size = getattr(request, "param", 10)
    return BufferLocal(size)


@pytest.fixture
def create_buffer_with_semaphore(request):
    size = getattr(request, "param", 10)
    return BufferWithSemaphore(size)


class TestProducer:
    @pytest.mark.parametrize(
        "buffer_fixture",
        [
            "create_buffer_local",
            "create_buffer_with_semaphore",
        ],
    )
    def test_run(self, request, buffer_fixture):
        buffer = request.getfixturevalue(buffer_fixture)
        producer = Producer(buffer, lambda: random.randint(1, 100))
        producer.run()
        assert buffer.pointer > 0

    @pytest.mark.parametrize(
        "buffer_fixture",
        [
            "create_buffer_local",
            "create_buffer_with_semaphore",
        ],
    )
    def test_multiple_runs(self, request, buffer_fixture):
        buffer = request.getfixturevalue(buffer_fixture)
        producer = Producer(buffer, lambda: random.randint(1, 100))

        for _ in range(10):
            producer.run()

        assert buffer.pointer == 10


class TestConsumer:
    @pytest.mark.parametrize(
        "buffer_fixture",
        [
            "create_buffer_local",
            "create_buffer_with_semaphore",
        ],
    )
    def test_run(self, request, buffer_fixture):
        buffer = request.getfixturevalue(buffer_fixture)
        buffer.insert(random.randint(1, 100))
        consumer = Consumer(buffer, lambda x: print(x))
        consumer.run()
        assert buffer.pointer == 0

    @pytest.mark.parametrize(
        "buffer_fixture",
        [
            "create_buffer_local",
            "create_buffer_with_semaphore",
        ],
    )
    def test_multiple_runs(self, request, buffer_fixture):
        buffer = request.getfixturevalue(buffer_fixture)
        consumer = Consumer(buffer, lambda x: print(x))

        for _ in range(10):
            buffer.insert(random.randint(1, 100))
            consumer.run()

        assert buffer.pointer == 0


class TestProducerAndConsumerConcurrency:
    def test_producer_consumer_concurrency(self, create_buffer_with_semaphore):
        buffer = create_buffer_with_semaphore
        producer = Producer(buffer, lambda: random.randint(1, 100))
        consumer = Consumer(buffer, lambda x: print(x))

        import threading

        producer_thread = threading.Thread(target=producer.run)
        consumer_thread = threading.Thread(target=consumer.run)

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

        assert buffer._pointer.value == 0
