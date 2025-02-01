import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Load known face encodings and their names
anjali_image = face_recognition.load_image_file("WIN_20241215_17_28_23_Pro.jpg")
anjali_encoding = face_recognition.face_encodings(anjali_image)[0]

anjuu_image = face_recognition.load_image_file("WIN_20250120_13_29_12_Pro.jpg")
anjuu_encoding = face_recognition.face_encodings(anjuu_image)[0]
khyathi_image = face_recognition.load_image_file("khyathi.jpg")
khyathi_encoding = face_recognition.face_encodings(khyathi_image)[0]

known_face_encodings = [anjali_encoding, anjuu_encoding,khyathi_encoding]
known_face_names = ["anjali", "anjuu","khyathi"]

# Copy of names to track attendance
students = known_face_names.copy()

# Initialize variables
face_locations = []
face_encodings = []
face_names = []
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

# Create a CSV file for attendance
filename = current_date + '.csv'
with open(filename, 'w', newline='') as f:
    lnwriter = csv.writer(f)
    lnwriter.writerow(["Name", "Time"])

print("Press 'q' to quit the attendance system.")

while True:
    # Capture frame from webcam
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Unable to access the camera.")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect face locations
    face_locations = face_recognition.face_locations(rgb_small_frame)
    if not face_locations:
        # If no faces are detected, continue the loop
        continue

    # Compute face encodings for detected faces
    try:
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    except Exception as e:
        print(f"Error during face encoding: {e}")
        continue

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            face_names.append(name)

            # Mark attendance
            if name in students:
                students.remove(name)
                current_time = now.strftime("%H:%M:%S")
                print(f"Attendance marked for {name} at {current_time}")

                # Write to CSV
                with open(filename, 'a', newline='') as f:
                    lnwriter = csv.writer(f)
                    lnwriter.writerow([name, current_time])

    # Display the video feed with recognized names
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame was scaled down
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Label the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    cv2.imshow("Attendance System", frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
video_capture.release()
cv2.destroyAllWindows()

print(f"Attendance recorded in {filename}.")


