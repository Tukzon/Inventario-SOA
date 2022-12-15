#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import os
import bcrypt
import hashlib
import time
import tabulate
import re

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)

server.sendall(bytes('00005getsv','utf-8'))
recibido=server.recv(4096)
print("SISTEMA DE INVENTARIO")

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux



while True:
    main_menu = False
    session_mail = ''
    userType = -1
    print("""
    ==========INVENTARIO==========
    Seleccione una opción:
        1. Registro
        2. Iniciar sesión
        0. Salir
    ==============================
    """)
    opcion = input("OPCION: ")
    if opcion == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
        ==============================
        Registrando...
        ==============================
        """)
        email = input("Ingrese su correo: ")
        password = input("Ingrese su contraseña: ")
        nombre = input("Ingrese su nombre: ")

        hash_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
        #print(hash_pwd)

        datos = "registrar "+email + " " + hash_pwd + " " + nombre
        aux = fill(len(datos+ 'users'))
        msg = aux + 'users' + datos
        #print("mensaje enviado: "+msg)
        server.sendall(bytes(msg,'utf-8'))
        recibido=server.recv(4096)
        if recibido.decode('utf-8').find('users')!=-1:
            recibido = recibido[12:]
            #print("desde usuario: "+recibido.decode('utf-8'))
            if recibido.decode('utf-8') == '1':
                print("Usuario registrado satisfactoriamente")
                continue
            else:
                print("Error al registrar usuario")
                continue
        
    elif opcion == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
        ==============================
        Iniciando sesión...
        ==============================
        """)
        email = input("Ingrese su correo: ")
        password = input("Ingrese su contraseña: ")

        hash_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()

        datos = email + " " + hash_pwd
        aux = fill(len(datos+ 'login'))
        msg = aux + 'login' + datos
        print("mensaje enviado: "+msg)

        server.sendall(bytes(msg,'utf-8'))
        while True:
            recibido=server.recv(4096)
            if recibido.decode('utf-8').find('login')!=-1:
                print("recibido cliente: "+recibido.decode('utf-8'))
                recibido = recibido[12:].decode()
                if recibido == '1':
                    print("Sesión iniciada correctamente")
                    session_mail = email
                    main_menu = True
                    datos = "tipo "+session_mail
                    aux = fill(len(datos+ 'dbget'))
                    msg = aux + 'dbget' + datos
                    #print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('dbget')!=-1:
                        recibido = recibido[12:].decode()
                        print("desde cliente: "+recibido)
                        if recibido == '0':
                            userType = 0
                            print("Usuario gestor")
                            time.sleep(2)
                            break
                        elif recibido == '2':
                            userType = 2
                            print("Usuario trabajador")
                            time.sleep(2)
                            break
                        elif recibido == '1':
                            userType = 1
                            print("Usuario administrador")
                            time.sleep(2)
                            break
                        else:
                            print("USER-Error")
                            time.sleep(2)
                            continue
                    break
                elif recibido == '0':
                    print("Usuario o contraseña incorrectos")
                    break
                else:
                    print("Error")
                    continue

        while main_menu:
            os.system('cls' if os.name == 'nt' else 'clear')
            if userType == 2:
                print("""
            ==========INVENTARIO==========
            Seleccione una opción:
                1. Inventario
                2. Despachos
                0. Salir
            ==============================
            """)
            else: 
                print("""
                ==========INVENTARIO==========
                Seleccione una opción:
                    1. Inventario
                    2. Despachos
                    3. Usuarios
                    4. Otros
                    0. Salir
                ==============================
                """)
            opcion = input("OPCION: ")
            if opcion == '1':
                os.system('cls' if os.name == 'nt' else 'clear')
                if userType == 2:
                   print("""
                ==========INVENTARIO==========
                Seleccione una opción:
                    2. Modificar producto
                    4. Listar productos
                    0. Regresar
                ==============================
                """)
                else: 
                    print("""
                ==========INVENTARIO==========
                Seleccione una opción:
                    1. Agregar producto
                    2. Modificar producto
                    3. Eliminar producto
                    4. Listar productos
                    0. Regresar
                ==============================
                """)
                opcion = input("OPCION: ")
                if opcion == '1' and userType == 2:
                    print("No tiene permisos para realizar esta acción")
                    time.sleep(2)
                    continue
                if opcion == '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========INVENTARIO==========
                    Agregando producto...
                    ==============================
                    """)
                    idProd = input("Ingrese el id del producto: ")
                    nombre = input("Ingrese el nombre del producto: ")
                    precio = input("Ingrese el precio del producto: ")
                    cantidad = input("Ingrese la cantidad del producto: ")
                    descripcion = input("Ingrese la descripcion del producto: ")
                    datos = "registrar "+session_mail + " " + idProd + " " + nombre + " " + cantidad + " " + precio + " " + descripcion
                    aux = fill(len(datos+ 'prods'))
                    msg = aux + 'prods' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('prods')!=-1:
                        recibido = recibido[12:]
                        #print("desde usuario: "+recibido.decode('utf-8'))
                        if recibido.decode('utf-8') == '1':
                            print("Producto registrado satisfactoriamente")
                            continue
                        else:
                            print("Error al registrar producto")
                    time.sleep(3)
                    continue
                elif opcion == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========INVENTARIO==========
                    Modificando producto...
                    ==============================
                    """)
                    idProd = input("Ingrese el id del producto: ")
                    nombre = input("Ingrese el nombre del producto: (dejar en blanco para no modificar) ")
                    precio = input("Ingrese el precio del producto: (dejar en blanco para no modificar) ")
                    cantidad = input("Ingrese la cantidad del producto: (dejar en blanco para no modificar)")
                    descripcion = input("Ingrese la descripcion del producto: (dejar en blanco para no modificar) ")
                    if nombre == '' and precio == '' and cantidad == '' and descripcion == '':
                        print("No se modificó el producto")
                        continue
                    if nombre == '':
                        nombre = '/'
                    if precio == '':
                        precio = '/'
                    if cantidad == '':
                        cantidad = '/'
                    if descripcion == '':
                        descripcion = '/'
                    datos = "actualizar "+session_mail+ " "+ str(idProd) + " " + str(nombre) + " " + str(precio) + " " + str(cantidad) + " " + descripcion + " " + str(userType)
                    aux = fill(len(datos+ 'prods'))
                    msg = aux + 'prods' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('prods')!=-1:
                        recibido = recibido[12:]
                        if recibido.decode('utf-8') == '1':
                            print("Producto modificado satisfactoriamente")
                            time.sleep(3)
                            continue
                        else:
                            print("Error al modificar producto")
                            time.sleep(3)
                    continue
                elif opcion == '3' and userType == 2:
                    print("No tiene permisos para realizar esta acción")
                    time.sleep(2)
                    continue
                elif opcion == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========INVENTARIO==========
                    Eliminando producto...
                    ==============================
                    """)
                    idProd = input("Ingrese el id del producto: ")
                    permanente = input("¿Desea eliminar el producto permanentemente? (s/n): ")
                    datos = "eliminar "+session_mail+ " "+permanente+ " "+ idProd
                    aux = fill(len(datos+ 'prods'))
                    msg = aux + 'prods' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('prods')!=-1:
                        recibido = recibido[12:]
                        if recibido.decode('utf-8') == '1':
                            print("Operación efectuada satisfactoriamente")
                            time.sleep(3)
                            continue
                        else:
                            print("Error al eliminar producto")
                            time.sleep(3)
                    continue
                elif opcion == '4':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========INVENTARIO==========
                    Listando productos...
                    ==============================
                    """)
                    prodID = input("Ingrese el id del producto (presione enter para mostrar todos): ")
                    if prodID == '':
                        datos = "leer "+session_mail + " " + str(userType)
                        aux = fill(len(datos+ 'prods'))
                        msg = aux + 'prods' + datos
                    else:
                        datos = "leer "+session_mail + " " + str(prodID) + " " + str(userType)
                        aux = fill(len(datos+ 'prods'))
                        msg = aux + 'prods' + datos

                    #print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('leerprod')!=-1:
                        try:
                            recibido = recibido[12:]
                            recibido = recibido.decode('utf-8').split(' ')
                            productos = recibido[1]
                            productos = productos.replace('/', ' ')
                            productos = productos.split(' ')
                            data = []
                            column_alignments = ["right", "left", "right", "left", "center", "center", "center", "right"]
                            for i in range(len(productos)):
                                productos[i] = productos[i].split('-')
                                data.append(productos[i])

                            print(tabulate.tabulate(data, headers=['ID', 'Nombre', 'Precio', 'Desc.', 'Cantidad'], tablefmt='orgtbl', stralign=column_alignments))
                            input("\nPresione enter para continuar...")
                            continue
                        except:
                            print("Error al listar productos")
                            time.sleep(3)
                            continue
                elif opcion == '0':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========INVENTARIO==========
                    Regresando...
                    ==============================
                    """)
                    continue

            elif opcion == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("""
                ==========DESPACHOS==========
                Seleccione una opción:
                    1. Agregar despacho
                    2. Modificar despacho
                    3. Eliminar despacho
                    4. Listar despachos
                    0. Regresar
                ==============================
                """)
                opcion = input("OPCION: ")
                if opcion == '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========DESPACHOS==========
                    Agregando despacho...
                    ==============================
                    """)
                    mail = input("Ingrese el mail de responsable de despacho: ")
                    direccion = input("Ingrese la direccion de despacho: ")
                    comprador = input("Ingrese el nombre de persona que recibirá: ")
                    totalProd = input("Ingrese el total de productos diferentes: ")
                    prods = []
                    qtt = []
                    for i in range(int(totalProd)):
                        print("====================================")
                        idProd = input("Ingrese el id del producto: ")
                        prods.append(idProd)
                        cantidad = input("Ingrese la cantidad del producto: ")
                        qtt.append(cantidad)
                    prods = '-'.join(prods)
                    qtt = '-'.join(qtt)
                    datos = "registrar "+ session_mail+ " " +mail + " " +direccion+ " "+comprador + " " +str(prods)+ " " +str(qtt)
                    aux = fill(len(datos+ 'despa'))
                    msg = aux + 'despa' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('despa')!=-1:
                        recibido = recibido[12:]
                        if recibido.decode('utf-8') == '1':
                            print("Despacho generado satisfactoriamente")
                            time.sleep(3)
                            continue
                        else:
                            print("Error al agregar despacho")
                            time.sleep(3)
                            continue
                    continue
                elif opcion == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========DESPACHOS==========
                    Modificando despacho...
                    ==============================
                    """)
                    idDesp = input("Ingrese el id del despacho: ")
                    direccion = input("Ingrese la direccion de despacho: (presione enter para no modificar) ")
                    comprador = input("Ingrese el nombre de persona que recibirá: (presione enter para no modificar) ")
                    responsable = input("Ingrese el mail de responsable de despacho: (presione enter para no modificar) ")
                    totalProd = input("Ingrese el total de productos diferentes: (presione enter para no modificar) ")

                    if totalProd == '' and direccion == '' and comprador == '' and responsable == '':
                        print("No se modificó nada")
                        time.sleep(3)
                        continue

                    prods = '/'
                    qtt = '/'
                    if totalProd != '':
                        prods = []
                        qtt = []
                        for i in range(int(totalProd)):
                            idProd = input("Ingrese el id del producto: ")
                            cantidad = input("Ingrese la cantidad del producto: ")
                            prods.append(idProd)
                            qtt.append(cantidad)
                        prods = '-'.join(prods)
                        qtt = '-'.join(qtt)
                    
                    if direccion == '':
                        direccion = '/'
                    if comprador == '':
                        comprador = '/'
                    if responsable == '':
                        responsable = '/'

                    
                    datos ="actualizar" + " " + session_mail + " " + idDesp + " " + direccion + " " + comprador + " " + responsable + " " + str(prods) + " " + str(qtt)
                    aux = fill(len(datos+ 'despa'))
                    msg = aux + 'despa' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('despa')!=-1:
                        recibido = recibido[12:]
                        if recibido.decode('utf-8') == '1':
                            print("Despacho modificado satisfactoriamente")
                            time.sleep(3)
                            continue
                        else:
                            print("Error al modificar despacho")
                            time.sleep(3)
                            continue
                    continue
                elif opcion == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========DESPACHOS==========
                    Eliminando despacho...
                    ==============================
                    """)
                    idDesp = input("Ingrese el id del despacho: ")
                    permanente = input("¿Desea eliminar permanentemente el despacho? (s/n): ")
                    datos = "eliminar "+ session_mail + " " + permanente +" "+idDesp
                    aux = fill(len(datos+ 'despa'))
                    msg = aux + 'despa' + datos
                    #print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('despa')!=-1:
                        recibido = recibido[12:]
                        if recibido.decode('utf-8') == '1':
                            print("Despacho eliminado satisfactoriamente")
                            time.sleep(3)
                            continue
                        else:
                            print("Error al eliminar despacho")
                            time.sleep(3)
                            continue
                    continue
                elif opcion == '4':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========DESPACHOS==========
                    Listando despachos...
                    ==============================
                    """)
                    despID = input("Ingrese el id del despacho: (enter para mostrar todos) ")
                    if despID == '':
                        despID = '0'
                    datos = "leer "+session_mail + " " + despID
                    aux = fill(len(datos+ 'despa'))
                    msg = aux + 'despa' + datos
                    #print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('despa')!=-1:
                        recibido = recibido[12:]
                        if recibido.decode('utf-8') == '0':
                            print("No hay deespachos registrados")
                            time.sleep(3)
                            continue
                        else:
                            recibido = recibido.decode('utf-8').split(' ')
                            data = recibido[1]
                            data = data.replace('|','')
                            data_rows = re.split("/", data)

                            data = []
                            for row in data_rows:
                                data.append(row.split("-"))
                            
                            column_alignments = ["right", "left", "right", "left", "center", "center", "center", "right"]

                            print(tabulate.tabulate(data, headers=['ID','Inventario','Productos','Cantidad','Direccion','Responsable','Comprador','Valido'], tablefmt='orgtbl', stralign=column_alignments))

                            input("\nPresione enter para continuar...")
                            continue
                    continue

                elif opcion == '0':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========DESPACHOS==========
                    Regresando...
                    ==============================
                    """)
                    continue
            elif opcion == '3' and userType == 2:
                print("No tiene permisos para acceder a esta sección")
                time.sleep(3)
                continue
            elif opcion == '3':
                #USUARIOS
                os.system('cls' if os.name == 'nt' else 'clear')
                print("""
                ==========USUARIOS==========
                Seleccione una opción:
                    1. Agregar usuario
                    2. Modificar usuario
                    3. Eliminar usuario
                    4. Listar usuarios
                    0. Regresar
                ==============================
                """)
                opcion = input("OPCION: ")
                if opcion == '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========USUARIOS==========
                    Agregando trabajador...
                    ==============================
                    """)
                    nombre = input("Ingrese el nombre del usuario: ")
                    correo = input("Ingrese el correo del usuario: ")
                    contra = input("Ingrese la contraseña del usuario: ")

                    hash_pwd = hashlib.sha256(contra.encode('utf-8')).hexdigest()

                    datos = "registrartrabajador "+session_mail+" "+nombre + " " + correo + " " + hash_pwd
                    aux = fill(len(datos+ 'users'))
                    msg = aux + 'users' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('users')!=-1:
                        recibido = recibido[12:]
                        if recibido.decode('utf-8') == '1':
                            print("Trabajador agregado satisfactoriamente")
                            time.sleep(3)
                            continue
                        else:
                            print("Error al agregar trabajador")
                            time.sleep(3)
                            continue
                    continue
                elif opcion == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========USUARIOS==========
                    Modificando usuario...
                    ==============================
                    """)
                    correo = input("Ingrese el correo del usuario a modificar: ")
                    nombre = input("Ingrese el nuevo nombre del usuario: ")
                    contra = input("Ingrese la nueva contraseña del usuario: ")
                    datos = correo + " " + nombre + " " + contra
                    aux = fill(len(datos+ 'modi2'))
                    msg = aux + 'modi2' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
                    continue
                elif opcion == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========USUARIOS==========
                    Eliminando usuario...
                    ==============================
                    """)
                    correo = input("Ingrese el correo del usuario a eliminar: ")
                    aux = fill(len(correo+ 'elim2'))
                    msg = aux + 'elim2' + correo
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
                    continue
                elif opcion == '4':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========USUARIOS==========
                    Listando usuarios...
                    ==============================
                    """)
                    aux = fill(len('lsus'))
                    msg = aux + 'lsusr'
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
                    continue
                elif opcion == '0':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========USUARIOS==========
                    Regresando...
                    ==============================
                    """)
                    continue
            elif opcion == '4' and userType == 2:
                print("No tiene permisos para acceder a esta sección")
                time.sleep(3)
                continue
            elif opcion == '4':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("""
                ===========OTROS===========
                Seleccione una opción:
                    1. Configurar alertas
                    2. Confirmar Despacho
                    3. Modo monitor stock
                    0. Regresar
                """)
                opcion = input("OPCION: ")
                if opcion == '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ===========OTROS===========
                    Configurando alertas...
                    ==============================
                    """)
                    idProd = input("Ingrese el id del producto: ")
                    stockMin = input("Ingrese el stock minimo: ")
                    datos = session_mail+" "+idProd + " " + stockMin
                    aux = fill(len(datos+ 'alert'))
                    msg = aux + 'alert' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('alert')!=-1:
                        recibido=recibido[10:].decode('utf-8')
                        if recibido == '1':
                            print("Alerta configurada correctamente")
                        else:
                            print("Error al configurar alerta")
                        time.sleep(3)
                    continue
                elif opcion == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ===========OTROS===========
                    Confirmar Despacho...
                    ==============================
                    """)
                    idDesp = input("Ingrese el id del despacho: ")
                    datos = session_mail+" "+idDesp
                    aux = fill(len(datos+ 'conde'))
                    msg = aux + 'conde' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('conde')!=-1:
                        recibido=recibido[10:].decode('utf-8')
                        if recibido == '1':
                            print("Despacho confirmado correctamente")
                        else:
                            print("Error al confirmar despacho")
                        time.sleep(3)
                    continue
                elif opcion == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ===========OTROS===========
                    Modo monitor stock...
                    ==============================
                    """)
                    continue
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ===========OTROS===========
                    Regresando...
                    ==============================
                    """)
                    continue
            
            elif opcion == '0':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("""
                ==========SALIENDO==========
                """)
                main_menu = False
                break
        
    else:
        print("Cerrando cliente...")
        break


