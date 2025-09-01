from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("input")

    response = client.responses.create(
        model="gpt-5",
        input=user_input
    )

    return jsonify({"response": response.output_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
