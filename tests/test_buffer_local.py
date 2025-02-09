import pytest

from src.producer_consumer_sync.buffer_local import BufferLocal


@pytest.fixture
def create_buffer(request):
    # Obtém o valor do parâmetro "size" ou usa o valor padrão 10
    size = getattr(request, "param", 10)
    return BufferLocal(size)

@pytest.fixture
def buffer_with_slot_fulfilled(request, create_buffer):
    data = getattr(request, "param", 1)
    create_buffer.insert(data)
    return create_buffer

class TestBufferLocal:
    @pytest.mark.parametrize("create_buffer", [1, 5, 10], indirect=True)
    def test_create(self, create_buffer):
        buffer = create_buffer

        assert buffer.pointer == 0
        assert buffer.size in [1, 5, 10]
        assert len(buffer.slots) in [1, 5, 10]

    # ! testar alterar os atributos privados
    def test_change_default_size(self, create_buffer):
        buffer = create_buffer

        with pytest.raises(AttributeError) as err:
            buffer._size = 1

        assert str(err.value) == "Attribute '_size' cannot be modified!"

    def test_insert(self, buffer_with_slot_fulfilled):
        buffer = buffer_with_slot_fulfilled

        assert buffer.slots[0] == 1
        assert buffer.pointer == 1

    def test_insert_until_max_capacity(self, create_buffer):
        buffer = create_buffer

        for i in range(10):
            buffer.insert(i)

        assert buffer.slots == list(range(10))
        assert buffer.pointer == 10

    @pytest.mark.parametrize("value", [1, 5, 10])
    def test_insert_changing_capacity(self, create_buffer, value):
        buffer = create_buffer

        range_values = list(range(value))

        for i in range_values:
            buffer.insert(i)

        assert buffer.slots[:len(range_values)] == range_values
        assert buffer.pointer == value

    @pytest.mark.parametrize("create_buffer", [1], indirect=True)
    def test_insert_above_maximum_capacity(self, create_buffer):
        buffer = create_buffer

        values = [0, 1]
        last_value = values[len(values) - 1]

        for value in values:
            buffer.insert(value)

        assert buffer.remove() != last_value
        assert buffer.skipped_insert == 1

    def test_remove(self, buffer_with_slot_fulfilled):
        buffer = buffer_with_slot_fulfilled

        assert buffer.remove() == 1
        assert buffer.pointer == 0

    def test_remove_when_empty(self, create_buffer):
        buffer = create_buffer

        assert buffer.remove() == -1
        assert buffer.invalid_access == 1
