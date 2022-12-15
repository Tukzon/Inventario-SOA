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

alertasActivas = []

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
        
        if tipoTransaccion == "tipo":
            try:
                query = "SELECT tipo FROM usuarios WHERE email = '" + str(data[1]) + "'"
                cursor.execute(query)
                row = cursor.fetchall()
                server.sendall(bytes('00010dbget'+str(row[0][0]),'utf-8'))
            except:
                server.sendall(bytes('00010dbgetfallo_tipo','utf-8'))

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

        if tipoTransaccion == "registrart":
            try:
                cursor.execute(query)
                db.commit()
                server.sendall(bytes('00010dbgettrabajador_registrado','utf-8'))
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

        if tipoTransaccion == "leeruser":
            try:
                query = data[1]
                query = query.replace("-", " ")
                cursor.execute(query)
                rows = cursor.fetchall()
                if row is None:
                    print("No posee trabajadores")
                    server.sendall(bytes('00010dbgetfallo_leeruser','utf-8'))
                else:
                    users = []
                    for row in rows:
                        user = row[0] + "-" + row[1] + "-" + str(row[2])
                        users.append(user)

                    msg = "leeruser " + "/".join(users)
                    #print(msg)
                    server.sendall(bytes('00010dbget'+msg,'utf-8'))
            except:
                print("Error al leer usuarios")
                server.sendall(bytes('00010dbgetfallo_leeruser','utf-8'))

        if tipoTransaccion == "eliminaruser":
            try:
                cursor.execute(query)
                db.commit()
                server.sendall(bytes('00010dbgetusuario_eliminado','utf-8'))
            except:
                db.rollback()
                server.sendall(bytes('00010dbgetfallo_eliminaruser','utf-8'))

        if tipoTransaccion == "actualizaruser":
            try:
                query_list = data[1]
                query_list = query_list.split("/")
                for query in query_list:
                    query = query.replace("-", " ")
                    cursor.execute(query)
                db.commit()
                server.sendall(bytes('00010dbgetusuario_actualizado','utf-8'))
            except:
                db.rollback()
                server.sendall(bytes('00010dbgetfallo_actualizaruser','utf-8'))

        if tipoTransaccion == "leerprod":
            try:
                query = data[1]
                query = query.replace("-", " ")
                #print(query) #LA QUERY ES CORRECTA, VERIFICADA CON PSQL
                cursor.execute(query)
                rows = cursor.fetchall()
                #print(rows) #CORRECTO
                if row is None:
                    print("No hay productos")
                    server.sendall(bytes('00010dbgetfallo_leerprod','utf-8'))
                else:
                    prods = []
                    for row in rows:
                        prod = str(row[0]) + "-" + row[1] + "-" + str(row[2]) + "-" + row[3] + "-" + str(row[4])
                        prods.append(prod)

                    msg = "leerprod " + "/".join(prods)
                    print(msg)
                    server.sendall(bytes('00010dbget'+msg,'utf-8'))
            except:
                print("Error al leer productos") 
                server.sendall(bytes('00010dbgetfallo_leerprod','utf-8'))

        if tipoTransaccion == "actualizarprod":
            try:
                query_list = data[1]
                query_list = query_list.split("/")
                for query in query_list:
                    query = query.replace("-", " ")
                    cursor.execute(query)
                db.commit()
                server.sendall(bytes('00010dbgetproducto_actualizado','utf-8'))
            except:
                db.rollback()
                server.sendall(bytes('00010dbgetproducto_no_actualizado','utf-8'))

        if tipoTransaccion == "eliminarprod":
            try:
                query = data[1]
                query = query.replace("-", " ")
                cursor.execute(query)
                db.commit()
                server.sendall(bytes('00010dbgetproducto_eliminado','utf-8'))
            except:
                db.rollback()
                server.sendall(bytes('00010dbgetproducto_no_eliminado','utf-8'))

        if tipoTransaccion == "agregardespacho":
            try:
                session_mail = data[1]
                query = data[2]
                query = query.replace("-", " ")
                cursor.execute(query)
                db.commit()
                server.sendall(bytes('00010dbgetdespacho_agregado','utf-8'))
            except:
                db.rollback()
                server.sendall(bytes('00010dbgetdespacho_no_agregado','utf-8'))

        if tipoTransaccion == "leerdespacho":
            try:
                query = data[1]
                query = query.replace("-", " ")
                cursor.execute(query)
                rows = cursor.fetchall()
                if rows is None:
                    server.sendall(bytes('00010dbgetfallo_leerdespacho','utf-8'))
                else:
                    despachos = []
                    for row in rows:
                        despacho = str(row[0]) + "-" + str(row[1]) + "-" + str(row[2]).replace(" ","|") + "-" + str(row[3]).replace(" ","|") + "-" + str(row[4]) + "-" + str(row[5]) + "-" + str(row[6]) + "-" + str(row[7])
                        despachos.append(despacho+"/")

                    msg = "leerdespacho " + "".join(despachos)
                    print(msg)
                    print("Despachos leidos")
                    server.sendall(bytes('00010dbget'+msg,'utf-8'))
            except:
                print("Error al leer despachos")
                server.sendall(bytes('00010dbgetfallo_leerdespacho','utf-8'))

        if tipoTransaccion == "eliminardespacho":
            try:
                query = data[1]
                query = query.replace("-", " ")
                cursor.execute(query)
                db.commit()
                server.sendall(bytes('00010dbgetdespacho_eliminado','utf-8'))
            except:
                db.rollback()
                server.sendall(bytes('00010dbgetdespacho_no_eliminado','utf-8'))

        if tipoTransaccion == "actualizardespacho":
            try:
                query_list = data[1]
                query_list = query_list.split("/")
                for query in query_list:
                    query = query.replace("-", " ")
                    cursor.execute(query)
                db.commit()
                server.sendall(bytes('00010dbgetdespacho_actualizado','utf-8'))
            except:
                db.rollback()
                server.sendall(bytes('00010dbgetdespacho_no_actualizado','utf-8'))

        if tipoTransaccion == "alertastock":
            try:
                session_mail = data[1]
                query = data[2]
                query = query.replace("-", " ")
                cursor.execute(query)
                rows = cursor.fetchall()
                if rows is None:
                    server.sendall(bytes('00010dbgetfallo_alerta','utf-8'))
                else:
                    if session_mail not in alertasActivas:
                        alertasActivas.append(session_mail)
                        #threading.Thread(target=alertaStock, args=(session_mail, rows)).start()
                    else:
                        server.sendall(bytes('00010dbgetalerta_activa','utf-8'))
                    numProds = len(rows)
                    prods = []
                    for row in rows:
                        prod = row[0] + "-" + row[1] + "-" + row[2]
                        prods.append(prod)
                    msg = "alertastock " + str(numProds) + " " + " ".join(prods)
                    print(msg)
                    server.sendall(bytes('00010dbget'+msg,'utf-8'))
            except:
                server.sendall(bytes('00010dbgetfallo_alerta','utf-8'))



