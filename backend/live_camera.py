import cv2
import face_recognition
import pickle
import numpy as np
from database import mark_attendance
from datetime import datetime

def start_live_attendance():
    # Check if encodings exist
    if not open("encodings.pkl", "rb"):
        print("No faces registered yet!")
        return

    # Load trained encodings
    with open("encodings.pkl", "rb") as f:
        data = pickle.load(f)

    # Open webcam
    cam = cv2.VideoCapture(0)
    print("✅ Camera started! Press 'q' to quit.")

    marked_today = set()

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        # Resize for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find faces
        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(
                data["encodings"], face_encoding, tolerance=0.5
            )
            name = "Unknown"

            if True in matches:
                face_distances = face_recognition.face_distance(
                    data["encodings"], face_encoding
                )
                best_index = np.argmin(face_distances)
                name = data["names"][best_index]

                # Mark attendance only once per day
                today = datetime.now().strftime("%Y-%m-%d")
                key = f"{name}_{today}"
                if key not in marked_today:
                    mark_attendance(name)
                    marked_today.add(key)
                    print(f"✅ Attendance marked for {name}!")

            # Draw box around face
            top, right, bottom, left = face_location
            top *= 4; right *= 4; bottom *= 4; left *= 4

            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        # Show frame
        cv2.imshow("Live Attendance System", frame)

        # Press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    print("✅ Camera stopped!")

if __name__ == "__main__":
    start_live_attendance()