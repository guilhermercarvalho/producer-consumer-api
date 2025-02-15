"""
    Quer implementar uma API para iniciar, parar e acompanhar processos
P e C

Core:
    A funcionalidade central é a execução de processos concorrentes,
onde o P gera e insere o dado no buffer, e o consumidor remove o
dado do buffer e consome. Sendo assim:
    - Buffer
        - insere, remove, representa uma lista, size, get_info
        - race condition em insere e remove
        - Redis, multiprocessing.Queue
    - Producer
        - buffer, produce, inserido, stop_event
            - produce: verifica se stop_event.is_set(), e enquanto não, executa função que produz um dado,
            insere no buffer e incrementa inserido
                - após evento parar, inserir proc em db
    - Consumer
        - buffer, consume, removido, stop_event
            - consume: função que remove dado do buffer, consome, e incrementa removido
    - ProcessManager
        - manager, processes, status, criar, iniciar, parar, get_status, cleanup, finished
            - processes: mantém compartilhado entre os processos
            - status: adiciona status dos processos em execução
            - criar: cria um id (uuid4) para o processo, instância buffer, cria evento de parada, define propriedades do processo
                - retorno: id do processo criado -> process_id
                - propriedades
                    - buffer: size/type
                    - stop_event
                    - producer: função de produção
                    - consumer: função de consumo
                    - start_time: timestamp início
                    - running: estado atual do processo. Em execução, finalizado, terminado, erro,
                    - processing_time: delay de processamento
                    - inseridos: número de processos que conseguiram inserir dado no buffer
                    - removidos: número de processos que conseguiram consumir um dado do buffer
                    - taxa: relação entre produção e consumo
            - iniciar processos: inicia os processos criados. Executado em criar processo
                - encontra processo, extrai propriedades necessárias:
                    - buffer
                    - stop_event
                    - processing_time
                - instância classes Producer e Consumer
                - instancia Process p e c
                - atualiza propriedades producer e consumer com instância dos processos p e c
                - inicia processos
                - cria função terminator
                    - aguarda limite padrão de 60s e executa cleanup(process_id)
                    - insere proc em db
                - cria novo processo que executa terminator
            - get_status: retorna processos em execução
                - busca processo
                    - se não encontrar retorna erro e log err
                    - se sim, retornar propriedade de proc
                        - adiciona uptime: time da resposta da requisição - temp de início em process[process_id]['start_time']
            - stop: para processo, insere no banco, limpa residuais
                - busca processo
                    - se não encontrar retorna erro e log err
                    - se sim, self.cleanup(), retorna sucesso e log info
            - cleanup
                - se sim, limpar residuais, retorna sucesso e log info
"""

import pytest
import threading
import time
import multiprocessing
import uuid
from src.producer_consumer_sync.all import QueueBuffer, RedisBuffer, Producer, Consumer, ProcessManager


class TestQueueBuffer:
    @pytest.fixture
    def create(self):
        return QueueBuffer()

    @pytest.fixture
    def create_with_n_inserts(self, request, create):
        buffer = create
        n_inserts = getattr(request, "param", 10)
        for i in range(n_inserts):
            buffer.insert(i)
        return buffer

    def test_create(self, create):
        assert isinstance(create, QueueBuffer)

    def test_insert_in_buffer(self, create):
        buffer = create
        buffer.insert(42)
        assert buffer.size() == 1

    def test_multiple_inserts_in_buffer(self, create_with_n_inserts):
        buffer = create_with_n_inserts
        assert buffer.size() == 10

    def test_remove_in_buffer(self, create):
        buffer = create
        buffer.insert(42)
        buffer.remove()
        assert buffer.size() == 0

    def test_multiple_removes_in_buffer(self, create_with_n_inserts):
        buffer = create_with_n_inserts
        for _ in range(5):
            buffer.remove()
        assert buffer.size() == 5


class TestRedisBuffer:
    @pytest.fixture
    def create(self):
        buffer = RedisBuffer()
        buffer.cleanup()
        return buffer

    @pytest.fixture
    def create_with_n_inserts(self, request, create):
        buffer = create
        n_inserts = getattr(request, "param", 10)
        for i in range(n_inserts):
            buffer.insert(i)
        return buffer

    def test_create(self, create):
        assert isinstance(create, RedisBuffer)

    def test_insert_in_buffer(self, create):
        buffer = create
        buffer.insert(42)
        assert buffer.size() == 1

    def test_multiple_inserts_in_buffer(self, create_with_n_inserts):
        buffer = create_with_n_inserts
        assert buffer.size() == 10

    def test_remove_in_buffer(self, create):
        buffer = create
        buffer.insert(42)
        buffer.remove()
        assert buffer.size() == 0

    def test_multiple_removes_in_buffer(self, create_with_n_inserts):
        buffer = create_with_n_inserts
        for _ in range(5):
            buffer.remove()
        assert buffer.size() == 5


class TestRunProcesses:
    def produce(self):
        return 1

    def consume(self, item):
        pass

    @pytest.fixture
    def buffer(self, ):
        return QueueBuffer()

    @pytest.fixture
    def stop_event(self):
        return threading.Event()

    def test_producer_run(self, buffer, stop_event):
        producer = Producer(buffer, self.produce, stop_event)
        threading.Thread(target=producer.run).start()
        time.sleep(0.5)
        stop_event.set()
        assert producer.inserted > 0

    def test_consumer_run(self, buffer, stop_event):
        consumer = Consumer(buffer, self.consume, stop_event)
        threading.Thread(target=consumer.run).start()
        time.sleep(0.5)
        stop_event.set()
        assert consumer.consumed == 0

    def test_producer_consumer_run(self, buffer, stop_event):
        producer = Producer(buffer, self.produce, stop_event)
        consumer = Consumer(buffer, self.consume, stop_event)
        threading.Thread(target=producer.run).start()
        threading.Thread(target=consumer.run).start()
        time.sleep(1)
        stop_event.set()
        assert producer.inserted > 0
        assert consumer.consumed > 0

    def test_producer_inserted(self, buffer, stop_event):
        producer = Producer(buffer, self.produce, stop_event)
        threading.Thread(target=producer.run).start()
        time.sleep(0.5)
        stop_event.set()
        assert producer.inserted == buffer.size()

    def test_consumer_consumed(self, buffer, stop_event):
        producer = Producer(buffer, self.produce, stop_event)
        consumer = Consumer(buffer, self.consume, stop_event)
        threading.Thread(target=producer.run).start()
        threading.Thread(target=consumer.run).start()
        time.sleep(1)
        stop_event.set()
        assert consumer.consumed <= producer.inserted
