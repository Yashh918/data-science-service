from flask import Flask
from flask import request, jsonify
from kafka import KafkaProducer
import json
from service.messageService import MessageService

app = Flask(__name__)
app.config.from_pyfile('config.py')

messageService = MessageService()
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
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