# Credit Registration Tool

Este proyecto es una aplicación web desarrollada con Flask, SQLite, HTML, JavaScript y Chart.js para el registro y visualización de créditos otorgados.

## Requisitos

Asegúrate de tener instalado lo siguiente en tu sistema:
- Python 3.8+
- pip
- Flask y dependencias necesarias

## Ejecución del Servidor

1. **Ejecutar la aplicación:**
   ```sh
   python app.py
   ```

2. **Acceder a la aplicación:**
   Abre tu navegador y ve a:
   ```
   http://127.0.0.1:3030/
   ```

## API Endpoints

- `GET /api/creditlist` - Obtiene la lista de créditos registrados.
- `POST /api/addcredit` - Agrega un nuevo crédito.
- `PUT /api/editcredit/<id>` - Edita un crédito existente.
- `DELETE /api/deletecredit/<id>` - Elimina un crédito por ID.

## Características

- Registro, edición y eliminación de créditos.
- Visualización de datos en tablas.
- Gráficos estadísticos con Chart.js:
  - Cantidad de créditos otorgados.
  - Distribución de montos por cliente o rangos de montos.

## Tecnologías Utilizadas

- **Backend:** Flask, SQLite
- **Frontend:** HTML, CSS, JavaScript, Chart.js


