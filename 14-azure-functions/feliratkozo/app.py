import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

FUNCTION_URL = os.getenv("FUNCTION_URL")
if not FUNCTION_URL:
    raise RuntimeError("Hiányzik a FUNCTION_URL a .env fájlból vagy a környezeti változókból.")

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/subscribe")
def subscribe():
    try:
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            return jsonify({"ok": False, "error": "Név és email kötelező"}), 400

        # Továbbítás az Azure Function-nek (HTTP trigger, Anonymous)
        payload = {"name": name, "email": email}
        resp = requests.post(FUNCTION_URL, json=payload, timeout=10)

        # Válasz vissza a böngészőnek
        try:
            data = resp.json()
        except Exception:
            data = {"raw": resp.text}

        return jsonify({
            "ok": resp.ok,
            "status": resp.status_code,
            "function_response": data
        }), resp.status_code

    except requests.Timeout:
        return jsonify({"ok": False, "error": "Azure Function timeout"}), 504
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    # Lokálisan fussunk a 5000-es porton
    app.run(host="127.0.0.1", port=5000)
