from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = "a171bca004084e3780e15c6f24f9a22e"

@app.route('/news')
def get_news():
    sujet = request.args.get('q', '')
    if not sujet:
        return jsonify({"error": "Missing 'q' parameter"}), 400
    
    url = f"https://newsapi.org/v2/everything?q={sujet}&language=fr&sortBy=publishedAt&pageSize=12&apiKey={API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
