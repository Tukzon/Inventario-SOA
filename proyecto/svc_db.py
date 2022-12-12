#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import psycopg2

#AÑADIR CONEXION A BASE DE DATOS
db = psycopg2.connect(host="postgres", database="inventario", user="postgres", password="postgres")
cursor = db.cursor()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)
server.send(bytes('00010sinitdblo1','utf-8'))
#server.send(bytes('00010sinitdbre1','utf-8'))

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux

print("Iniciado servicio de base de datos")
recibido=server.recv(4096)

while True:
    datos=server.recv(4096)
    print("desde db: "+datos.decode('utf-8'))
    if datos.decode('utf-8').find('dbre1')!=-1:
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        email = data[0]
        password = data[1]
        nombre = data[2]

        #MODIFICAR ESTO SEGUN DB, ES PARA TESTING
        if email == 'test' and nombre == 'gonzalo':
            #REGISTRADO
            server.send(bytes('00010dbre11','utf-8'))
        else:
            #ERROR
            server.send(bytes('00010dbre10','utf-8'))

    if datos.decode('utf-8').find('dblo1')!=-1:
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        email = data[0]
        password = data[1]

        print(email)
        print(password)

        #MODIFICAR ESTO SEGUN DB, ES PARA TESTING
        if email == 'test':
            #LOGUEADO
            server.sendall(bytes('00010dblo11','utf-8'))
        else:
            #ERROR
            server.sendall(bytes('00010dblo10','utf-8'))