from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    text_type = data.get('text_type')
    era = data.get('era')
    
    if text_type == 'Liebesgedicht' and era == '17':
        generated_text = "Ein Liebesgedicht aus dem 17. Jahrhundert."
    else:
        generated_text = "Ein generierter Text."
    
    return jsonify({"text": generated_text})
