# Validación y pruebas

## Metodología
Dataset Iris de scikit-learn. División estratificada 80/20, `random_state=42`, RandomForestClassifier con 100 árboles. Métricas generadas en `docs/metricas.json`. Las pruebas de API usan FastAPI TestClient, sin servidor de red.

## Casos automatizados
- GET `/`: página HTML disponible.
- GET `/api/health`: modelo cargado.
- POST `/api/predict`: muestra válida de setosa y probabilidades normalizadas.
- Campos faltantes: HTTP 422.
- Medidas negativas: HTTP 422.
- Valores superiores a 20 cm: HTTP 422.
- Tipo de dato inválido: HTTP 422.
- Límite inferior 0: HTTP 200 (válido por esquema, aunque puede carecer de sentido botánico).
- OpenAPI: endpoint documentado.

## Evidencias y alcance
Consultar `docs/evidencias/resultado_pytest.txt` y `docs/evidencias/resultado_entrenamiento.txt` para resultados efectivamente ejecutados. **No se ejecutó Docker ni Cloud Run en el entorno de preparación cuando Docker no está instalado**. Se proporcionan instrucciones reproducibles, pero la construcción de imagen, ejecución local real en Docker y despliegue remoto quedan pendientes de verificar en un equipo con esas herramientas.

## Pruebas manuales pendientes
1. Ejecutar `docker build -t iris-ml:1.0 .` y guardar salida.
2. Ejecutar `docker run --rm -p 8080:8080 iris-ml:1.0`.
3. Verificar `curl` de salud y predicción, y navegador.
4. Verificar comportamiento ante reinicio del contenedor.
5. Desplegar en Cloud Run y registrar URL, estado y logs.

## Conclusiones
El modelo se entrena reproduciblemente y la API tiene pruebas automatizadas. El contenedor y el despliegue requieren validación en infraestructura Docker/Cloud Run antes de afirmar que el proyecto cumple completamente el criterio de ejecución en esos entornos. Las entradas se limitan a [0,20] cm para prevenir valores manifiestamente fuera de rango; esta validación no implica que toda medida aceptada sea botánicamente plausible.
