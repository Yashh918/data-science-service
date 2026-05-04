from flask import Flask
from flask import request, jsonify
from service.messageService import MessageService

app = Flask(__name__)
app.config.from_pyfile('config.py')

messageService = MessageService()

@app.route('/api/v1/ds/message', methods=['POST'])
def handle_message():
    message = request.json.get('message')
    result = messageService.process_message(message)

    if result is None:
        return jsonify({"error": "Not a Bank SMS"}), 400

    return jsonify(result.dict()), 200

if __name__ == "__main__":
    app.run(host="localhost", port=8010, debug=True)