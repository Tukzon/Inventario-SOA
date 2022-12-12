#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import os
import bcrypt
import hashlib

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
                    main_menu = True
                    break
                elif recibido == '0':
                    print("Usuario o contraseña incorrectos")
                    break
                else:
                    print("Error")
                    continue

        while main_menu:
            os.system('cls' if os.name == 'nt' else 'clear')
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
                    datos = idProd + " " + nombre + " " + precio + " " + cantidad + " " + descripcion
                    aux = fill(len(datos+ 'addpr'))
                    msg = aux + 'addpr' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
                    continue
                elif opcion == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========INVENTARIO==========
                    Modificando producto...
                    ==============================
                    """)
                    idProd = input("Ingrese el id del producto: ")
                    nombre = input("Ingrese el nombre del producto: ")
                    precio = input("Ingrese el precio del producto: ")
                    cantidad = input("Ingrese la cantidad del producto: ")
                    descripcion = input("Ingrese la descripcion del producto: ")
                    datos = idProd + " " + nombre + " " + precio + " " + cantidad + " " + descripcion
                    aux = fill(len(datos+ 'modpr'))
                    msg = aux + 'modpr' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
                    continue
                elif opcion == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========INVENTARIO==========
                    Eliminando producto...
                    ==============================
                    """)
                    idProd = input("Ingrese el id del producto: ")
                    aux = fill(len(nombre+ 'delpr'))
                    msg = aux + 'delpr' + idProd
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
                    continue
                elif opcion == '4':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========INVENTARIO==========
                    Listando productos...
                    ==============================
                    """)
                    aux = fill(len('listpr'))
                    msg = aux + 'lsprd'
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
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
                    totalProd = input("Ingrese el total de productos: ")
                    prods = []
                    for i in range(int(totalProd)):
                        idProd = input("Ingrese el id del producto: ")
                        cantidad = input("Ingrese la cantidad del producto: ")
                        prods.append(idProd + " " + cantidad)
                    datos = totalProd + " " + str(prods)
                    aux = fill(len(datos+ 'addes'))
                    msg = aux + 'addes' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
                    continue
                elif opcion == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========DESPACHOS==========
                    Modificando despacho...
                    ==============================
                    """)
                    idDesp = input("Ingrese el id del despacho: ")
                    totalProd = input("Ingrese el total de productos: ")
                    prods = []
                    for i in range(int(totalProd)):
                        idProd = input("Ingrese el id del producto: ")
                        cantidad = input("Ingrese la cantidad del producto: ")
                        prods.append(idProd + " " + cantidad)
                    datos = idDesp + " " + totalProd + " " + str(prods)
                    aux = fill(len(datos+ 'modes'))
                    msg = aux + 'modes' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
                    continue
                elif opcion == '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========DESPACHOS==========
                    Eliminando despacho...
                    ==============================
                    """)
                    idDesp = input("Ingrese el id del despacho: ")
                    aux = fill(len(idDesp+ 'dedes'))
                    msg = aux + 'dedes' + idDesp
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
                    continue
                elif opcion == '4':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========DESPACHOS==========
                    Listando despachos...
                    ==============================
                    """)
                    aux = fill(len('lsdes'))
                    msg = aux + 'lsdes'
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
                    continue
                elif opcion == '0':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ==========DESPACHOS==========
                    Regresando...
                    ==============================
                    """)
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
                    Agregando usuario...
                    ==============================
                    """)
                    nombre = input("Ingrese el nombre del usuario: ")
                    correo = input("Ingrese el correo del usuario: ")
                    contra = input("Ingrese la contraseña del usuario: ")
                    datos = nombre + " " + correo + " " + contra
                    aux = fill(len(datos+ 'regi2'))
                    msg = aux + 'regi2' + datos
                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    print(recibido[10:].decode('utf-8'))
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
                    continue
                elif opcion == '2':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("""
                    ===========OTROS===========
                    Confirmar Despacho...
                    ==============================
                    """)
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


