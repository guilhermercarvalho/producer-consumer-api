from threading import Thread

import pytest

from src.producer_consumer_sync.buffer_with_semaphore import BufferWithSemaphore


@pytest.fixture
def create_buffer(request):
    # Obtém o valor do parâmetro "size" ou usa o valor padrão 10
    size = getattr(request, "param", 10)
    return BufferWithSemaphore(size)


@pytest.fixture
def create_buffer_with_timeout(request):
    # Obtém o valor do parâmetro "size" ou usa o valor padrão 10
    size = getattr(request, "param", 10)
    return BufferWithSemaphore(size, 1)


@pytest.fixture
def buffer_with_slot_fulfilled(request, create_buffer):
    data = getattr(request, "param", 1)
    create_buffer.insert(data)
    return create_buffer


class TestBufferWithSemaphore:
    @pytest.mark.parametrize("create_buffer", [1, 5, 10], indirect=True)
    def test_create(self, create_buffer):
        buffer = create_buffer

        assert buffer._pointer.value == 0
        assert buffer._size in [1, 5, 10]
        assert len(buffer._slots) in [1, 5, 10]

    # def test_change_default_size(self):
    #     buffer = BufferWithSemaphore(10)

    #     with pytest.raises(AttributeError) as err:
    #         buffer._size = 1

    #     assert str(err.value) == "Attribute '_size' cannot be modified!"

    def test_insert(self, buffer_with_slot_fulfilled):
        buffer = buffer_with_slot_fulfilled

        assert buffer._slots[0] == 1
        assert buffer._pointer.value == 1
        assert buffer._produced.value == 1

    def test_insert_until_max_capacity(self, create_buffer):
        buffer = create_buffer

        range_list = list(range(10))

        for i in range_list:
            buffer.insert(i)

        assert list(buffer._slots) == range_list
        assert buffer._pointer.value == 10
        assert buffer._produced.value == 10

    @pytest.mark.parametrize("value", [1, 5, 10])
    def test_insert_changing_capacity(self, create_buffer, value):
        buffer = create_buffer

        range_values = list(range(value))

        for i in range_values:
            buffer.insert(i)

        assert buffer._slots[: len(range_values)] == range_values
        assert buffer._pointer.value == value
        assert buffer._produced.value == value

    @pytest.mark.parametrize("create_buffer_with_timeout", [1], indirect=True)
    def test_insert_above_maximum_capacity(self, create_buffer_with_timeout):
        buffer = create_buffer_with_timeout
        buffer.insert(1)

        def insert():
            buffer.insert(2)

        thread = Thread(target=insert)
        thread.start()

        import time

        time.sleep(2)

        assert not thread.is_alive()
        assert buffer._pointer.value == 1
        assert buffer._skipped_insert.value == 1
        assert buffer._produced.value == 1

    def test_remove(self, buffer_with_slot_fulfilled):
        buffer = buffer_with_slot_fulfilled

        assert buffer.remove() == 1
        assert buffer._pointer.value == 0
        assert buffer._consumed.value == 1

    def test_remove_when_empty(self, create_buffer_with_timeout):
        buffer = create_buffer_with_timeout

        def remove():
            buffer.remove()

        thread = Thread(target=remove)

        thread.start()

        import time

        time.sleep(2)

        assert not thread.is_alive()
        assert buffer._pointer.value == 0
        assert buffer._invalid_access.value == 1
        assert buffer._consumed.value == 0
