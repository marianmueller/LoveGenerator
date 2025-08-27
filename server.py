import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        text_type = data.get('text_type')
        era = data.get('era')
        
        prompt = f"Schreibe einen {text_type} im Stil des {era}. Jahrhunderts."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        
        generated_text = response.choices[0].message.content
        
        return jsonify({"text": generated_text})
    
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return jsonify({"text": f"Es ist ein Fehler aufgetreten: {str(e)}"})
