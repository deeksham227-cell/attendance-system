from flask import Blueprint, request, jsonify
from database import add_student
from face_engine import save_face_image, train_faces

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    try:
        # Get name from request
        name = request.form.get("name")

        if not name:
            return jsonify({"status": "error", "message": "Name is required!"}), 400

        # Get image file from Flutter
        if "image" not in request.files:
            return jsonify({"status": "error", "message": "Image is required!"}), 400

        image_file = request.files["image"]
        image_data = image_file.read()

        # Save face image
        save_face_image(name, image_data)

        # Add student to database
        add_student(name)

        # Re-train with new face
        total = train_faces()

        return jsonify({
            "status": "success",
            "message": f"{name} registered successfully!",
            "total_faces": total
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500