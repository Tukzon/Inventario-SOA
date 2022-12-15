#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)
server.send(bytes('00010sinitconde','utf-8'))

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux

print("Iniciado servicio de confirmacion de despachos")
recibido=server.recv(4096)

while True:
    datos=server.recv(4096)
    if datos.decode('utf-8').find('conde')!=-1:
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        session_mail = data[0]
        idDesp = data[1]
        recibe = data[2]
        #print(data)
        if len(data) == 4:
            query = "UPDATE despachos SET entregado = '1' WHERE id = '" + idDesp + "' AND entregado = '0'"
            query = query.replace(" ", "-")
            conde_data = "confirmar "+session_mail + " " + recibe + " " + query + " " + str(1)
        else:
            query1 = "SELECT despachos.comprador FROM despachos WHERE id = '" + idDesp + "' AND entregado = '0'"
            query2 = "UPDATE despachos SET entregado = '1' WHERE id = '" + idDesp + "' AND entregado = '0'"
            query1 = query1.replace(" ", "-")
            query2 = query2.replace(" ", "-")
            query = query1 + "/" + query2
            conde_data = "confirmar "+session_mail + " " + recibe + " " + query

        aux = fill(len(conde_data+ 'dbget'))
        msg = aux + 'dbget' + conde_data

        server.sendall(bytes(msg,'utf-8'))
        recibido=server.recv(4096)
        #print(recibido)
        if recibido.decode('utf-8').find('dbget')!=-1:
            recibido = recibido[12:]
            if recibido.decode('utf-8') == 'confirmado':
                print("Despacho confirmado")
                server.sendall(bytes('00010conde1','utf-8'))
            elif recibido.decode('utf-8') == 'no_match':
                print("Comprador no coincide con el inventario")
                server.sendall(bytes('00010conde2','utf-8'))
            elif recibido.decode('utf-8') == 'fallo_confirmacion':
                print("Error al confirmar despacho")
                server.sendall(bytes('00010conde0','utf-8'))
