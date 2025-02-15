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
