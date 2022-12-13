#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)
server.send(bytes('00010sinitalert','utf-8'))

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux

print("Iniciado servicio de alertas de stock")
recibido=server.recv(4096)

while True:
    datos = server.recv(4096)
    if datos.decode('utf-8').find('alert')!=-1:
        print("Alerta de stock")
        datos = datos[10:]
        print("DATA DEBUG ALERTA: " + datos.decode('utf-8'))
        target = datos.decode()
        data = target.split()
        session_mail = data[0]
        idProd = data[1]
        stockMin = data[2]

        query = "SELECT productos.id, data_productos.nombre, productos.stock FROM productos, data_productos, inventarios WHERE productos.id = '" + idProd + "' AND productos.inventario = inventarios.id AND inventarios.admin_mail = '" + session_mail + "' AND productos.stock < '" + stockMin + "' AND productos.id = data_productos.id AND data_productos.inventario = productos.inventario"
        query = query.replace(" ", "-")
        
        alert_data ="alertastock " +session_mail + " " + query
        aux = fill(len(alert_data + "dbget"))
        msg = aux + "dbget" + alert_data
        server.send(bytes(msg, 'utf-8'))
        recibido = server.recv(4096)
        if recibido.decode('utf-8').find('dbget')!=-1:
            recibido = recibido[12:]
            print("DEBUG: " + recibido.decode('utf-8'))
            if recibido.decode('utf-8') == 'fallo_alerta':
                print("Error al configurar alerta de stock")
                server.sendall(bytes('00010alert0','utf-8'))
            else:
                print("finish: " + recibido.decode('utf-8'))
                print("Alerta de stock configurada satisfactoriamente")
                server.sendall(bytes('00010alert1','utf-8'))
                
                




