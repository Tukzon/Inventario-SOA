#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)
server.sendall(bytes('00010sinitusers','utf-8'))

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux

print("Iniciado servicio de usuarios")
recibido=server.recv(4096)

while True:
    datos=server.recv(4096)
    #print("desde usuario: "+datos.decode('utf-8'))
    #REGISTRO DE NUEVO USUARIO
    if datos.decode('utf-8').find('users')!=-1:
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        tipoTransaccion = data[0]
        email = data[1]
        password = data[2]
        nombre = data[3]

        if tipoTransaccion == 'registrar':
            query = "INSERT INTO usuarios (email, password, nombre) VALUES ('" + email + "', '" + password + "', '" + nombre + "')"
            query = query.replace(" ", "-")
            reg_data = "registrar "+email+ " "+query
            aux = fill(len(reg_data+ 'dbget'))
            msg = aux + 'dbget' + reg_data
            #print("mensaje enviado: "+msg)
            server.sendall(bytes(msg,'utf-8'))
            recibido=server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("desde usuario: "+recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'usuario_registrado':
                    print("Usuario registrado satisfactoriamente")
                    server.sendall(bytes('00010users1','utf-8'))
                else:
                    print("Error al registrar usuario")
                    server.sendall(bytes('00010users0','utf-8'))


