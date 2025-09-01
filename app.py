from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "API запущено! Используй POST /ask для запросов."

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Отсутствует поле 'prompt'"}), 400

        prompt = data["prompt"]

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # или gpt-4, если есть доступ
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content
        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
print("RAW DATA:", request.data)
print("JSON:", request.get_json(silent=True))
