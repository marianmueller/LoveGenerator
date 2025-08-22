import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# OpenAI Client mit Environment Variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.json
        text_type = data.get('text_type')
        era = data.get('era')
        tone = data.get('tone')
        context = data.get('context', '')
        
        # Validation
        if not text_type or not era or not tone:
            return jsonify({'error': 'Textart, Jahrhundert und Tonfall sind erforderlich'}), 400
        
        prompt = f"Schreibe einen {text_type} im Stil des {era}. Jahrhunderts mit einem {tone} Tonfall. Du kannst dich hieran orientieren: Klassisch-romantisch bedeutet z.B. sehnsuchtsvoll – voller Fernweh und unerfüllter Liebe oder schwärmerisch – verträumt, begeistert, idealisierend oder zärtlich – sanft, warmherzig, liebevoll oder leidenschaftlich – intensiv, brennend, fast dramatisch; Feierliche-kunstvoll bedeutet z.B. feierlich – würdevoll, erhaben, fast wie eine Hymne oder pathetisch – mit großer Geste, überbordend, rhetorisch oder höfisch-galant – charmant, elegant, höflich-unterwerfend oder ergeben/dienend – unterwürfig, voller Hingabe; Verspielt-leicht bedeutet z.B. verspielt – mit Witz, Leichtigkeit, kleinen Neckereien oder neckisch – humorvoll, augenzwinkernd, flirtend oder innlich – körpernah, anspielungsreich, ohne derb zu sein oder melancholisch – sanfte Traurigkeit, bittersüße Note; Dunkel-dramatisch bedeutet z.B. dramatisch – von Schmerz, Trennung, Gefahr überschattet oder klagend – voller Wehmut, fast wie eine Klage oder schicksalsergeben – tragisch, von Unausweichlichkeit geprägt. Die Texte sollen geschlechterneutral sein. Die Texte dürfen sich sehr gerne der Ausdrucksweisen des jeweils ausgewählten Jahrhunderts bedienen. Die Texte sollen bitte alle eine zum jeweiligen Text passende Überschrift bzw. Titel haben."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein kreativer Autor für romantische Texte im deutschen Sprachraum."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=800,
            timeout=30
        )
        
        generated_text = response.choices[0].message.content
        return jsonify({'text': generated_text})
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({'error': 'Ein Fehler ist aufgetreten. Bitte versuche es erneut.'}), 500

if __name__ == '__main__':
    # Lokale Entwicklung
    app.run(debug=True, port=5000)
