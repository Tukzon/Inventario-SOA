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
    #REGISTRO DE NUEVO USUARIO
    if datos.decode('utf-8').find('users')!=-1:
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        tipoTransaccion = data[0]

        if tipoTransaccion == 'registrar':
            email = data[1]
            password = data[2]
            nombre = data[3]
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

        elif tipoTransaccion == 'registrartrabajador':
            session_mail = data[1]
            nombre = data[2]
            email = data[3]
            password = data[4]
            subquery = "(SELECT id FROM inventarios WHERE admin_mail = '" + session_mail + "')"
            query = "INSERT INTO usuarios (email, password, nombre, inventario, tipo) VALUES ('" + email + "', '" + password + "', '" + nombre + "', " + subquery + ", '2')"
            query = query.replace(" ", "-")
            reg_data = "registrart "+query
            aux = fill(len(reg_data+ 'dbget'))
            msg = aux + 'dbget' + reg_data
            #print("mensaje enviado: "+msg)
            server.sendall(bytes(msg,'utf-8'))
            recibido=server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("desde usuario: "+recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'trabajador_registrado':
                    print("Trabajador registrado satisfactoriamente")
                    server.sendall(bytes('00010users1','utf-8'))
                else:
                    print("Error al registrar Trabajador")
                    server.sendall(bytes('00010users0','utf-8'))

        elif tipoTransaccion == 'leer':
            session_mail = data[1]
            query = "SELECT email,nombre,inventario FROM usuarios WHERE inventario = (SELECT id FROM inventarios WHERE admin_mail = '" + session_mail + "')"
            query = query.replace(" ", "-")
            reg_data = "leeruser "+query
            aux = fill(len(reg_data+ 'dbget'))
            msg = aux + 'dbget' + reg_data
            #print("mensaje enviado: "+msg)
            server.sendall(bytes(msg,'utf-8'))
            recibido=server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                #print("DESDE USUARIO BUG: "+recibido.decode('utf-8'))
                #print("desde usuario: "+recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'fallo_leeruser':
                    print("No se encontraron trabajadores")
                    server.sendall(bytes('00010users0','utf-8'))
                else:
                    print("Trabajadores encontrados")
                    server.sendall(bytes('00010users'+recibido.decode('utf-8'),'utf-8'))

        elif tipoTransaccion == 'eliminar':
            session_mail = data[1]
            email = data[2]
            
            query = "DELETE FROM usuarios WHERE email = '" + email + "' AND inventario = (SELECT id FROM inventarios WHERE admin_mail = '" + session_mail + "')"
            query = query.replace(" ", "-")
            reg_data = "eliminaruser "+query
            aux = fill(len(reg_data+ 'dbget'))
            msg = aux + 'dbget' + reg_data
            #print("mensaje enviado: "+msg)
            server.sendall(bytes(msg,'utf-8'))
            recibido=server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("desde usuario: "+recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'usuario_eliminado':
                    print("Usuario eliminado satisfactoriamente")
                    server.sendall(bytes('00010users1','utf-8'))
                else:
                    print("Error al eliminar usuario")
                    server.sendall(bytes('00010users0','utf-8'))

        elif tipoTransaccion == 'actualizar':
            session_mail = data[1]
            email = data[2]
            newCorreo = data[3]
            nombre = data[4]
            password = data[5]

            query_list = []
            if newCorreo != '/':
                subquery = "UPDATE usuarios SET email = '" + newCorreo + "' WHERE email = '" + email + "' AND inventario = (SELECT id FROM inventarios WHERE admin_mail = '" + session_mail + "')"
                query_list.append(subquery)
            if nombre != '/':
                subquery = "UPDATE usuarios SET nombre = '" + nombre + "' WHERE email = '" + email + "' AND inventario = (SELECT id FROM inventarios WHERE admin_mail = '" + session_mail + "')"
                query_list.append(subquery)
            if password != '/':
                subquery = "UPDATE usuarios SET password = '" + password + "' WHERE email = '" + email + "' AND inventario = (SELECT id FROM inventarios WHERE admin_mail = '" + session_mail + "')"
                query_list.append(subquery)
            
            query = "/".join(query_list)
            
            query = query.replace(" ", "-")
            reg_data = "actualizaruser "+query
            aux = fill(len(reg_data+ 'dbget'))
            msg = aux + 'dbget' + reg_data
            #print("mensaje enviado: "+msg)
            server.sendall(bytes(msg,'utf-8'))
            recibido=server.recv(4096)
            if recibido.decode('utf-8').find('dbget')!=-1:
                recibido = recibido[12:]
                print("desde usuario: "+recibido.decode('utf-8'))
                if recibido.decode('utf-8') == 'usuario_actualizado':
                    print("Usuario actualizado satisfactoriamente")
                    server.sendall(bytes('00010users1','utf-8'))
                else:
                    print("Error al actualizar usuario")
                    server.sendall(bytes('00010users0','utf-8'))



