import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# Erstelle eine Flask-App
app = Flask(__name__)
# Aktiviere CORS, um Anfragen von der Webseite zu erlauben
CORS(app)

# Initialisiere den OpenAI-Client mit dem API-Schlüssel
# Der API-Schlüssel wird aus der Umgebungsvariable geladen
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/generate', methods=['POST'])
def generate_text():
    """
    Diese Funktion verarbeitet POST-Anfragen, um einen Text von der KI zu generieren.
    """
    try:
        data = request.get_json()
        text_type = data.get('text_type')
        era = data.get('era')
        tone = data.get('tone')
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Deine Aufgabe ist es, einen EINZIGEN, geschlechtsneutralen Text zu erstellen, entweder einen Liebesbrief ODER ein Liebesgedicht. "
                        "Generiere KEINEN TITEL wie 'Liebesbrief' oder 'Liebesgedicht'. "
                        "Generiere KEINE PLATZHALTER wie 'Dein Name' oder ähnliches. NIEMALS. "
                        "Verfasse einen Liebesbrief AUSSCHLIESSLICH als Prosatext. "
                        "Verfasse ein Liebesgedicht AUSSCHLIESSLICH in Versform mit Reimen oder Rhythmus. "
                        "Beschränke den Liebesbrief auf maximal acht Zeilen und 70 Wörter. "
                        "Beschränke das Liebesgedicht auf maximal zwei Strophen zu je vier Versen."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Schreibe einen {text_type} im Stil des {era}. Jahrhunderts mit einem {tone} Tonfall. "
                        f"Orientierung: "
                        "Klassisch-romantisch: sehnsuchtsvoll, schwärmerisch, zärtlich, leidenschaftlich. "
                        "Feierlich-kunstvoll: würdevoll, erhaben, pathetisch, höfisch-galant, ergeben/dienend. "
                        "Verspielt-leicht: witzig, humorvoll, augenzwinkernd, flirtend, innlich, melancholisch. "
                        "Dunkel-dramatisch: schmerzhaft, klagend, schicksalsergeben, tragisch. "
                        "Epochen-Orientierung: "
                        "Barock (1600-1720); Aufklärung (1720-1800); Empfindsamkeit (1740-1790); Sturm und Drang (1765-1785); "
                        "Weimarer Klassik (1786-1805); Romantik (1795-1835); Biedermeier (1815-1845); Vormärz (1825-1848); "
                        "Realismus (1850-1890); Naturalismus (1880-1900); Moderne (1890-1920); Expressionismus (1910-1925); "
                        "Avantgarde/Dadaismus (1915-1925); Nachkriegsliteratur (1945-1960); Neue Subjektivität (seit 1970); "
                        "Postmoderne (seit 1980)."
                    )
                }
            ],
            max_tokens=200
        )
        
        generated_text = response.choices[0].message.content
        
        return jsonify({"text": generated_text})
    
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return jsonify({"text": f"Es ist ein Fehler aufgetreten: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
