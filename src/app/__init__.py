from flask import Flask
from flask import request, jsonify
from kafka import KafkaProducer
import json
import os
from app.service.messageService import MessageService

app = Flask(__name__)
app.config.from_pyfile('config.py')

kafka_host = os.getenv('KAFKA_HOST', 'localhost')
kafka_port = os.getenv('KAFKA_PORT', 9092)
kafka_bootstrap_servers = f"{kafka_host}:{kafka_port}"

messageService = MessageService()
producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(2, 5, 0)
)

@app.route('/api/v1/ds/message', methods=['POST'])
def handle_message():
    message = request.json.get('message')
    result = messageService.process_message(message)

    if result is None:
        return jsonify({"error": "Not a Bank SMS"}), 400

    
    result_dict = result.model_dump()
    
    producer.send('bank.message', result_dict)

    return jsonify(result_dict), 200

if __name__ == "__main__":
    app.run(host="localhost", port=8010, debug=True)