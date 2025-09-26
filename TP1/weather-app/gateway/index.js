const express = require("express");
const grpc = require("@grpc/grpc-js");
const { loadProto } = require("./protoload");

const app = express();

const LocationPkg = loadProto("location.proto", "location");
const WeatherPkg  = loadProto("weather.proto",  "weather");

const locationClient = new LocationPkg.LocationService(
  "location:50051",
  grpc.credentials.createInsecure()
);

const weatherClient = new WeatherPkg.WeatherService(
  "weather:50052",
  grpc.credentials.createInsecure()
);

// Endpoint HTTP público
app.get("/weather", (req, res) => {
  let ip = (req.query.ip || "").toString().trim();
  if (!ip) {
    // ipwho.is soporta request sin IP → detecta la pública automáticamente
    ip = "";
  }

  locationClient.GetLocation({ ip }, (locErr, locRes) => {
    if (locErr) {
      const code = locErr.code === 3 ? 400 : 502;
      return res.status(code).json({ error: "location", detail: locErr.message });
    }

    weatherClient.GetWeather(
      { latitude: locRes.latitude, longitude: locRes.longitude },
      (wErr, wRes) => {
        if (wErr) {
          return res.status(502).json({ error: "weather", detail: wErr.message });
        }
        return res.json({
          ip: ip || "auto",
          coordinates: { latitude: locRes.latitude, longitude: locRes.longitude },
          weather: wRes
        });
      }
    );
  });
});

app.get("/health", (_req, res) => res.json({ ok: true }));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Gateway HTTP listening on ${PORT}`);
});
