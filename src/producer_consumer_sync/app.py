from flask import Flask, request, jsonify
from multiprocessing import Process, Manager
from random import uniform
from .producer_consumer import Producer, Consumer, Buffer
from .buffer_with_semaphore import BufferWithSemaphore as BufferLocal


class App(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.manager = Manager()
        self.processes = self.manager.dict()

    def produce(self):
        return uniform(0, 100)

    def consume(self, data):
        print(f"Consumido: {data}")

    def start(self):
        def run_producer_consumer():
            buffer: Buffer = BufferLocal(10)
            producer = Producer(buffer, self.produce, (3, 5))
            consumer = Consumer(buffer, self.consume, (3, 5))
            p = Process(target=producer.run)
            c = Process(target=consumer.run)
            p.start()
            c.start()
            p.join()
            c.join()

        p = Process(target=run_producer_consumer)
        p.start()
        self.processes[len(self.processes)] = p.pid
        return jsonify({'id': len(self.processes) - 1})

    def stop(self, id):
        if id in self.processes:
            p_pid = self.processes[id]

            import os
            os.kill(p_pid, 9)

            del self.processes[id]
            return jsonify({'message': 'Processo parado'})
        else:
            return jsonify({'message': 'Processo não encontrado'}), 404

    def stats(self, id):
        if id in self.processes:
            _, _, buffer= self.processes[id]
            buffer_stats= buffer.stats()
            return jsonify({
                'taxa de produção': buffer_stats['production']['rate'],
                'produzido': buffer_stats['production']['quantity'],
                'taxa de consumo': buffer_stats['consumption']['rate'],
                'consumido': buffer_stats['consumption']['quantity'],
                'buffer': len(buffer.slots)
            })
        else:
            return jsonify({'message': 'Processo não encontrado'}), 404


app= App()


@ app.route('/start', methods=['POST'])
def start():
    return app.start()


@ app.route('/stop/<int:id>', methods=['POST'])
def stop(id):
    return app.stop(id)


@ app.route('/stats/<int:id>', methods=['GET'])
def stats(id):
    return app.stats(id)


if __name__ == '__main__':
    app.run(debug=True)
