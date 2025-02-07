import threading
import time
import random

# Configurações
BUFFER_SIZE = 10
MAX_ITEMS = 20

# Recursos compartilhados
buffer = [None] * BUFFER_SIZE
counter = 0

# Controles de sincronização
mutex = threading.Lock()
empty = threading.Semaphore(BUFFER_SIZE)  # Slots vazios
full = threading.Semaphore(0)             # Slots ocupados

# Estatísticas
insert_skipped = 0
remove_missed = 0

# Método de inserção sem semáforo (race condition)


def insert_in_buffer(item):
    global counter, insert_skipped
    if counter < BUFFER_SIZE:
        buffer[counter] = item
        counter += 1
    else:
        insert_skipped += 1

# Método de remoção sem semáforo (race condition)


def remove_from_buffer():
    global counter, remove_missed
    if counter > 0:
        item = buffer[counter - 1]
        counter -= 1
        return item
    else:
        remove_missed += 1
        return None

# Método de inserção com semáforo


def insert_with_semaphore(item):
    empty.acquire()  # Espera slot vazio
    mutex.acquire()
    # Seção crítica
    insert_in_buffer(item)
    print(f'Produzido: {item} | Buffer: {counter}/{BUFFER_SIZE}')
    mutex.release()
    full.release()   # Notifica slot ocupado

# Método de remoção com semáforo


def remove_with_semaphore():
    full.acquire()   # Espera slot ocupado
    mutex.acquire()
    # Seção crítica
    item = remove_from_buffer()
    print(f'Consumido: {item} | Buffer: {counter}/{BUFFER_SIZE}')
    mutex.release()
    empty.release()  # Notifica slot vazio
    return item

# Métodos com delay


def insert_with_semaphore_delay(delay):
    time.sleep(delay)
    insert_with_semaphore(random.randint(1, 100))


def remove_with_semaphore_delay(delay):
    time.sleep(delay)
    remove_with_semaphore()

# Funções para threads


def produtor():
    for _ in range(MAX_ITEMS):
        insert_with_semaphore(random.randint(1, 100))
        time.sleep(random.uniform(0.1, 0.5))  # Simula trabalho


def consumidor():
    for _ in range(MAX_ITEMS):
        remove_with_semaphore()
        time.sleep(random.uniform(0.1, 0.5))  # Simula trabalho


# Testando
if __name__ == "__main__":
    # Cria threads
    produtor_thread = threading.Thread(target=produtor)
    consumidor_thread = threading.Thread(target=consumidor)

    # Inicia threads
    produtor_thread.start()
    consumidor_thread.start()

    # Aguarda conclusão
    produtor_thread.join()
    consumidor_thread.join()

    print(f"\nEstatísticas:")
    print(f"Slots perdidos (produção): {insert_skipped}")
    print(f"Slots falhos (consumo): {remove_missed}")
