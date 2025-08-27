import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Dies ist neu
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Dies ist neu

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        text_type = data.get('text_type')
        era = data.get('era')
        tone = data.get('tone')
        
        prompt = f"Schreibe einen {text_type} im Stil des {era}. Jahrhunderts mit einem {tone} Tonfall. Du kannst dich hieran orientieren: Klassisch-romantisch bedeutet z.B. sehnsuchtsvoll – voller Fernweh und unerfüllter Liebe oder schwärmerisch – verträumt, begeistert, idealisierend oder zärtlich – sanft, warmherzig, liebevoll oder leidenschaftlich – intensiv, brennend, fast dramatisch; Feierliche-kunstvoll bedeutet z.B. feierlich – würdevoll, erhaben, fast wie eine Hymne oder pathetisch – mit großer Geste, überbordend, rhetorisch oder höfisch-galant – charmant, elegant, höflich-unterwerfend oder ergeben/dienend – unterwürfig, voller Hingabe; Verspielt-leicht bedeutet z.B. verspielt – mit Witz, Leichtigkeit, kleinen Neckereien oder neckisch – humorvoll, augenzwinkernd, flirtend oder innlich – körpernah, anspielungsreich, ohne derb zu sein oder melancholisch – sanfte Traurigkeit, bittersüße Note; Dunkel-dramatisch bedeutet z.B. dramatisch – von Schmerz, Trennung, Gefahr überschattet oder klagend – voller Wehmut, fast wie eine Klage oder schicksalsergeben – tragisch, von Unausweichlichkeit geprägt. Die Texte sollen geschlechterneutral sein. Die Texte dürfen sich sehr gerne der Ausdrucksweisen des jeweils ausgewählten Jahrhunderts bedienen. Bitte maximal acht Zeilen für einen Liebesbrief oder zwei Strophen zu je vier Versen für ein Liebesgedicht."
        
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
