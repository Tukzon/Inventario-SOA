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
        print("Se ha recibido un mensaje para productos")
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        print(data)
        tipoTransaccion = data[0]

        if tipoTransaccion == 'registrar':
            mail = data[1]
            idProd = data[2]
            nombre = data[3]
            cantidad = data[4]
            precio = data[5]
            descripcion = data[6]

            subquery = "(SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + mail + "')"
            query = "WITH ins1 AS (INSERT INTO productos (id, inventario, stock ) VALUES ('" + idProd + "', " + subquery + ", '" + cantidad + "') RETURNING id), ins2 AS (INSERT INTO data_productos (id, inventario, nombre, precio, descripcion) VALUES ('" + idProd + "', " + subquery + ", '" + nombre + "', '" + precio + "', '" + descripcion + "') RETURNING id) SELECT * FROM ins1, ins2"

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
        
        if tipoTransaccion == 'leer':
            session_mail = data[1]
            try:
                # Si se envia el id del producto, se busca solo ese producto
                idProd = data[2]
                query = "SELECT productos.id, data_productos.nombre, data_productos.precio, data_productos.descripcion, productos.stock FROM productos INNER JOIN data_productos ON productos.id = data_productos.id INNER JOIN inventarios ON productos.inventario = inventarios.id WHERE productos.id = '" + idProd + "' AND inventarios.admin_mail = '" + session_mail + "'"

            except:
                # Si no se envia el id del producto, se buscan todos los productos activos del usuario
                query = "SELECT productos.id, data_productos.nombre, data_productos.precio, data_productos.descripcion, productos.stock FROM productos INNER JOIN data_productos ON productos.id = data_productos.id INNER JOIN inventarios ON productos.inventario = inventarios.id WHERE inventarios.admin_mail = '" + session_mail + "' AND productos.valido = '1'"
            query = query.replace(" ", "-")

            reg_data = "leerprod "+query
            aux = fill(len(reg_data+ 'dbget'))
            msg = aux + 'dbget' + reg_data
            server.sendall(bytes(msg,'utf-8'))
            recibido=server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("desde producto: "+recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'fallo_leerprod':
                    print("Producto no encontrado")
                    server.sendall(bytes('00010prods0','utf-8'))
                else:
                    print("Producto encontrado")
                    server.sendall(bytes('00010prods1'+recibido.decode('utf-8'),'utf-8'))

        if tipoTransaccion == 'actualizar':
            session_mail = data[1]
            idProd = data[2]
            nombre = data[3]
            precio = data[4]
            cantidad = data[5]
            descripcion = data[6]

            query_list = []
            if nombre != '/':
                query_nombre = "UPDATE data_productos SET nombre = '" + nombre + "' WHERE id = '" + idProd + "' AND inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "')"
                query_nombre = query_nombre.replace(" ", "-")
                query_list.append(query_nombre)
            if precio != '/':
                query_precio = "UPDATE data_productos SET precio = '" + precio + "' WHERE id = '" + idProd + "' AND inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "')"
                query_precio = query_precio.replace(" ", "-")
                query_list.append(query_precio)
            if cantidad != '/':
                query_cantidad = "UPDATE productos SET stock = '" + cantidad + "' WHERE id = '" + idProd + "' AND inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "')"
                query_cantidad = query_cantidad.replace(" ", "-")
                query_list.append(query_cantidad)
            if descripcion != '/':
                query_descripcion = "UPDATE data_productos SET descripcion = '" + descripcion + "' WHERE id = '" + idProd + "' AND inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "')"
                query_descripcion = query_descripcion.replace(" ", "-")
                query_list.append(query_descripcion)

            
            query = "/".join(query_list)
            reg_data = "actualizarprod "+query
            aux = fill(len(reg_data+ 'dbget'))
            msg = aux + 'dbget' + reg_data
            server.sendall(bytes(msg,'utf-8'))
            recibido=server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("desde producto: "+recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'fallo_actualizarprod':
                    print("No se pudo actualizar el producto")
                    server.sendall(bytes('00010prods0','utf-8'))
                else:
                    print("Producto actualizado satisfactoriamente")
                    server.sendall(bytes('00010prods1','utf-8'))

        if tipoTransaccion == 'eliminar':   
            session_mail = data[1]
            permanente = data[2]
            idProd = data[3]

            if permanente == 's':
                query = "DELETE FROM productos WHERE id = '" + idProd + "' AND inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "')"
            elif permanente == 'n':
                query = "UPDATE productos SET valido = '0' WHERE id = '" + idProd + "' AND inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "')"
            else:
                print("Error al eliminar el producto")
                server.sendall(bytes('00010prods0','utf-8'))
                
            query = query.replace(" ", "-")
            reg_data = "eliminarprod "+query
            aux = fill(len(reg_data+ 'dbget'))
            msg = aux + 'dbget' + reg_data
            server.sendall(bytes(msg,'utf-8'))
            recibido=server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("desde producto: "+recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'producto_eliminado':
                    print("Producto eliminado satisfactoriamente")
                    server.sendall(bytes('00010prods1','utf-8'))
                else:
                    print("Producto no eliminado")
                    server.sendall(bytes('00010prods0','utf-8'))

