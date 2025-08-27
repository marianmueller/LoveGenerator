import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        text_type = data.get('text_type')
        era = data.get('era')
        tone = data.get('tone')
        
        prompt = (
            f"Generiere ausschließlich einen einzigen Text: entweder einen Liebesbrief ODER ein Liebesgedicht. "
            f"Generiere KEINEN TITEL wie 'Liebesbrief' oder 'Liebesgedicht'. "
            f"Beschränke den Liebesbrief auf maximal acht Zeilen. "
            f"Beschränke das Liebesgedicht auf maximal zwei Strophen zu je vier Versen. "
            f"Die Texte sollen geschlechterneutral sein und KEINE Gendersternchen oder ähnliches enthalten. "
            f"Die Texte sollen sich im Stil des {era}. Jahrhunderts mit einem {tone} Tonfall anlehnen. "
            "Nutze dafür folgende Stilanweisungen: "
            "Klassisch-romantisch: sehnsuchtsvoll, schwärmerisch, zärtlich, leidenschaftlich. "
            "Feierlich-kunstvoll: würdevoll, pathetisch, höfisch-galant, ergeben/dienend. "
            "Verspielt-leicht: witzig, humorvoll, augenzwinkernd, flirtend, innlich, melancholisch. "
            "Dunkel-dramatisch: schmerzhaft, klagend, schicksalsergeben, tragisch. "
            "Orientiere dich gerne auch an den verschiedenen Epochen: "
            "Barock (1600-1720); Aufklärung (1720-1800); Empfindsamkeit (1740-1790); Sturm und Drang (1765-1785); "
            "Weimarer Klassik (1786-1805); Romantik (1795-1835); Biedermeier (1815-1845); Vormärz (1825-1848); "
            "Realismus (1850-1890); Naturalismus (1880-1900); Moderne (1890-1920); Expressionismus (1910-1925); "
            "Avantgarde/Dadaismus (1915-1925); Nachkriegsliteratur (1945-1960); Neue Subjektivität (seit 1970); "
            "Postmoderne (seit 1980)."
        )

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
