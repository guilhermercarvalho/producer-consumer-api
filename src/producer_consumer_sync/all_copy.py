import multiprocessing
import redis
import uuid
import time
import random


class BufferStrategy:
    def insert(self, item): raise NotImplementedError
    def remove(self): raise NotImplementedError
    def size(self): raise NotImplementedError
    def get_info(self): raise NotImplementedError


class QueueBuffer(BufferStrategy):
    def __init__(self, queue: multiprocessing.Queue, metrics):
        self.queue = queue
        self.metrics = metrics

    def insert(self, item):
        self.queue.put(item)
        self.metrics['produced'] += 1
        self.metrics['buffer_size'] = self.queue.qsize()

    def remove(self):
        item = self.queue.get()
        self.metrics['consumed'] += 1
        self.metrics['buffer_size'] = self.queue.qsize()
        return item


class RedisBuffer(BufferStrategy):
    def __init__(self, metrics, redis_url="redis://redis:6379"):
        self.redis = redis.Redis.from_url(redis_url)
        self.channel = 'buffer_channel'
        self.metrics = metrics

    def insert(self, item):
        self.redis.rpush(self.channel, item)
        self.metrics['produced'] += 1
        self.metrics['buffer_size'] = self.redis.llen(self.channel)

    def remove(self):
        item = self.redis.lpop(self.channel)
        if item:
            self.metrics['consumed'] += 1
            self.metrics['buffer_size'] = self.redis.llen(self.channel)
            return item
        return None

    def cleanup(self):
        return self.redis.delete(self.channel)


class Producer:
    def __init__(self, buffer, produce, stop_event, metrics):
        self.buffer = buffer
        self.produce = produce
        self.stop_event = stop_event
        self.metrics = metrics

    def run(self):
        while not self.stop_event.is_set():
            item = self.produce()
            self.buffer.insert(item)
            self.metrics['produced'] += 1
            self.metrics['items_processed'] += 1
            self.update_throughput(self.metrics)

    def update_throughput(self, metrics):
        elapsed_time = time.time() - metrics['start_time']
        if elapsed_time > 0:
            metrics['throughput'] = metrics['items_processed'] / elapsed_time


class Consumer:
    def __init__(self, buffer, consume, stop_event, metrics):
        self.buffer = buffer
        self.consume = consume
        self.stop_event = stop_event
        self.metrics = metrics

    def run(self):
        while not self.stop_event.is_set():
            item = self.buffer.remove()
            self.consume(item)
            self.metrics['consumed'] += 1
            self.metrics['items_processed'] += 1
            self.update_throughput(self.metrics)

    def update_throughput(self, metrics):
        elapsed_time = time.time() - metrics['start_time']
        if elapsed_time > 0:
            metrics['throughput'] = metrics['items_processed'] / elapsed_time


def produce():
    return random.randint(1, 1000)


def consume(item):
    pass


FIVE_MINUTES = 60 * 5

class ProcessManager:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.processes = self.manager.dict()
        self.queues = self.manager.list()

    def start_process(self, buffer_type, processing_time=(1, 5)):
        process_id = str(uuid.uuid4())
        stop_event = self.manager.Event()
        metrics = self.manager.dict({
            'produced': 0,
            'consumed': 0,
            'buffer_size': 0,
            'throughput': 0.0,
            'start_time': time.time(),
            'items_processed': 0
        })

        if buffer_type == 'queue':
            queue = self.manager.Queue()
            self.queues.append(queue)
            buffer = QueueBuffer(queue, metrics)
        else:
            buffer = RedisBuffer(metrics)

        # Armazena apenas informações necessárias
        self.processes[process_id] = {
            'buffer_type': buffer_type,
            'stop_event': stop_event,
            'producer_proc': None,
            'consumer_proc': None,
            'start_time': time.time(),
            'metrics': metrics
        }

        # Inicia os processos
        producer_proc = multiprocessing.Process(
            target=self._run_producer,
            args=(process_id, buffer, stop_event, processing_time)
        )
        consumer_proc = multiprocessing.Process(
            target=self._run_consumer,
            args=(process_id, buffer, stop_event, processing_time)
        )


        self.processes[process_id]['producer_proc'] = producer_proc
        self.processes[process_id]['consumer_proc'] = consumer_proc

        producer_proc.start()
        consumer_proc.start()

        # Agenda a parada automática após 120 segundos
        def terminate():
            time.sleep(FIVE_MINUTES)
            self.cleanup_process(process_id)

        multiprocessing.Process(target=terminate).start()

        return process_id

    def _run_producer(self, process_id, buffer, stop_event, processing_time):
        time.sleep(random.uniform(processing_time[0], processing_time[1]))
        metrics = self.processes[process_id]['metrics']
        producer = Producer(buffer, produce, stop_event, metrics)
        producer.run()

    def _run_consumer(self, process_id, buffer, stop_event, processing_time):
        time.sleep(random.uniform(processing_time[0], processing_time[1]))
        metrics = self.processes[process_id]['metrics']
        consumer = Consumer(buffer, consume, stop_event, metrics)
        consumer.run()

    def cleanup_process(self, process_id):
        if process_id in self.processes:
            proc = self.processes[process_id]
            proc['stop_event'].set()  # Sinaliza para parar

            # Aguarda os processos terminarem
            if proc['producer_proc']:
                proc['producer_proc'].join(timeout=5)
            if proc['consumer_proc']:
                proc['consumer_proc'].join(timeout=5)

            del self.processes[process_id]

    def stop_process(self, process_id):
        if process_id in self.processes:
            self.cleanup_process(process_id)
            return {"message": f"Processo {process_id} parado"}

    def get_process_status(self, process_id):
        if process_id in self.processes:
            proc = self.processes[process_id]
            metrics = proc['metrics']
            return {
                'buffer_type': proc['buffer_type'],
                'running': not proc['stop_event'].is_set(),
                'uptime': time.time() - proc['start_time'],
                'produced': metrics['produced'],
                'consumed': metrics['consumed'],
                'throughput': metrics['throughput'],
                'rate': metrics['produced'] / metrics['consumed'] if metrics['consumed'] > 0 else 0
            }
        return None
