from flask import Flask, send_from_directory
from config import RECORDINGS_DIR
from api.routes import api  # ← make sure this is imported

app = Flask(__name__)

# ✅ Register API Blueprint under `/api`
app.register_blueprint(api, url_prefix="/api")

@app.route("/")
def home():
    return "Flask backend is running"

# Static file routes (covers and audio)
@app.route("/cover/<path:filepath>")
def serve_cover(filepath):
    import os
    return send_from_directory(
        os.path.join(RECORDINGS_DIR, os.path.dirname(filepath)),
        os.path.basename(filepath)
    )

@app.route("/audio/<path:filepath>")
def serve_audio(filepath):
    import os
    return send_from_directory(
        os.path.join(RECORDINGS_DIR, os.path.dirname(filepath)),
        os.path.basename(filepath)
    )

if __name__ == "__main__":
    print("🚀 Flask running at http://localhost:5000")
    app.run(debug=True)
