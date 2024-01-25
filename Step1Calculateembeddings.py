import numpy as np
from imgbeddings import imgbeddings  # Ensure this is correctly installed and imported.
from PIL import Image
import os
import psycopg2
import cv2

# Establish database connection
conn = psycopg2.connect("dbname='facial_recognition' user='postgres' host='localhost' port='5433' password='timney'")

# Process each image in the stored-faces directory
for filename in os.listdir("stored-faces"):
    img = Image.open(os.path.join("stored-faces", filename))
    ibed = imgbeddings()
    embedding = ibed.to_embeddings(img)
    
    cur = conn.cursor()
    # Ensure your column name in the database is 'vector_embedding' and of type 'vector'
    cur.execute("INSERT INTO pictures(filename, vector_embedding) VALUES (%s, %s::vector)", (filename, embedding[0].tolist()))
    print(filename)
conn.commit()

# Process a single image for finding similar images
file_name = "test-image.jpeg"
img = Image.open(file_name)
ibed = imgbeddings()
embedding = ibed.to_embeddings(img)

cur = conn.cursor()
string_representation = embedding[0].tolist()
# Assuming the column name in the database is 'vector_embedding' of type 'vector'
cur.execute("SELECT * FROM pictures ORDER BY vector_embedding <-> %s::vector LIMIT 1;", (string_representation,))

rows = cur.fetchall()
for row in rows:
    # Display or process the similar image found
    print("Similar image:", row[0])

cur.close()
conn.close()
