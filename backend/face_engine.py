import face_recognition
import cv2
import os
import pickle
import numpy as np
from database import mark_attendance

def save_face_image(name, image_data):
    folder = f"dataset/{name}"
    os.makedirs(folder, exist_ok=True)
    count = len(os.listdir(folder))
    img_path = f"{folder}/{count + 1}.jpg"
    with open(img_path, "wb") as f:
        f.write(image_data)
    return img_path

def train_faces():
    encodings = []
    names = []
    dataset_path = "dataset"
    for person_name in os.listdir(dataset_path):
        person_folder = os.path.join(dataset_path, person_name)
        if not os.path.isdir(person_folder):
            continue
        for img_file in os.listdir(person_folder):
            img_path = os.path.join(person_folder, img_file)
            image = face_recognition.load_image_file(img_path)
            encoding_list = face_recognition.face_encodings(image)
            if encoding_list:
                encodings.append(encoding_list[0])
                names.append(person_name)
    with open("encodings.pkl", "wb") as f:
        pickle.dump({"encodings": encodings, "names": names}, f)
    return len(names)

def recognize_face(image_data):
    if not os.path.exists("encodings.pkl"):
        return {"status": "error", "message": "No trained faces found!"}
    with open("encodings.pkl", "rb") as f:
        data = pickle.load(f)
    np_array = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    if not face_encodings:
        return {"status": "error", "message": "No face detected!"}
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(
            data["encodings"], face_encoding, tolerance=0.5)
        face_distances = face_recognition.face_distance(
            data["encodings"], face_encoding)
        if True in matches:
            best_index = np.argmin(face_distances)
            name = data["names"][best_index]
            mark_attendance(name)
            return {"status": "success", "name": name}
    return {"status": "unknown", "message": "Face not recognized!"}