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
            f"Generiere KEINE PLATZHALTER wie 'Dein Name' oder ähnliches. "
            f"Beschränke den Liebesbrief auf maximal acht Zeilen und 80 Wörter. "
            f"Beschränke das Liebesgedicht auf maximal zwei Strophen zu je vier Versen. "
            f"Verfasse einen Liebesbrief nur als Prosatext und ein Liebesgedicht nur in Versform. "
            f"Die Texte sollen geschlechterneutral sein und KEINE Gendersternchen oder ähnliches enthalten. "
            f"Die Texte sollen sich im Stil des {era}. Jahrhunderts mit einem {tone} Tonfall anlehnen. "
            f"Nutze dafür folgende Stilanweisungen: "
            f"Klassisch-romantisch: sehnsuchtsvoll, schwärmerisch, zärtlich, leidenschaftlich. "
            f"Feierlich-kunstvoll: würdevoll, pathetisch, höfisch-galant, ergeben/dienend. "
            f"Verspielt-leicht: witzig, humorvoll, augenzwinkernd, flirtend, innlich, melancholisch. "
            f"Dunkel-dramatisch: schmerzhaft, klagend, schicksalsergeben, tragisch. "
            f"Orientiere dich gerne auch an den verschiedenen Epochen: "
            f"Barock (1600-1720); Aufklärung (1720-1800); Empfindsamkeit (1740-1790); Sturm und Drang (1765-1785); "
            f"Weimarer Klassik (1786-1805); Romantik (1795-1835); Biedermeier (1815-1845); Vormärz (1825-1848); "
            f"Realismus (1850-1890); Naturalismus (1880-1900); Moderne (1890-1920); Expressionismus (1910-1925); "
            f"Avantgarde/Dadaismus (1915-1925); Nachkriegsliteratur (1945-1960); Neue Subjektivität (seit 1970); "
            f"Postmoderne (seit 1980)."
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
