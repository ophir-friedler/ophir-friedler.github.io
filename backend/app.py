import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    content = data.get("user_input")
    if not content:
        return jsonify({"error": "No input"}), 400
    supabase.table("submissions").insert({"content": content}).execute()
    return jsonify({"message": "Submitted!"}), 200

@app.route("/admin", methods=["POST"])
def admin():
    data = request.get_json()
    if data.get("password") != ADMIN_PASSWORD:
        return jsonify({"error": "Forbidden"}), 403
    response = supabase.table("submissions").select("*").order("created_at", desc=True).execute()
    return jsonify(response.data), 200

@app.route("/")
def home():
    return "API is running"

if __name__ == "__main__":
    app.run()
