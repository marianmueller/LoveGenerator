# Importiert Flask, um einen Server zu erstellen
from flask import Flask, request, jsonify

# Erstellt eine Instanz der App
app = Flask(__name__)

# Der Endpunkt (die "Adresse"), die Ihre Webseite anruft
@app.route('/generate', methods=['POST'])
def generate_text():
    # Holt die Daten von Ihrer Webseite
    data = request.get_json()
    text_type = data.get('text_type')
    era = data.get('era')
    
    # Simuliert die Antwort der KI
    if text_type == 'Liebesgedicht' and era == '17':
        generated_text = "Ein Liebesgedicht aus dem 17. Jahrhundert."
    else:
        generated_text = "Ein generierter Text."
    
    # Sendet die Antwort als JSON zurück an Ihre Webseite
    return jsonify({"text": generated_text})

# Der Server startet, wenn das Skript läuft
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
