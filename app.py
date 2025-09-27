from flask import Flask, render_template, request, jsonify, Response
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    try:
        response = requests.post('http://localhost:1234/v1/chat/completions', json=data, stream=True)
        def generate():
            for line in response.iter_lines():
                if line:
                    yield f"data: {line.decode('utf-8')}\n\n"
        return Response(generate(), mimetype='text/event-stream')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)