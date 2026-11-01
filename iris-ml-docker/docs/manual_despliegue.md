# Manual técnico de despliegue

## Arquitectura
Navegador -> frontend estático servido por FastAPI -> POST /api/predict -> Random Forest cargado desde `backend/modelo.joblib` -> JSON -> navegador. Un contenedor expone el puerto 8080.

## Requisitos
- Docker Engine y plugin Compose para ejecución local.
- Python 3.11 para entrenamiento y pruebas.
- Git y cuenta GitHub para publicación.
- Google Cloud CLI, cuenta con proyecto y facturación habilitada, permisos para habilitar APIs, publicar imágenes y desplegar Cloud Run. Puede haber costos.

## 1. Preparación y ejecución local
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
docker build -t iris-ml:1.0 .
docker run --name iris-local --rm -p 8080:8080 iris-ml:1.0
```
En otra terminal:
```bash
curl -f http://localhost:8080/api/health
curl -X POST http://localhost:8080/api/predict -H 'Content-Type: application/json' -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```
Abrir http://localhost:8080. Para detener: Ctrl+C. Como alternativa `docker compose up --build`.

## 2. Publicación de imagen en Artifact Registry
Reemplaza `MI_PROYECTO` con el ID de tu proyecto y elige una región disponible, aquí `us-central1`.
```bash
gcloud auth login
gcloud config set project MI_PROYECTO
gcloud services enable run.googleapis.com artifactregistry.googleapis.com
gcloud artifacts repositories create iris-images --repository-format=docker --location=us-central1 --description='Imagen Iris'
gcloud auth configure-docker us-central1-docker.pkg.dev
docker build -t us-central1-docker.pkg.dev/MI_PROYECTO/iris-images/iris-ml:1.0 .
docker push us-central1-docker.pkg.dev/MI_PROYECTO/iris-images/iris-ml:1.0
```
Si el repositorio ya existe, omite el comando `create`.

## 3. Despliegue en Cloud Run
```bash
gcloud run deploy iris-ml --image us-central1-docker.pkg.dev/MI_PROYECTO/iris-images/iris-ml:1.0 --region us-central1 --platform managed --port 8080 --memory 512Mi --allow-unauthenticated
```
`--allow-unauthenticated` crea un servicio accesible públicamente; úsalo solo si es lo deseado. Para acceso privado, configura autenticación y permisos de invocación. La consola muestra la URL del servicio. Verifica `URL/api/health`, `URL/docs` y predicciones desde la interfaz.

## 4. Operación y seguridad
- Revisa logs: `gcloud run services logs read iris-ml --region us-central1 --limit 50`.
- Mantén secretos fuera del repositorio; usa Secret Manager cuando corresponda.
- Versiona las imágenes con etiquetas inmutables o digest; evita depender de `latest`.
- Define límites de recursos, control de acceso y presupuesto de facturación.
- Para actualizar: construye, publica una nueva etiqueta y despliega esa imagen.
- Para eliminar y evitar costos: `gcloud run services delete iris-ml --region us-central1`; revisa también imágenes en Artifact Registry.

## 5. Evidencias para entrega
Captura de `docker build`, `docker ps`, GET `/api/health`, POST `/api/predict`, navegador con resultado, ejecución de `pytest`, servicio Cloud Run y URL pública si se despliega. Guarda imágenes en `docs/evidencias/` sin secretos.

## 6. Herramientas de documentación
README y documentos Markdown versionados en Git. GitHub Copilot puede asistir en borradores de comentarios, documentación y casos de prueba, pero cada instrucción y resultado debe revisarse y comprobarse manualmente. Indica en tu entrega si realmente utilizaste Copilot; no atribuyas uso no realizado.

## 7. Portabilidad
Python y bibliotecas fijados en `requirements.txt`, modelo incluido en la imagen, rutas relativas al proyecto, sin dependencia de base de datos externa. El despliegue es compatible con servicios de contenedores que acepten imágenes OCI y un puerto HTTP.
