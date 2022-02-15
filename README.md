# Challenge-MeLi-2022

Aplicacion desarrollada para el Challenge Tecnico de Mercadolibre 2022.

# Stack tecnologico

* Python 3.x
* MySQL

## Variables de entorno

Para correr esta aplicacion, es necesario crear un archivo de configuracion llamado 'config.ini', con las variables presentes en config.ini.example. Estas variables son necesarias para la creacion de la base de datos y sus tablas, como asi tambien para poder enviar mails con la API de Google.

# Ejecucion del programa

* Primero y principal, se debera tener instalado SQLServer y PIP.
* Descargar los archivos de este repositorio
* Ingresar a la carpeta donde estan guardados los archivos, abrir una terminal ahi dentro e instalar las dependencias necesarias para correr la aplicacion. El comando para esto es **pip install -r requirements.txt**
* Para la ejecucion del programa, en la misma consola correr **python3 main.py**
* Para la ejecucion de los tests, en la misma consola correr **python3 test.py**

# Archivos presentes

## database.py

Contiene el codigo fuente necesario para crear una conexion SQL y crear la base de datos con sus respectivas tablas.
Las tablas generadas son 2:

* **drive**, donde se guardan los siguientes datos: **id, nombre, extension, propietario, visibilidad (publico = 1, privado = 0) , fecha de ultima modificacion** de cada archivo presente en el Drive.

* **logs_drive**, donde se guardan los siguiente datos: **id, nombre, visibilidad** de cada archivo que fue publico alguna vez en el Drive.

## google_api.py

Contiene el codigo fuente necesario para crear una conexion con Google Drive y GMail. Es necesario contar con las credenciales para poder usar la aplicacion (**credentials.json**). Se genera un archivo llamado **token.pickle** luego de la primera ejecucion y autorizacion con google.
Además, se encuentra la lógica que permite listar todos los archivos presentes en el Google Drive; la lógica que permite hacer cambio de permisos y visibilidad de un archivo y la lògica que permite enviar emails.

## main.py

Archivo principal del programa. Se encarga de buscar los archivos en el Drive del usuario, los guarda en la tabla **drive** de la base de datos: si el archivo es público, ademàs se lo guarda en la tabla **logs_drive** para llevar un historico de documentos públicos. Luego, se le cambian los permisos y la visibilidad, y se envia un email al propietario del archivo, avisandole que su archivo fue modificado por razones de seguridad.

# Bibliografía

* https://developers.google.com/gmail/api/quickstart/python
* https://developers.google.com/drive/api/v3/quickstart/python
* https://realpython.com/python-testing/
* https://docs.python.org/3/library/unittest.mock.html
* https://dev.mysql.com/doc/connector-python/en/
* https://developers.google.com/gmail/api/auth/scopes
* https://developers.google.com/drive/api/v3/reference/permissions/delete
* https://www.iperiusbackup.net/es/activar-la-api-de-google-drive-y-obtener-las-credenciales-para-la-copia-de-seguridad/
