#!/bin/bash

function start_service {
  while true; do
    python3 $1 &
    PID=$!
    trap "kill $PID" SIGINT SIGTERM
    if wait $PID; then
      echo "$1 exited successfully"
    else
      echo "$1 exited with an error"
    fi
  done
  exit 0
}

echo "================================"
echo "Inicializando todos los servicios"
echo "================================"

start_service svc_db.py &
start_service svc_login.py &
start_service svc_usuarios.py &
start_service svc_productos.py &
start_service svc_alerta.py &
start_service svc_confirmar.py