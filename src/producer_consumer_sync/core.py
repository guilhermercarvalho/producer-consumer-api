import random
import threading
import time
from typing import Any, Callable

# Configurações
BUFFER_SIZE = 10
MAX_ITEMS = 20

# Recursos compartilhados
buffer = [None] * BUFFER_SIZE
counter = 0

# Controles de sincronização
mutex = threading.Lock()
empty = threading.Semaphore(BUFFER_SIZE)  # Slots vazios
full = threading.Semaphore(0)  # Slots ocupados

# Estatísticas
insert_skipped = 0
remove_missed = 0

# Funções genéricas


def producer(
    produce_data: Callable[[], Any],
    buffer_insert: Callable[[Any], None],
    delay_range: tuple[float, float] = (0.1, 0.5),
) -> None:
    """Thread produtora genérica"""
    print(f"Função de produção: {produce_data.__name__}")
    data = produce_data()
    print(f"Função de inserção no buffer: {buffer_insert.__name__}")
    buffer_insert(data)
    time.sleep(random.uniform(*delay_range))
    print("\n")


def consumer(
    consume_data: Callable[[Any], None],
    buffer_remove: Callable[[], Any],
    delay_range: tuple[float, float] = (0.1, 0.5),
) -> None:
    """Thread consumidora genérica"""
    print(f"Função de remoção do buffer: {buffer_remove.__name__}")
    data = buffer_remove()
    print(f"Função de consumo: {consume_data.__name__}")
    consume_data(data)
    time.sleep(random.uniform(*delay_range))
    print("\n")


# Funções de produção


def produce_random_number() -> int:
    return random.randint(1, 100)


def produce_string() -> str:
    return f"MSG-{time.time()}"


# Funções de consumo


def consume_log_data(data: Any) -> None:
    print(f"Log: {data}")


def consume_save_to_file(data: Any) -> None:
    with open("output.txt", "a") as f:
        f.write(f"{data}\n")


# Insert and remove from buffer


def insert_in_buffer(item):
    global counter, insert_skipped

    hasEmptySlot = counter < BUFFER_SIZE

    if hasEmptySlot:
        buffer[counter] = item
        counter += 1
    else:
        insert_skipped += 1

    msg_info = f"Produzido: {item} | Buffer: {counter}/{BUFFER_SIZE}"
    msg_info += f" | Skipped: {insert_skipped}" if not hasEmptySlot else ""
    print(msg_info)

    print(buffer)


def insert_with_semaphore(item):
    empty.acquire()  # Espera slot vazio
    mutex.acquire()
    # Seção crítica
    insert_in_buffer(item)
    mutex.release()
    full.release()


def remove_from_buffer():
    global counter, remove_missed

    item = None

    hasFullSlot = counter > 0

    if hasFullSlot:
        item = buffer[counter - 1]
        buffer[counter - 1] = None
        counter -= 1
    else:
        remove_missed += 1

    msg_info = f"Consumido: {item} | Buffer: {counter}/{BUFFER_SIZE}"
    msg_info += f" | Missed: {remove_missed}" if not hasFullSlot else ""
    print(msg_info)

    print(buffer)

    return item


def remove_with_semaphore():
    full.acquire()  # Espera slot ocupado
    mutex.acquire()
    # Seção crítica
    item = remove_from_buffer()
    mutex.release()
    empty.release()  # Notifica slot vazio
    return item


# Create generic threads


def create_thread(
    target: Callable,
    action: Callable,
    buffer_action: Callable,
    delay_range: tuple[float, float] = (0, 1),
) -> threading.Thread:
    if delay_range:
        return threading.Thread(
            target=target, args=(action, buffer_action, delay_range)
        )
    else:
        return threading.Thread(target=target, args=(action, buffer_action))


# Producer threads


def produce_random_number_with_semaphore_thread() -> threading.Thread:
    return create_thread(
        target=producer,
        action=produce_random_number,
        buffer_action=insert_with_semaphore,
    )


def produce_random_number_with_semaphore_and_delay_thread() -> threading.Thread:
    return create_thread(
        target=producer,
        action=produce_random_number,
        buffer_action=insert_with_semaphore,
        delay_range=(1, 5),
    )


def produce_random_number_thread() -> threading.Thread:
    return create_thread(
        target=producer, action=produce_random_number, buffer_action=insert_in_buffer
    )


def produce_random_number_with_delay_thread() -> threading.Thread:
    return create_thread(
        target=producer,
        action=produce_random_number,
        buffer_action=insert_in_buffer,
        delay_range=(1, 5),
    )


# Consumer threads


def consume_random_number_with_semaphore_thread() -> threading.Thread:
    return create_thread(
        target=consumer, action=consume_log_data, buffer_action=remove_with_semaphore
    )


def consume_random_number_with_semaphore_and_delay_thread() -> threading.Thread:
    return create_thread(
        target=consumer,
        action=consume_log_data,
        buffer_action=remove_with_semaphore,
        delay_range=(1, 5),
    )


def consume_random_number_thread() -> threading.Thread:
    return create_thread(
        target=consumer, action=consume_log_data, buffer_action=remove_from_buffer
    )


def consume_random_number_with_delay_thread() -> threading.Thread:
    return create_thread(
        target=consumer,
        action=consume_log_data,
        buffer_action=remove_from_buffer,
        delay_range=(1, 5),
    )


# Testando
if __name__ == "__main__":
    NUM_THREAD = 8

    # Cria threads
    threads: list[threading.Thread] = []
    count = 0
    for i in range(NUM_THREAD):
        count += 1
        condition = i % 3 != 0

        print(f'Cria {"Produtor" if condition else "Consumidor"}: Thread-{count}')

        # TODO: criar listas com cenários de testes e verificar execução
        if condition:
            threads.append(produce_random_number_with_semaphore_thread())
            # threads.append(produce_random_number_with_semaphore_and_delay_thread())
            # threads.append(produce_random_number_thread())
            # threads.append(produce_random_number_with_delay_thread())
        else:
            threads.append(consume_random_number_with_semaphore_thread())
            # threads.append(consume_random_number_with_semaphore_and_delay_thread())
            # threads.append(consume_random_number_thread())
            # threads.append(consume_random_number_with_delay_thread())

    print(f"\n{threads}\n")

    # Inicia threads
    start = time.perf_counter()

    for thread in threads:
        thread.start()

    # Aguarda conclusão
    for thread in threads:
        thread.join()

    end = time.perf_counter()

    print("\nEstatísticas:")
    print(f"Slots perdidos (produção): {insert_skipped}")
    print(f"Slots falhos (consumo): {remove_missed}")
    print(f"Total time: {end - start}")
