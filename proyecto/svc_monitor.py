#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)
server.send(bytes('00010sinitmonis','utf-8'))

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux

print("Iniciado servicio de monitor de stock")
recibido=server.recv(4096)

while True:
    datos=server.recv(4096)
    if datos.decode('utf-8').find('offmn')!=-1:
        encendido = False
    if datos.decode('utf-8').find('monis')!=-1:
        encendido = True
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        session_mail = data[1]
        while encendido:
            query = f"SELECT productos.id, data_productos.nombre, productos.stock FROM productos, data_productos, inventarios WHERE productos.id = data_productos.id AND productos.inventario = inventarios.id AND inventarios.admin_mail = '{session_mail}'"

            query = query.replace(" ", "-")
            monis_data = "monitor "+session_mail+ " " +query

            aux = fill(len(monis_data+ 'dbget'))
            msg = aux + 'dbget' + monis_data

            server.sendall(bytes(msg,'utf-8'))
            recibido=server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("DEBUG MONITOR: " + recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'fallo_monitor':
                    print("Error al monitorear stock")
                    server.sendall(bytes('00010monis0','utf-8'))
                else:
                    #print("Stock monitoreado")
                    server.sendall(bytes('00010monis'+recibido.decode('utf-8'),'utf-8'))
                    time.sleep(15)