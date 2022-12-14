#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import os
import bcrypt
import hashlib
import time

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
                    datos = "registrar "+session_mail + " " + idProd + " " + nombre + " " + precio + " " + cantidad + " " + descripcion
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
                    datos = "actualizar "+session_mail+ " "+ idProd + " " + nombre + " " + precio + " " + cantidad + " " + descripcion
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
                        datos = "leer "+session_mail
                        aux = fill(len(datos+ 'prods'))
                        msg = aux + 'prods' + datos
                    else:
                        datos = "leer "+session_mail + " " + prodID
                        aux = fill(len(datos+ 'prods'))
                        msg = aux + 'prods' + datos

                    print("mensaje enviado: "+msg)
                    server.sendall(bytes(msg,'utf-8'))
                    recibido=server.recv(4096)
                    if recibido.decode('utf-8').find('leerprod')!=-1:
                        try:
                            recibido = recibido[12:]
                            recibido = recibido.decode('utf-8').split(' ')
                            productos = recibido[1]
                            productos = productos.replace('/', ' ')
                            productos = productos.split(' ')
                            #transforma los elementos dentro de productos, cambiando los - como elementos de un subarray
                            for i in range(len(productos)):
                                productos[i] = productos[i].split('-')
                            
                            #imprime los productos
                            print("ID\tNombre\tCant.\tDesc.\tPrecio")
                            for i in range(len(productos)):
                                print(productos[i][0]+"\t"+productos[i][1]+"\t"+productos[i][2]+"\t"+productos[i][3]+"\t"+productos[i][4])
                            #press enter to continue
                            input("Presione enter para continuar...")
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
                    totalProd = input("Ingrese el total de productos: ")
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


