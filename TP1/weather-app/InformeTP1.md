1. DESCRIPCION GENERAL

Este proyecto implementa una aplicación distribuida para consultar el clima a partir de una dirección IP.
La arquitectura está basada en microservicios, cada uno con una responsabilidad única:

Location Service (Python + gRPC):

Recibe una IP.

Usa la API pública ipwho.is
 para obtener latitud y longitud.

En caso de error o IP inválida, devuelve coordenadas de Buenos Aires como fallback.

Weather Service (Python + gRPC):

Recibe coordenadas (lat, lon).

Usa la API Open-Meteo
 para obtener clima actual.

Devuelve temperatura, viento, dirección del viento, código de clima y timestamp.

Gateway (Node.js + Express):

Único servicio que expone HTTP.

Endpoint: /weather?ip=<IP> o /weather (auto-detección).

Orquesta la comunicación entre Location y Weather usando gRPC.

Devuelve un JSON consolidado con la IP, coordenadas y clima.

Orquestación (Docker Compose):

Los tres servicios se corren como contenedores.

Solo el Gateway expone un puerto al host (3000).

La comunicación interna es por red de Docker.

2.  APIS UTILIZADAS

ipwho.is: geolocalización por IP. No requiere autenticación.

Open-Meteo: consulta de clima actual por coordenadas. API gratuita.

3. CONTRATOS gRPC:

Location Service
rpc GetLocation(LocationRequest) returns (LocationResponse);

message LocationRequest { string ip = 1; }
message LocationResponse { double latitude = 1; double longitude = 2; }

Weather Service
rpc GetWeather(WeatherRequest) returns (WeatherResponse);

message WeatherRequest { double latitude = 1; double longitude = 2; }
message WeatherResponse {
  double temperature = 1;
  double windspeed = 2;
  double winddirection = 3;
  int32 weathercode = 4;
  string time = 5;
}

4. FLUJO DE EJECUCION

Cliente hace request HTTP a GET /weather (con o sin parámetro ip).

El Gateway invoca a LocationService.GetLocation.

Si no se pasa IP, ipwho.is intenta detectar la IP pública.

Si falla, el servicio retorna coordenadas de Buenos Aires como fallback.

El Gateway invoca a WeatherService.GetWeather con las coordenadas obtenidas.

Devuelve al cliente un JSON consolidado con la IP, coordenadas y clima.