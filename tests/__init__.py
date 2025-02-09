"""
Dependem da classe Producer e Consumer
Funções de Produção (fn P()):
    - classe Producer que executa a fn P e insere no buffer
    - lógica de execução de fn P e método de inserção no buffer
    - produção fn generate_rand_number()

Funções de Consumo (fn C(data)):
    - classe Consumer que executa a fn C e remove do buffer
    - lógica de execução de fn C e método de remoção do buffer
    - consumo fn log(data)

Interação no Buffer
Buffer -> inserção e remoção abstratos
LocalBuffer
    - tamanho mínimo para armazenar data
    - apontador/contador para armazenar a posição atual
    S/ Semáforo
        - inserção
            - contar dado perdido
        - remoção
            - contar acesso inválido
    C/ Semáforo
        - semaphore
            - mutex: gerenciar a permissão de acesso ao buffer (inserir ou remover)
            - empty, full: informam o estado atual do buffer (se pode inserir ou remover)
        - inserção
        - remoção
RedisBuffer
    - configurar conexão
    - inserção
    - remoção
"""


class Buffer:
    pass


class BufferLocal(Buffer):
    def __init__(self, size):
        super().__setattr__("_size", size)
        self.slots = [None] * size
        self.pointer = 0

        self.invalid_access = 0
        self.skipped_insert = 0

    def insert(self, data):
        hasAnyEmptySlot = self.pointer < self._size

        if hasAnyEmptySlot:
            self.slots[self.pointer] = data
            self.pointer += 1
        else:
            self.skipped_insert += 1

    def remove(self):
        hasAnySlotFulfilled = self.pointer > 0

        if hasAnySlotFulfilled:
            data = self.slots[self.pointer - 1]
            self.pointer -= 1
            return data
        else:
            self.invalid_access += 1
            return -1

    @property
    def size(self):
        return self._size

    def __setattr__(self, name, value):
        if name == "_size":
            raise AttributeError("Attribute '_size' cannot be modified!")
        super().__setattr__(name, value)
