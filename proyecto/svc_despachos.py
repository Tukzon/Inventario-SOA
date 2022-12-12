#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)
server.send(bytes('00010sinitdespa','utf-8'))

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux

print("Iniciado servicio de despachos")
recibido=server.recv(4096)

while True:
    datos=server.recv(4096)
    #print(datos)
    if datos.decode('utf-8').find('despa')!=-1:
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        tipoTransaccion = data[0]
        session_mail = data[1]
        email_responsable = data[2]
        direccion = data[3]
        comprador = data[4]
        productos = data[5]

        productossplitarray = ""
        cantidadsplitarray = ""

        if tipoTransaccion == 'registrar':
            #SEPARAR VALORES DE PRODUCTOS EN ID - CANTIDAD PARA APLICAR EN QUERY
            subquery = "(SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "')"
            query = "INSERT INTO despachos (inventario, productos, cantidad, direccion, responsable, comprador) VALUES (" + subquery + ", '" + productossplitarray + "', '" + cantidadsplitarray + "', '" + direccion + "', '" + email_responsable + "', '" + comprador + "')"
            
