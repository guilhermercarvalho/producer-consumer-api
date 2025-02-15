from flask import Flask, request, jsonify
from flask_cors import CORS
from .all import ProcessManager


class App:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, origins=["http://localhost:5173"])
        self.process_manager = ProcessManager()
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/start', 'start', self.start, methods=['POST', 'OPTIONS'])
        self.app.add_url_rule('/status/<process_id>', 'get_status',
                              self.get_status, methods=['GET', 'OPTIONS'])
        self.app.add_url_rule('/stop/<process_id>', 'stop', self.stop, methods=['POST', 'OPTIONS'])

    def start(self):
        if request.method == 'OPTIONS':
            return jsonify({}), 200, {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
        buffer_type = request.json.get('buffer_type', 'queue')
        process_id = self.process_manager.start_process(buffer_type)
        return jsonify({'process_id': process_id})

    def get_status(self, process_id):
        if request.method == 'OPTIONS':
            return jsonify({}), 200, {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
        status = self.process_manager.get_process_status(process_id)
        if status:
            return jsonify(status), 200
        return jsonify({"error": "Processo não encontrado"}), 404

    def stop(self, process_id):
        try:
            if request.method == 'OPTIONS':
                return jsonify({}), 200, {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                }
            self.process_manager.stop_process(process_id)
            return jsonify({"message": f"Processo {process_id} parado"})
        except RuntimeError:
            return jsonify({"error": "Processo não encontrado"}), 404


app = App().app

if __name__ == '__main__':
    app.run()
