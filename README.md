# Proyecto: Consulta de Boletos para Concierto

Este proyecto es una aplicación web sencilla que permite consultar la información de boletos de un concierto benéfico usando un archivo Excel como fuente de datos. La persona usuaria ingresa el número de correlativo y el sistema muestra los detalles del boleto.

## Estructura del Proyecto
- `app.py`: Código principal de la aplicación Flask.
- `templates/index.html`: Interfaz web para la consulta.
- `boletos.xlsx`: Archivo Excel con la información de los boletos.
- `README.md`: Documentación y guía de uso.

## Requisitos
- Python 3.8+
- Flask
- pandas
- openpyxl

## Instalación
1. Instala las dependencias:
   ```powershell
   pip install flask pandas openpyxl
   ```
2. Coloca tu archivo `boletos.xlsx` en la carpeta raíz del proyecto.
3. Ejecuta la aplicación:
   ```powershell
   python app.py
   ```
4. Accede a la interfaz en tu navegador en `http://localhost:5000`

## Personalización
- Puedes modificar el archivo Excel para agregar o cambiar información de los boletos.
- La interfaz web puede personalizarse editando `templates/index.html`.

## Contacto
Para dudas o mejoras, contacta al responsable de logística del concierto.
