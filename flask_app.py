from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/process-text', methods=['POST'])
def process_text():
    # Get the text from the request body
    data = request.get_json()
    t = data['text']

    # Example processing: Count words and characters
    word_count = len(t.split())
    char_count = len(t)

    return jsonify({
        'status': 'success',
        'word_count': word_count,
        'char_count': char_count
    })

if __name__ == '__main__':
    app.run(debug=True)



'''
curl -X POST http://localhost:5000/process-text \
-H "Content-Type: application/json" \
-d '{"text": "This is a song. It has lyrics. Line by line."}'
'''