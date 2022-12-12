#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)
server.send(bytes('00010sinitlogin','utf-8'))

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux

print("Iniciado servicio de login")
recibido=server.recv(4096)
print("login: "+recibido.decode('utf-8'))

while True:
    datos=server.recv(4096)
    #print(datos)
    if datos.decode('utf-8').find('login')!=-1:
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        email = data[0]
        password = data[1]

        login_data = email + " " + password

        aux = fill(len(login_data+ 'dblo1'))
        msg = aux + 'dblo1' + login_data
        print("mensaje enviado: "+msg)
        server.sendall(bytes(msg,'utf-8'))
        recibido=server.recv(4096)
        print("recibido desde login: "+recibido.decode('utf-8'))
        if recibido.decode('utf-8').find('dblo1')!=-1:
            recibido = recibido[12:]
            print(recibido.decode('utf-8'))
            if recibido.decode('utf-8') == '1':
                print("Usuario logueado")
                #send 1 to cliente to show login success
                server.sendall(bytes('00010login1','utf-8'))
            else:
                print("Usuario no logueado")
                #send 0 to cliente to show login fail
                server.sendall(bytes('00010login0','utf-8'))
                
