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
            f"Schreibe einen {text_type} im Stil des {era}. Jahrhunderts mit einem {tone} Tonfall. "
            f"Du kannst dich hieran orientieren: "
            "Klassisch-romantisch bedeutet z.B. sehnsuchtsvoll – voller Fernweh und unerfüllter Liebe oder schwärmerisch – verträumt, begeistert, idealisierend oder zärtlich – sanft, warmherzig, liebevoll oder leidenschaftlich – intensiv, brennend, fast dramatisch; "
            "Feierlich-kunstvoll bedeutet z.B. feierlich – würdevoll, erhaben, fast wie eine Hymne oder pathetisch – mit großer Geste, überbordend, rhetorisch oder höfisch-galant – charmant, elegant, höflich-unterwerfend oder ergeben/dienend – unterwürfig, voller Hingabe; "
            "Verspielt-leicht bedeutet z.B. verspielt – mit Witz, Leichtigkeit, kleinen Neckereien oder neckisch – humorvoll, augenzwinkernd, flirtend oder innlich – körpernah, anspielungsreich, ohne derb zu sein oder melancholisch – sanfte Traurigkeit, bittersüße Note; "
            "Dunkel-dramatisch bedeutet z.B. dramatisch – von Schmerz, Trennung, Gefahr überschattet oder klagend – voller Wehmut, fast wie eine Klage oder schicksalsergeben – – tragisch, von Unausweichlichkeit geprägt. "
            "Die älteren Gedichte dürfen auch gerne älter und die modernen Gedichte moderner klingen. Orientiere dich gerne auch an den verschiedenen Epochen: "
            "Barock 1600 bis 1720; Aufklärung 1720 bis 1800; Empfindsamkeit 1740 bis 1790; Sturm und Drang 1765 bis 1785; Weimarer Klassik 1786 bis 1805; Romantik 1795 bis 1835; Biedermeier 1815 bis 1845; Vormärz 1825 bis 1848; Realismus 1850 bis 1890; "
            "Naturalismus 1880 bis 1900; Moderne 1890 bis 1920; Expressionismus 1910 bis 1925; Avantgarde/Dadaismus 1915 bis 1925; Nachkriegsliteratur 1945 bis 1960; Neue Subjektivität seit 1970; Postmoderne seit 1980. "
            "Die Texte dürfen sich sehr gerne der Ausdrucksweisen des jeweils ausgewählten Jahrhunderts bedienen. Die Texte sollen geschlechterneutral sein; bitte keine Gendersternchen oder ähnliches, sondern wirklich neutral. "
            "Bitte unbedingt maximal acht Zeilen für einen Liebesbrief und zwei Strophen zu je vier Versen für ein Liebesgedicht. Bitte nur eines erstellen, also entweder Liebesgedicht oder Liebesbrief. Bitte alle ohne Titel und ohne Überschrift!"
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
