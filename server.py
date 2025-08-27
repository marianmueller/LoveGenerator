# Import the Flask web framework
from flask import Flask, request, jsonify

# Create a Flask application instance. This is what Gunicorn looks for.
app = Flask(__name__)

# The endpoint (the "address") that your website calls
@app.route('/generate', methods=['POST'])
def generate_text():
    # Get the data from your website's request
    data = request.get_json()
    text_type = data.get('text_type')
    era = data.get('era')

    # Simulate the AI response. This is for testing the connection.
    if text_type == 'Liebesgedicht' and era == '17':
        generated_text = "Ein Liebesgedicht aus dem 17. Jahrhundert."
    else:
        generated_text = "Ein generierter Text."

    # Return the response as JSON to your website
    return jsonify({"text": generated_text})

# Gunicorn will run the "app" object directly, so the following block is not needed for Render.
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=10000)
