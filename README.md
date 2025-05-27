# Transfer System - Sistema de Transferencias Bancarias
---
### Este proyecto es una simulación de un sistema bancario distribuido
Permite crear cuentas de usuario.
- Administra transferencias entre cuentas.
- Usa RabbitMQ para enviar:
  - Confirmaciones personalizadas (Direct)
  - Notificaciones generales (Fanout)
  - Alertas específicas por tipo y banco (Topic)
- Guarda un registro (`log`) de cada mensaje recibido.
- Almacena las transferencias realizadas en un archivo JSON. 
### 

###
Antes de ejecutar el proyecto, asegúrate de tener instalado:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Python 3.9+ (para correr el programa en consola)
###

### Archivo docker-compose.yml
Este archivo levanta un servidor de RabbitMQ local con panel web.

### Para levantar RabbitMQ con Docker

- Abre la terminal de Docker Desktop
- Ubícate en la carpeta del proyecto 
- Ejecuta:
    docker compose up -d
- Esto iniciará RabbitMQ en segundo plano
- URL de acceso: http://localhost:15672
###

### Para ejecutar el programa corre main.py
