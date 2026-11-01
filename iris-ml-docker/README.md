# Clasificador Iris - API + Frontend + Docker

Proyecto académico de clasificación de especies Iris con Random Forest entrenado con `sklearn.datasets.load_iris` (150 observaciones, 4 atributos, 3 clases). No requiere claves externas.

## Requisitos
Python 3.11, Docker Engine con Compose, Git. Para nube: cuenta Google Cloud, gcloud CLI, proyecto con facturación y permisos.

## Ejecución sin Docker
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/train_model.py  # opcional: regenerar artefacto y métricas
uvicorn backend.main:app --host 127.0.0.1 --port 8080
```
Visita http://localhost:8080 y documentación interactiva en http://localhost:8080/docs.

## Docker
```bash
docker build -t iris-ml:1.0 .
docker run --rm -p 8080:8080 iris-ml:1.0
# Alternativa: docker compose up --build
```
Prueba API:
```bash
curl http://localhost:8080/api/health
curl -X POST http://localhost:8080/api/predict -H 'Content-Type: application/json' -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

## Pruebas
```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

## Organización
- `backend/main.py`: API y carga del modelo.
- `backend/modelo.joblib`: modelo entrenado (solo cargar artefactos confiables).
- `frontend/`: interfaz integrada mediante `fetch`.
- `scripts/train_model.py`: entrenamiento reproducible.
- `tests/`: pruebas de API y casos límite.
- `docs/`: manual de nube, validación y métricas.
- `.github/workflows/tests.yml`: integración continua.

## GitHub
```bash
git init
git add .
git commit -m 'Proyecto Iris Docker y FastAPI'
git branch -M main
git remote add origin https://github.com/TU_USUARIO/iris-ml-docker.git
git push -u origin main
```
Crea antes un repositorio vacío con ese nombre y reemplaza `TU_USUARIO`. No incluyas credenciales. Consulta `docs/manual_despliegue.md`.

## Alcance
Predicciones educativas, no identificación botánica profesional. El modelo se entrenó en un conjunto pequeño y no garantiza generalización a medidas fuera de distribución.
