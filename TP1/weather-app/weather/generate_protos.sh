#!/usr/bin/env bash
set -euo pipefail
python -m grpc_tools.protoc \
  -I /app/protos \
  --python_out=/app \
  --grpc_python_out=/app \
  /app/protos/weather.proto
