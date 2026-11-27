# Application web — Responsable : Mickael

Prototype Flask local avec base SQLite. Les événements ajoutés depuis le formulaire sont des données de démonstration : aucune connexion ESP32, caméra ou robot n'est encore active.

Installation depuis `web/` :
```bash
python -m venv .venv
# Windows : .venv\Scripts\activate
# Linux/macOS : source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Ouvrir http://127.0.0.1:5000
