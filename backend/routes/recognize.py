from flask import Blueprint, request, jsonify
from face_engine import recognize_face
from database import mark_attendance

recognize_bp = Blueprint("recognize", __name__)

@recognize_bp.route("/recognize", methods=["POST"])
def recognize():
    try:
        if "image" not in request.files:
            return jsonify({"status": "error", "message": "Image is required!"}), 400
        image_file = request.files["image"]
        image_data = image_file.read()
        result = recognize_face(image_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@recognize_bp.route("/mark", methods=["POST"])
def mark_manual():
    try:
        data = request.get_json()
        name = data.get("name")
        if not name:
            return jsonify({"status": "error", "message": "Name required!"}), 400
        mark_attendance(name)
        return jsonify({
            "status": "success",
            "message": f"Attendance marked for {name}!"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500