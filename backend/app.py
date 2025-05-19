# ✅ Do this FIRST before any other imports
import eventlet
eventlet.monkey_patch()

# Then import everything else
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from api.routes import api

# === SETUP ===
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Register routes
app.register_blueprint(api)

# === RUN ===
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
