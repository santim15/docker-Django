# Dockerfile
FROM python:3.10-alpine

# directorio dentro del contenedor para el código
WORKDIR /app  
COPY . /app
RUN pip install -r requirements.txt

