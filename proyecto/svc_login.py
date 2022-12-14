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
#print("login: "+recibido.decode('utf-8'))

while True:
    datos=server.recv(4096)
    #print(datos)
    if datos.decode('utf-8').find('login')!=-1:
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        email = data[0]
        password = data[1]

        query = "SELECT * FROM usuarios WHERE email = '" + email + "' AND password = '" + password + "'"
        query = query.replace(" ", "-")
        login_data = "iniciarsesion "+query

        aux = fill(len(login_data+ 'dbget'))
        msg = aux + 'dbget' + login_data
        #print("mensaje enviado: "+msg)
        server.sendall(bytes(msg,'utf-8'))
        recibido=server.recv(4096)
        if recibido.decode('utf-8').find('dbget')!=-1:
            recibido = recibido[12:]
            if recibido.decode('utf-8') == 'sesion_iniciada':
                print("Usuario logueado")
                server.sendall(bytes('00010login1','utf-8'))
            elif recibido.decode('utf-8') == 'fallo_login':
                print("Credenciales ingresadas no son correctas")
                server.sendall(bytes('00010login0','utf-8'))
                
