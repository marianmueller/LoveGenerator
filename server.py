import os
from flask import Flask, request, jsonify
from openai import OpenAI

# Erstellt eine Instanz der App
app = Flask(__name__)

# Initialisiert den OpenAI-Client mit dem API-Schlüssel aus den Umgebungsvariablen
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Der Endpunkt, der die Anfrage von der Webseite empfängt
@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        # Holt die Daten von der Webseite
        data = request.get_json()
        text_type = data.get('text_type')
        era = data.get('era')
        
        # Erstellt den Prompt für die KI
        prompt = f"Schreibe einen {text_type} im Stil des {era}. Jahrhunderts."
        
        # Ruft die OpenAI-API auf
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        
        # Extrahiert den generierten Text
        generated_text = response.choices[0].message.content
        
        # Gibt den Text an die Webseite zurück
        return jsonify({"text": generated_text})
    
    except Exception as e:
        # Wenn ein Fehler auftritt, wird er abgefangen und eine Fehlermeldung gesendet
        print(f"Ein Fehler ist aufgetreten: {e}")
        return jsonify({"text": f"Es ist ein Fehler aufgetreten: {str(e)}"})

# Gunicorn wird die 'app' ausführen, daher benötigen wir keinen eigenen Start-Block.
