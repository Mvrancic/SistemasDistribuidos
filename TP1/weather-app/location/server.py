import os
import time
import logging
from concurrent import futures

import grpc
import requests

import location_pb2
import location_pb2_grpc

logging.basicConfig(level=logging.INFO)
IPWHO_BASE = "https://ipwho.is"

class LocationService(location_pb2_grpc.LocationServiceServicer):
    def GetLocation(self, request, context):
        ip = (request.ip or "").strip()

        if not ip:
            url = f"{IPWHO_BASE}"
        else:
            url = f"{IPWHO_BASE}/{ip}"

        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            if not data.get("success", False):
                msg = data.get("message") or "ipwho.is error"
                logging.warning(f"ipwho.is fallback: {msg}")
                # Devolvemos coordenadas de Buenos Aires por defecto
                return location_pb2.LocationResponse(
                    latitude=-34.6037,
                    longitude=-58.3816
                )
            lat = float(data["latitude"])
            lon = float(data["longitude"])
            logging.info(f"[location] {ip or 'auto'} -> ({lat}, {lon})")
            return location_pb2.LocationResponse(latitude=lat, longitude=lon)
        except requests.exceptions.RequestException as e:
            logging.exception("Network error calling ipwho.is")
            # En caso de error de red, también devolvemos Buenos Aires
            logging.warning("Using Buenos Aires as fallback due to network error")
            return location_pb2.LocationResponse(
                latitude=-34.6037,
                longitude=-58.3816
            )
        except Exception as e:
            logging.exception("Unexpected error")
            # En caso de cualquier otro error, también devolvemos Buenos Aires
            logging.warning("Using Buenos Aires as fallback due to unexpected error")
            return location_pb2.LocationResponse(
                latitude=-34.6037,
                longitude=-58.3816
            )

def serve():
    port = os.environ.get("PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationService(), server)
    server.add_insecure_port(f"[::]:{port}")
    logging.info(f"LocationService gRPC listening on {port}")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
