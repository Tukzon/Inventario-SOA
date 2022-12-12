#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)
server.sendall(bytes('00010sinitusre1','utf-8'))

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux

print("Iniciado servicio de usuarios")
recibido=server.recv(4096)
print("db: "+recibido.decode('utf-8'))

while True:
    datos=server.recv(4096)
    print("desde usuario: "+datos.decode('utf-8'))
    #REGISTRO DE NUEVO USUARIO
    if datos.decode('utf-8').find('usre1')!=-1:
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        email = data[0]
        password = data[1]
        nombre = data[2]

        print(email)
        print(password)
        print(nombre)

        reg_data = email + " " + password + " " + nombre
        aux = fill(len(reg_data+ 'dbre1'))
        msg = aux + 'dbre1' + reg_data
        print("mensaje enviado: "+msg)
        server.sendall(bytes(msg,'utf-8'))
        recibido=server.recv(4096)
        if recibido.decode('utf-8').find('dbre1')!=-1:
            recibido = recibido[10:]
            if recibido.decode('utf-8') == '1':
                print("Usuario registrado")
            else:
                print("Usuario no registrado")


