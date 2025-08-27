# Importieren des Flask-Webframeworks
from flask import Flask, request, jsonify

# Erstellen einer Flask-Anwendung
app = Flask(__name__)

# Haupt-Endpunkt für die Textgenerierung
@app.route('/generate', methods=['POST'])
def generate_text():
    # Erhalten der Daten aus der Anfrage
    data = request.get_json()
    text_type = data.get('text_type')
    era = data.get('era')
    
    # Hier simulieren wir die KI-Antwort.
    # In einem echten Projekt würde hier die KI-API aufgerufen.
    if text_type == 'Liebesgedicht' and era == '17':
        generated_text = "Ihr holdes Antlitz, ein strahlend Licht, / In dem die Liebe ihr Wesen spricht. / Ein Herz aus Gold, so rein und wahr, / Ich schwör' Euch Treu, mein' einziges Haar."
    elif text_type == 'Liebesbrief' and era == '19':
        generated_text = "Verehrteste, / In tiefer Sehnsucht verfasst, dieser Brief. Die Abwesenheit Eures holden Wesens hat eine schmerzliche Lücke hinterlassen. Mögen die Sterne uns bald wieder vereinen."
    else:
        generated_text = "Kein passender Text gefunden."
    
    # Die Antwort als JSON zurückgeben
    return jsonify({"text": generated_text})

# Der Server startet, wenn das Skript direkt ausgeführt wird
if __name__ == '__main__':
    app.run(debug=True)
