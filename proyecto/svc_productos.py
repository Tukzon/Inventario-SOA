#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)
server.send(bytes('00010sinitprods','utf-8'))

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux

print("Iniciado servicio de productos")
recibido=server.recv(4096)

while True:
    datos = server.recv(4096)
    if datos.decode('utf-8').find('prods')!=-1:
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        tipoTransaccion = data[0]

        if tipoTransaccion == 'registrar':
            mail = data[1]
            idProd = data[1]
            nombre = data[2]
            cantidad = data[3]
            precio = data[4]
            descripcion = data[5]

            subquery = "(SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + mail + "')"
            query = "WITH ins1 AS (INSERT INTO productos (id, inventario, stock ) VALUES ('" + idProd + "', '" + subquery + "', '" + cantidad + "') RETURNING id), ins2 AS (INSERT INTO data_productos (id, inventario, nombre, precio, descripcion) VALUES ('" + idProd + "', '" + subquery + "', '" + nombre + "', '" + precio + "', '" + descripcion + "') RETURNING id) SELECT * FROM ins1, ins2"

            query = query.replace(" ", "-")
            reg_data = "registrarprod "+query
            aux = fill(len(reg_data+ 'dbget'))
            msg = aux + 'dbget' + reg_data
            server.sendall(bytes(msg,'utf-8'))
            recibido=server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("desde producto: "+recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'producto_registrado':
                    print("Producto registrado satisfactoriamente")
                    server.sendall(bytes('00010prods1','utf-8'))
                else:
                    print("Error al registrar producto")
                    server.sendall(bytes('00010prods0','utf-8'))

