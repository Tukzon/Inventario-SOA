# Sistema de inventario

Este código es un programa en Python que implementa un sistema de inventario. El programa se conecta a un servidor mediante un socket, y envía y recibe mensajes para realizar diferentes operaciones relacionadas con el inventario, como registrar usuarios, iniciar sesión, agregar productos, consultar existencias, etc.

## Dependencias

El programa utiliza las siguientes librerías de Python:

    - socket: para establecer la conexión con el servidor.
    - threading: para ejecutar ciertas operaciones en paralelo.
    - bcrypt: para encriptar las contraseñas de los usuarios.
    - hashlib: para generar hashes de las contraseñas y verificar si coinciden con los hashes almacenados en la base de datos.

## Funcionamiento

El programa comienza con un menú principal que permite al usuario registrarse o iniciar sesión. Si el usuario elige registrarse, se le piden su correo, contraseña y nombre, y se envía un mensaje al servidor para que registre al usuario en la base de datos. Si el usuario elige iniciar sesión, se le piden su correo y contraseña, y se envía un mensaje al servidor para que verifique si el usuario existe y si la contraseña es correcta.

Si la sesión se inicia correctamente, el programa entra en un menú principal que permite al usuario realizar diferentes operaciones con el inventario, dependiendo de su tipo de usuario. Si el usuario es un administrador, puede agregar, modificar o eliminar productos, consultar el inventario completo, consultar las existencias de un producto específico, y agregar un nuevo usuario como administrador. Si el usuario es un vendedor, puede consultar el inventario completo y consultar las existencias de un producto específico.

Para realizar estas operaciones, el programa envía mensajes al servidor con diferentes comandos y parámetros, y recibe respuestas del servidor con la información solicitada o con mensajes de error en caso de que se produzca.
