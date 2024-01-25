import numpy as np
import psycopg2
import cv2
from PIL import Image as PilImage
from imgbeddings import imgbeddings

# Initialize the face detector and the imgbeddings instance
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
ibed = imgbeddings()

# Establish the database connection
conn = psycopg2.connect("dbname='facial_recognition' user='postgres' host='localhost' port='5433' password='timney'")

# Load and process the image for finding similar images
file_name = "test-image.jpeg"
img = cv2.imread(file_name)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=6, minSize=(30, 30))

# Loop over the face detections
for (x, y, w, h) in faces:
    # Extract the face ROI
    face_roi = img[y:y + h, x:x + w]
    pil_face = PilImage.fromarray(cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB))

    # Calculate embeddings for the detected face
    embedding = ibed.to_embeddings(pil_face)

    # Convert the embedding into a format suitable for comparison in PostgreSQL
    string_representation = embedding[0].tolist()

    # Find similar images in the database
    cur = conn.cursor()
    cur.execute(
        "SELECT filename, vector_embedding <-> %s::vector AS distance FROM pictures ORDER BY distance LIMIT 1;",
        (string_representation,)
    )
    row = cur.fetchone()
    
    # If the distance is within the tolerance, draw a box and label the face
    tolerance = 20  # Adjust this tolerance level to match your dataset's requirements
    print(f"Matched filename: {row[0]}, Distance: {row[1]}")
    if row and row[1] < tolerance:
        text = f"{row[0]}: {row[1]:.2f}"
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

cur.close()
conn.close()

# Resize the image for display if it's too large
scale_percent = 50  # percentage of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

# Display the annotated image
cv2.imshow('Image with Detected Faces', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()