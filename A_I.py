import os
from flask import Flask, request, jsonify
from openai import OpenAI

# Инициализация Flask
app = Flask(__name__)

# Получаем API-ключ из переменной окружения
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY не найден. Установи его в Railway → Variables")

# Создаём клиента OpenAI
client = OpenAI(api_key=api_key)

# Маршрут для проверки
@app.route("/", methods=["GET"])
def home():
    return "API запущено! Используй POST /ask для запросов."

# Маршрут для запросов к модели
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Поле 'prompt' обязательно"}), 400

    try:
        response = client.responses.create(
            model="gpt-5",  # можно заменить на gpt-5 если есть доступ
            input=prompt
        )
        return jsonify({"response": response.output_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Railway ждёт, что сервер слушает на 0.0.0.0 и порту из ENV
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
