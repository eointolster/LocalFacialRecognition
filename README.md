To run locally you must have docker desktop running (with this setup)
Build the docker image provided
      docker build -t postgres-pgvector .
Connect to postgresql database
     docker exec -it facial_recognition psql -U postgres
then
     CREATE EXTENSION vector;
then
     CREATE TABLE pictures (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    vector_embedding vector
);

Create a folder called stored-faces.
Run Step1Calculateembeddings.py to create embeddings that go to your postgres database
Run Step2NewFaceScan.py to see the result on an image you have called test-image.jpeg. 
