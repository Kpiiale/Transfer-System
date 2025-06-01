# Monitor IoT - Azure Service Bus

Este proyecto simula un sistema de monitoreo de incidentes de sensores industriales usando Azure Service Bus.

## Archivos

- `productor.py`: simula sensores IoT que envían alertas a una cola.
- `consumidor.py`: recibe y procesa las alertas.
- `config.example.json`: plantilla de configuración.
- `.gitignore`: evita subir el archivo json original.
- `requirements.txt`: Lista de dependencias

## Configuración del proyecto
Crear y activar un entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Instrucciones

1. Copia `config.example.json` como `config.json` y coloca tu Connection String real.
2. Ejecuta el productor:

```bash
python productor.py
```
3. Ejecuta el consumidor:

```bash
python consumidor.py
```

## Recomendaciones

Si al ejecutar los scripts aparece un error como:

```bash
FileNotFoundError: [Errno 2] No such file or directory
```
Esto indica que el archivo config.json no se encuentra en el directorio actual desde donde estás ejecutando el script.

Para solucionarlo asegúrate de estar ubicado en la carpeta correcta dentro del proyecto. Por ejemplo:

```bash
cd ruta/a/tu/proyecto/productores_consumidores
```

Reemplaza ruta/a/tu/proyecto con la ruta real donde tengas el repositorio clonado.