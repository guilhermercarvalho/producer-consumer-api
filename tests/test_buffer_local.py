import pytest

from src.producer_consumer_sync.buffer_local import BufferLocal


class TestBufferLocal:
    @pytest.mark.parametrize("size", [1, 5, 10])
    def test_create(self, size):
        buffer = BufferLocal(size)

        assert buffer.pointer == 0
        assert buffer.size == size
        assert len(buffer.slots) == size

    # TODO: Utilizar parametros para testar alterar os atributos privados
    def test_change_default_size(self):
        buffer = BufferLocal(10)

        with pytest.raises(AttributeError) as err:
            buffer._size = 1

        assert str(err.value) == "Attribute '_size' cannot be modified!"

    # TODO: Simular por parâmetro até capacidade máxima do buffer
    def test_insert_data_in(self):
        buffer = BufferLocal(10)
        buffer.insert(123)

        assert buffer.slots[0] == 123
        assert buffer.pointer == 1

    @pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
    def test_inserts_data_in(self, value):
        buffer = BufferLocal(5)
        buffer.insert(value)

        assert buffer.slots[0] == value
        assert buffer.pointer == 1

    def test_insert_data_in_fulfilled(self):
        buffer = BufferLocal(1)
        buffer.insert(123)
        buffer.insert(456)

        assert buffer.remove() != 456
        assert buffer.skipped_insert == 1

    def test_remove_data_in(self):
        buffer = BufferLocal(10)
        buffer.insert(123)

        assert buffer.remove() == 123
        assert buffer.pointer == 0

    def test_remove_data_in_empty(self):
        buffer = BufferLocal(10)

        assert buffer.remove() == -1
        assert buffer.invalid_access == 1
