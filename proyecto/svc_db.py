#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import psycopg2

#AÑADIR CONEXION A BASE DE DATOS
db = psycopg2.connect(host="postgres", database="inventario", user="postgres", password="postgres")
cursor = db.cursor()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)
server.send(bytes('00010sinitdbget','utf-8'))

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux

print("Iniciado servicio de base de datos")
recibido=server.recv(4096)

while True:
    datos=server.recv(4096)
    #print("desde db: "+datos.decode('utf-8'))
    if datos.decode('utf-8').find('dbget')!=-1:
        print("Petición realizada a la base de datos")
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        tipoTransaccion = data[0]
        query = data[1]
        query = query.replace("-", " ")
        
        if tipoTransaccion == "iniciarsesion":
            try:
                cursor.execute(query)
                row = cursor.fetchone()
                if row is None:
                    server.sendall(bytes('00010dbgetfallo_login','utf-8'))
                else:
                    server.sendall(bytes('00010dbgetsesion_iniciada','utf-8'))
            except:
                server.sendall(bytes('00010dbgetfallo_login','utf-8'))

        if tipoTransaccion == "registrar":
            try:
                query = data[2]
                query = query.replace("-", " ")
                mail = data[1]
                cursor.execute(query)
                cursor.execute("INSERT INTO inventarios (admin_mail, nombre) VALUES ('" + mail + "', 'inventario_"+mail + "')")
                db.commit()
                server.sendall(bytes('00010dbgetusuario_registrado','utf-8'))
            except:
                db.rollback()
                server.sendall(bytes('00010dbgetfallo_registro','utf-8'))

        if tipoTransaccion == "registrarprod":
            try:
                cursor.execute(query)
                db.commit()
                server.sendall(bytes('00010dbgetproducto_registrado','utf-8'))
            except:
                db.rollback()
                server.sendall(bytes('00010dbgetproducto_no_registrado','utf-8'))