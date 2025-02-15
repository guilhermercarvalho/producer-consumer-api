from multiprocessing import Manager, Process
from random import uniform

from flask import Flask, jsonify

from .producer_consumer import Consumer, Producer
from .producer_consumer_flask import BufferFlask, ConsumerFlask, ProducerFlask


class AppOld(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.manager = Manager()
        self.processes = self.manager.dict()
        self.stats_buffers = self.manager.dict()

    def produce(self):
        return uniform(0, 100)

    def consume(self, data):
        print(f"Consumido: {data}")

    def start(self):
        def run_producer_consumer(app):
            bufferFlask: BufferFlask = BufferFlask(app)

            producer = Producer(bufferFlask, self.produce)
            consumer = Consumer(bufferFlask, self.consume)

            p_flask = ProducerFlask(producer)
            c_flask = ConsumerFlask(consumer)


            p = Process(target=p_flask.run)
            c = Process(target=c_flask.run)

            p.start()
            c.start()

            p.join()
            c.join()

        p = Process(target=run_producer_consumer, args=(self,))
        p.start()


        self.processes[len(self.processes)] = p.pid
        self.stats_buffers[len(self.stats_buffers)] = {
            "production": {
                "quantity": 0,
                "rate": 0,
            },
            "consumption": {"quantity": 0, "rate": 0},
        }
        return jsonify({"id": len(self.processes) - 1})

    def stop(self, id):
        if id in self.processes:
            p_pid = self.processes[id]

            import os

            os.kill(p_pid, 9)

            del self.processes[id]
            del self.stats_buffers[id]
            return jsonify({"message": "Processo parado"})
        else:
            return jsonify({"message": "Processo não encontrado"}), 404

    def stats(self, id):
        if id in self.stats_buffers:
            return jsonify(self.stats_buffers[id])
        else:
            return jsonify({"message": "Processo não encontrado"}), 404


app = AppOld()


@app.route("/start", methods=["POST"])
def start():
    return app.start()


@app.route("/stop/<int:id>", methods=["POST"])
def stop(id):
    return app.stop(id)


@app.route("/stats/<int:id>", methods=["GET"])
def stats(id):
    return app.stats(id)


if __name__ == "__main__":
    app.run(debug=True)
