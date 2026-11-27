
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pathlib import Path
from datetime import datetime, timezone
import sqlite3

HERE = Path(__file__).resolve().parent
DB = HERE / "orion_sort.db"

app = Flask(__name__)
app.secret_key = "local-demo-key-change-before-deployment"

CATEGORIES = {"plastic", "metal", "paper", "cardboard", "unknown"}


def connect():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                weight_g REAL,
                confidence REAL,
                destination TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_event(category, weight, confidence, status):
    destination = (
        "unknown" if category == "unknown"
        else "bin_" + category
    )

    with connect() as db:
        cursor = db.execute("""
            INSERT INTO events
            (category, weight_g, confidence, destination, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            category,
            weight,
            confidence,
            destination,
            status,
            datetime.now(timezone.utc).isoformat()
        ))

        return cursor.lastrowid


@app.route("/")
def index():
    with connect() as db:
        events = db.execute("""
            SELECT * FROM events
            ORDER BY id DESC LIMIT 20
        """).fetchall()

        stats = db.execute("""
            SELECT category,
                   COUNT(*) AS n,
                   COALESCE(SUM(weight_g), 0) AS grams
            FROM events
            GROUP BY category
        """).fetchall()

        total = db.execute(
            "SELECT COUNT(*) FROM events"
        ).fetchone()[0]

    return render_template(
        "index.html",
        events=events,
        stats=stats,
        total=total
    )


@app.post("/demo/add")
def add_demo():
    category = request.form.get("category", "unknown")

    if category not in CATEGORIES:
        flash("Catégorie invalide.")
        return redirect(url_for("index"))

    try:
        weight = float(request.form.get("weight_g", "0"))
        confidence = float(request.form.get("confidence", "0"))

        if weight < 0 or not 0 <= confidence <= 1:
            raise ValueError

    except (ValueError, TypeError):
        flash("Poids ou confiance invalide.")
        return redirect(url_for("index"))

    save_event(category, weight, confidence, "DEMO")

    flash("Événement de démonstration enregistré.")
    return redirect(url_for("index"))


@app.post("/api/detection")
def api_detection():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "JSON invalide."
        }), 400

    category = str(data.get("category", "")).lower()

    if category not in CATEGORIES:
        return jsonify({
            "success": False,
            "error": "Catégorie inconnue."
        }), 400

    try:
        weight = float(data.get("weight_g", 0))
        confidence = float(data.get("confidence", 0))

        if weight < 0 or not 0 <= confidence <= 1:
            raise ValueError

    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Poids ou confiance invalide."
        }), 400

    event_id = save_event(
        category,
        weight,
        confidence,
        "AI"
    )

    return jsonify({
        "success": True,
        "message": "Détection IA enregistrée.",
        "event_id": event_id,
        "category": category
    }), 201


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "demo",
        "hardware_connected": False,
        "ai_api_available": True
    }

# --- AJOUTE CETTE ROUTE DANS TON APP.PY ---
import cv2
from flask import Response

# On charge le modèle une deuxieme fois pour le flux (ou on utilise le même que le script séparé)
# Pour simplifier, on va faire un flux vidéo simple sans IA dessus (l'IA est gérée par camera_ai.py)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
# ------------------------------------------
if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
