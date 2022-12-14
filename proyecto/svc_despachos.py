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
        cantidad = data[6]

        productos = productos.split("-")
        cantidad = cantidad.split("-")

        if tipoTransaccion == 'registrar':


            subquery = "(SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "')"
            #query = "INSERT INTO despachos (inventario, productos, cantidad, direccion, responsable, comprador) VALUES (" + subquery + ", '" + str(productos) + "', '" + str(cantidad) + "', '" + direccion + "', '" + email_responsable + "', '" + comprador + "')"

            query = f"INSERT INTO despachos (inventario, productos, cantidad, direccion, responsable, comprador) VALUES ({subquery}, ARRAY{productos}::integer[], ARRAY{cantidad}::integer[], '{direccion}', '{email_responsable}', '{comprador}')"

            
            
            #print(query)
            query = query.replace(" ", "-")
            despacho_data ="agregardespacho " +session_mail + " " + query
            aux = fill(len(despacho_data + "dbget"))
            msg = aux + "dbget" + despacho_data
            server.send(bytes(msg, 'utf-8'))
            recibido = server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                #print("DEBUG: " + recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'despacho_no_agregado':
                    print("Error al registrar despacho")
                    server.sendall(bytes('00010despa0','utf-8'))
                else:
                    #print("finish: " + recibido.decode('utf-8'))
                    print("Despacho registrado satisfactoriamente")
                    server.sendall(bytes('00010despa1','utf-8'))
