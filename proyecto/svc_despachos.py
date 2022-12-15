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
        

        if tipoTransaccion == 'registrar':
            session_mail = data[1]
            email_responsable = data[2]
            direccion = data[3]
            comprador = data[4]
            productos = data[5]
            cantidad = data[6]

            productos = productos.split("-")
            cantidad = cantidad.split("-")

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

        elif tipoTransaccion == 'leer':
            session_mail = data[1]
            despID = data[2]

            if despID == '0':
                query = "SELECT * FROM despachos WHERE inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "') AND valido = '1'"
            else:
                query = "SELECT * FROM despachos WHERE inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "') AND id = " + despID + " AND valido = '1'"
            
            query = query.replace(" ", "-")
            despacho_data = "leerdespacho " + query
            aux = fill(len(despacho_data + "dbget"))
            msg = aux + "dbget" + despacho_data
            server.sendall(bytes(msg, 'utf-8'))
            recibido = server.recv(4096)

            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("DEBUG: " + recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'fallo_leerdespacho':
                    print("Error al leer despacho")
                    server.sendall(bytes('00010despa0','utf-8'))
                elif recibido.decode('utf-8') == 'no_match':
                    print("Comprador no coincide con el inventario")
                    server.sendall(bytes('00010despa2','utf-8'))
                else:
                    print("Despacho leido satisfactoriamente")
                    server.sendall(bytes('00010despa1'+recibido.decode('utf-8'),'utf-8'))

        elif tipoTransaccion == 'eliminar':
            session_mail = data[1]
            permanente = data[2]
            despID = data[3]
            print(permanente)
            if "s" in permanente.lower():
                query = "DELETE FROM despachos WHERE inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "') AND id = " + despID
            else:
                query = "UPDATE despachos SET valido = '0' WHERE inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "') AND id = " + despID
            
            query = query.replace(" ", "-")
            despacho_data = "eliminardespacho " + query
            aux = fill(len(despacho_data + "dbget"))
            msg = aux + "dbget" + despacho_data
            server.sendall(bytes(msg, 'utf-8'))
            recibido = server.recv(4096)

            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("DEBUG: " + recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'despacho_eliminado':
                    print("Se ha eliminado el despacho satisfactoriamente")
                    server.sendall(bytes('00010despa1','utf-8'))
                else:
                    print("Error al eliminar despacho")
                    server.sendall(bytes('00010despa0','utf-8'))

        elif tipoTransaccion == 'actualizar':
            session_mail = data[1]
            despID = data[2]
            direccion = data[3]
            responsable = data[4]
            comprador = data[5]
            prods = data[6]
            cantidad = data[7]

            query = []

            if direccion != '/':
                subquery = "UPDATE despachos SET direccion = '" + direccion + "' WHERE inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "') AND id = " + despID
                subquery = subquery.replace(" ", "-")
                query.append(subquery)
            if responsable != '/':
                subquery = "UPDATE despachos SET responsable = '" + responsable + "' WHERE inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "') AND id = " + despID
                subquery = subquery.replace(" ", "-")
                query.append(subquery)
            if comprador != '/':
                subquery = "UPDATE despachos SET comprador = '" + comprador + "' WHERE inventario = (SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "') AND id = " + despID
                subquery = subquery.replace(" ", "-")
                query.append(subquery)
            if prods != '/':
                prods = prods.split('-')
                presubquery = "(SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "')"
                subquery = f"UPDATE despachos SET productos = ARRAY{prods}::integer[] WHERE inventario = {presubquery} AND id = " + despID
                subquery = subquery.replace(" ", "-")
                query.append(subquery)
            if cantidad != '/':
                cantidad = cantidad.split('-')
                presubquery = "(SELECT inventarios.id FROM inventarios WHERE inventarios.admin_mail = '" + session_mail + "')"
                subquery = f"UPDATE despachos SET cantidad = ARRAY{cantidad}::integer[] WHERE inventario = {presubquery} AND id = " + despID
                subquery = subquery.replace(" ", "-")
                query.append(subquery)

            query = "/".join(query)
            despacho_data = "actualizardespacho " + query
            aux = fill(len(despacho_data + "dbget"))
            msg = aux + "dbget" + despacho_data
            server.sendall(bytes(msg, 'utf-8'))
            recibido = server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("DEBUG: " + recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'despacho_actualizado':
                    print("Se ha actualizado el despacho satisfactoriamente")
                    server.sendall(bytes('00010despa1','utf-8'))
                else:
                    print("Error al actualizar despacho")
                    server.sendall(bytes('00010despa0','utf-8'))

            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("DEBUG: " + recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'despacho_actualizado':
                    print("Se ha actualizado el despacho satisfactoriamente")
                    server.sendall(bytes('00010despa1','utf-8'))
                else:
                    print("Error al actualizar despacho")
                    server.sendall(bytes('00010despa0','utf-8'))
