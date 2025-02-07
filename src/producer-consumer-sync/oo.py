import threading
import time
import random
import unittest


class Buffer:
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.counter = 0
        self.mutex = threading.Lock()
        self.empty = threading.Semaphore(size)
        self.full = threading.Semaphore(0)
        self.insert_skipped = 0
        self.remove_missed = 0

    def insert_without_semaphore(self, item):
        if self.counter < self.size:
            self.buffer[self.counter] = item
            self.counter += 1
        else:
            self.insert_skipped += 1

    def remove_without_semaphore(self):
        if self.counter > 0:
            item = self.buffer[self.counter - 1]
            self.counter -= 1
            return item
        else:
            self.remove_missed += 1
            return None

    def insert_with_semaphore(self, item):
        self.empty.acquire()
        with self.mutex:
            self.insert_without_semaphore(item)
            print(f'Produzido: {item} | Buffer: {self.counter}/{self.size}')
        self.full.release()

    def remove_with_semaphore(self):
        self.full.acquire()
        with self.mutex:
            item = self.remove_without_semaphore()
            print(f'Consumido: {item} | Buffer: {self.counter}/{self.size}')
        self.empty.release()
        return item


class Producer(threading.Thread):
    def __init__(self, buffer, max_items, delay_range=(0.1, 0.5)):
        super().__init__()
        self.buffer = buffer
        self.max_items = max_items
        self.delay_range = delay_range

    def run(self):
        for _ in range(self.max_items):
            item = random.randint(1, 100)
            self.buffer.insert_with_semaphore(item)
            time.sleep(random.uniform(*self.delay_range))


class Consumer(threading.Thread):
    def __init__(self, buffer, max_items, delay_range=(0.1, 0.5)):
        super().__init__()
        self.buffer = buffer
        self.max_items = max_items
        self.delay_range = delay_range

    def run(self):
        for _ in range(self.max_items):
            self.buffer.remove_with_semaphore()
            time.sleep(random.uniform(*self.delay_range))

# Testes Unitários


class TestBuffer(unittest.TestCase):
    def setUp(self):
        self.buffer_size = 5
        self.max_items = 10

    def test_race_condition(self):
        buffer = Buffer(self.buffer_size)
        threads = []

        # Cria produtores e consumidores sem semáforos
        for _ in range(2):
            threads.append(threading.Thread(
                target=lambda: [buffer.insert_without_semaphore(i) for i in range(3)]
            ))
            threads.append(threading.Thread(
                target=lambda: [buffer.remove_without_semaphore() for _ in range(3)]
            ))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertGreater(buffer.insert_skipped + buffer.remove_missed, 0)

    def test_with_semaphores(self):
        buffer = Buffer(self.buffer_size)
        producer = Producer(buffer, self.max_items)
        consumer = Consumer(buffer, self.max_items)

        producer.start()
        consumer.start()

        producer.join()
        consumer.join()

        self.assertEqual(buffer.counter, 0)
        self.assertEqual(buffer.insert_skipped, 0)
        self.assertEqual(buffer.remove_missed, 0)

    def test_delayed_operations(self):
        buffer = Buffer(2)
        producer = Producer(buffer, 5, delay_range=(0.5, 1.0))
        consumer = Consumer(buffer, 5, delay_range=(0.1, 0.3))

        producer.start()
        consumer.start()

        producer.join()
        consumer.join()

        self.assertLessEqual(buffer.counter, buffer.size)


if __name__ == "__main__":
    # Exemplo de uso
    buffer = Buffer(10)
    producer = Producer(buffer, 20)
    consumer = Consumer(buffer, 20)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    print("\nResultado final:")
    print(f"Itens no buffer: {buffer.counter}")
    print(f"Produções perdidas: {buffer.insert_skipped}")
    print(f"Consumos falhos: {buffer.remove_missed}")

    # Executar testes
    unittest.main(argv=[''], exit=False)
