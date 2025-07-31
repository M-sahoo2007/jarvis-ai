from flask import Flask, request, jsonify
from flask_cors import CORS
import os, requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "your_api_key_here")
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

@app.route("/api/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        user_prompt = data.get("prompt", "")
        system_prompt = "You are a helpful AI assistant named Jarvis."

        full_prompt = f"{system_prompt}\nUser: {user_prompt}\nAssistant:"

        payload = {
            "model": MODEL,
            "prompt": full_prompt,
            "max_tokens": 300,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50
        }

        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post("https://api.together.xyz/v1/completions", headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            return jsonify({"response": result["choices"][0]["text"].strip()})
        else:
            return jsonify({"response": "Error from Together API"}), 500

    except Exception as e:
        return jsonify({"response": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
