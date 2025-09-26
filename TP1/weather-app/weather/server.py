import os
import time
import logging
from concurrent import futures

import grpc
import requests

import weather_pb2
import weather_pb2_grpc

logging.basicConfig(level=logging.INFO)
OPEN_METEO = "https://api.open-meteo.com/v1/forecast"

class WeatherService(weather_pb2_grpc.WeatherServiceServicer):
    def GetWeather(self, request, context):
        lat = request.latitude
        lon = request.longitude
        try:
            url = (
                f"{OPEN_METEO}"
                f"?latitude={lat}&longitude={lon}"
                f"&current_weather=true"
            )
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            cw = data.get("current_weather")
            if not cw:
                context.abort(grpc.StatusCode.FAILED_PRECONDITION, "No current_weather in response")
            logging.info(f"[weather] ({lat}, {lon}) -> {cw}")
            return weather_pb2.WeatherResponse(
                temperature=float(cw["temperature"]),
                windspeed=float(cw["windspeed"]),
                winddirection=int(cw["winddirection"]),
                weathercode=int(cw["weathercode"]),
                time=str(cw["time"]),
            )
        except requests.exceptions.RequestException as e:
            logging.exception("Network error calling open-meteo")
            context.abort(grpc.StatusCode.UNAVAILABLE, f"open-meteo unreachable: {e}")
        except Exception as e:
            logging.exception("Unexpected error")
            context.abort(grpc.StatusCode.INTERNAL, str(e))

def serve():
    port = os.environ.get("PORT", "50052")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherService(), server)
    server.add_insecure_port(f"[::]:{port}")
    logging.info(f"WeatherService gRPC listening on {port}")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
