# Clasificador Iris

Clasificador web de especies Iris con Random Forest entrenado con el dataset de `sklearn.datasets.load_iris`

## Requisitos
Python 3.11, Docker Engine con Compose, Git. 

## Abrir el proyecto en GitHub Codespaces

1. Accede a GitHub y abre el repositorio del proyecto.
2. Selecciona **Code → Codespaces → Create codespace on main**.
3. Espera a que se abra el editor de Visual Studio Code en el navegador.
4. Abre **Terminal → New Terminal**.
5. Verifica que estás en la carpeta que contiene `docker-compose.yml`:

```bash
pwd
ls
```

## Estructura del proyecto

```text
fase-ii/
├── backend/
│   ├── main.py
│   └── modelo.joblib
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── scripts/
│   └── train_model.py
├── tests/
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Construir la imagen Docker

En la terminal de Codespaces ejecutar:

```bash
docker compose build --no-cache
```

El parámetro `--no-cache` evita reutilizar las capas de compilación anteriores. Verifica la imagen creada:

```bash
docker images
```

## Iniciar y verificar el contenedor

```bash
docker compose up -d
docker compose ps
```

El servicio se llama `iris` y la configuración original publica el **puerto 8080 del Codespace hacia el puerto 8080 del contenedor** (`8080:8080`). Comprueba que figure como `Up` o `running`.

Para revisar los registros:

```bash
docker compose logs --tail=100
```

## Abrir la interfaz web

1. En Codespaces abre la pestaña **Ports**.
2. Busca el puerto **8080**; si no aparece, agrégalo desde la pestaña Ports.
3. Selecciona **Open in Browser** en la URL reenviada.
4. Verifica que aparezca el formulario de clasificación Iris.

Para probar una predicción, introduce estos valores:

| Característica | Valor (cm) |
| --- | ---: |
| Longitud del sépalo | 5.1 |
| Ancho del sépalo | 3.5 |
| Longitud del pétalo | 1.4 |
| Ancho del pétalo | 0.2 |

Selecciona el botón de predicción. Para esta entrada se espera la especie **setosa**; verifica la respuesta real del modelo.

## Verificar el API

Desde la terminal del Codespace:

```bash
curl http://localhost:8080/api/health
```

La respuesta esperada incluye:

```json
{"status":"ok","model":"loaded"}
```

Ejemplo de predicción por API:

```bash
curl -X POST http://localhost:8080/api/predict \
  -H 'Content-Type: application/json' \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

La respuesta contiene `species`, `confidence` y `probabilities`. Para consultar Swagger UI, abre la **URL reenviada del puerto 8080** y añade `/docs`.

## Ejecutar pruebas automatizadas

El proyecto incluye pruebas en `tests/`. Para ejecutarlas en el entorno de Codespaces, instala las dependencias de desarrollo en un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

## Organización
- `backend/main.py`: API y carga del modelo.
- `backend/modelo.joblib`: modelo entrenado.
- `frontend/`: interfaz grafica web.
- `scripts/train_model.py`: generador del modelo de clasificación.
- `tests/`: pruebas de API.
- `docs/`:  métricas y evidencias de test.
