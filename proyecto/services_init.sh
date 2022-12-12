#!/bin/bash
echo "================================"
echo "Inicializando todos los servicios"
echo "================================"
python3 svc_db.py &
python3 svc_login.py &
python3 svc_usuarios.py &
python3 svc_productos.py 