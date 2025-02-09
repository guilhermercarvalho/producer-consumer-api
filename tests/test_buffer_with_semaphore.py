import pytest
from threading import Thread

from src.producer_consumer_sync.buffer_with_semaphore import BufferWithSemaphore

class TestBufferWithSemaphore:
    @pytest.mark.parametrize("size", [1, 5, 10])
    def test_create(self, size):
        buffer = BufferWithSemaphore(size)

        assert buffer.pointer == 0
        assert buffer.size == size
        assert len(buffer.slots) == size

    # TODO: Utilizar parametros para testar alterar os atributos privados
    def test_change_default_size(self):
        buffer = BufferWithSemaphore(10)

        with pytest.raises(AttributeError) as err:
            buffer._size = 1

        assert str(err.value) == "Attribute '_size' cannot be modified!"

    # TODO: Simular por parâmetro até capacidade máxima do buffer
    def test_insert_data(self):
        buffer = BufferWithSemaphore(10)
        buffer.insert(123)

        assert buffer.slots[0] == 123
        assert buffer.pointer == 1

    @pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
    def test_insert_until_max_capacity(self, value):
        buffer = BufferWithSemaphore(5)
        buffer.insert(value)

        assert buffer.slots[0] == value
        assert buffer.pointer == 1

    def test_insert_data_in_fulfilled(self):
        buffer = BufferWithSemaphore(1)
        buffer.insert(123)

        def insert():
            buffer.insert(456)

        thread = Thread(target=insert)

        thread.start()

        import time
        time.sleep(0.1)

        assert thread.is_alive()
        assert buffer.pointer == 1
        assert buffer.skipped_insert == 0

    def test_remove_data_in(self):
        buffer = BufferWithSemaphore(10)
        buffer.insert(123)

        assert buffer.remove() == 123
        assert buffer.pointer == 0

    def test_remove_data_in_empty(self):
        buffer = BufferWithSemaphore(10)

        def remove():
            buffer.remove()

        thread = Thread(target=remove)

        thread.start()

        import time
        time.sleep(0.1)

        assert thread.is_alive()
        assert buffer.pointer == 0
        assert buffer.invalid_access == 0
