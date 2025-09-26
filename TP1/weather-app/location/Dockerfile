FROM python:3.11-slim

WORKDIR /app

# Copiamos protos a una ruta común /app/protos
COPY ./protos /app/protos
COPY ./location/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Generamos stubs gRPC
COPY ./location/generate_protos.sh /app/generate_protos.sh
RUN chmod +x /app/generate_protos.sh && /app/generate_protos.sh

# Copiamos el servidor
COPY ./location/server.py /app/server.py

EXPOSE 50051
CMD ["python", "/app/server.py"]
