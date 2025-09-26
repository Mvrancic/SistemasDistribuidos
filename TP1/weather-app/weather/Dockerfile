FROM python:3.11-slim

WORKDIR /app

COPY ./protos /app/protos
COPY ./weather/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./weather/generate_protos.sh /app/generate_protos.sh
RUN chmod +x /app/generate_protos.sh && /app/generate_protos.sh

COPY ./weather/server.py /app/server.py

EXPOSE 50052
CMD ["python", "/app/server.py"]
