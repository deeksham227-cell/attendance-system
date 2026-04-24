from flask import Flask, jsonify
from flask_cors import CORS
from database import create_tables
from routes.register import register_bp
from routes.recognize import recognize_bp
from routes.attendance import attendance_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(register_bp)
app.register_blueprint(recognize_bp)
app.register_blueprint(attendance_bp)

@app.route("/live", methods=["GET"])
def live_attendance():
    try:
        from live_camera import start_live_attendance
        import threading
        thread = threading.Thread(target=start_live_attendance)
        thread.daemon = True
        thread.start()
        return jsonify({"status": "success", "message": "Live camera started!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("✅ Creating database tables...")
    create_tables()
    print("✅ Starting Flask server...")
    app.run(debug=True, host="0.0.0.0", port=5000)