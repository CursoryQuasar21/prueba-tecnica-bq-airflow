# prueba-tecnica-bq-airflow

Proyecto de Data Engineering desarrollado con Python 3.12 para extraer datos desde una API REST publica, cargarlos en BigQuery, transformarlos mediante SQL idempotente y orquestar patrones basicos con Airflow.

## Arquitectura

```text
JSONPlaceholder comments API
        |
        v
Python extraction
        |
        v
BigQuery RAW: prueba-tecnica-496919.SANDBOX_prueba_tecnica.comments_raw
        |
        v
SQL idempotente: sql/transform.sql
        |
        v
BigQuery final: prueba-tecnica-496919.INTEGRATION.integration_prueba_tecnica
        |
        v
Airflow DAG: test
```

## Estructura

```text
dags/
  test.py                         DAG de Airflow de la Parte 3
plugins/
  operators/
    time_diff_operator.py          Operador custom TimeDiffOperator
sql/
  transform.sql                    Transformacion SQL idempotente
src/
  api/
    client.py                      Cliente REST para JSONPlaceholder
  bigquery/
    loader.py                      Capa de carga a BigQuery
  config/
    settings.py                    Configuracion centralizada
  pipelines/
    ingestion_pipeline.py          Orquestacion de extraccion y carga
  utils/
    logger.py                      Logger comun del proyecto
tests/                             Carpeta preparada para tests
credentials/                       Credenciales locales ignoradas por Git
run_api_check.py                   Validacion manual de extraccion API
run_bigquery_load_check.py         Validacion manual de carga RAW
check_bigquery.py                  Validacion temporal de conexion BigQuery
requirements.txt                   Dependencias del proyecto
pyproject.toml                     Configuracion base Python
```

## Tecnologias

- Python 3.12
- `requests`
- Google Cloud BigQuery
- SQL
- Apache Airflow 2.x
- GitHub

## Parte 2: Extraccion y Carga RAW

La fuente usada es `https://jsonplaceholder.typicode.com/comments`. El flujo de validacion local extrae 100 registros, cumpliendo el minimo requerido por la prueba.

La extraccion esta encapsulada en `APIClient`, dentro de `src/api/client.py`. El cliente usa `requests.Session`, valida el estado HTTP con `raise_for_status()` y comprueba que la respuesta sea una lista antes de devolver los registros.

La carga a BigQuery esta encapsulada en `BigQueryLoader`, dentro de `src/bigquery/loader.py`. Esta clase crea la tabla RAW si no existe y carga registros en modo append sobre:

```text
prueba-tecnica-496919.SANDBOX_prueba_tecnica.comments_raw
```

Los registros RAW mantienen los campos originales de la API:

- `postId`
- `id`
- `name`
- `email`
- `body`

Tambien se anaden metadatos tecnicos de ingesta:

- `ingestion_timestamp`
- `ingestion_date`
- `source`

## SQL Idempotente

La transformacion final esta en `sql/transform.sql`.

El SQL usa `CREATE OR REPLACE TABLE` para reconstruir la tabla final en cada ejecucion:

```text
prueba-tecnica-496919.INTEGRATION.integration_prueba_tecnica
```

La capa RAW es append-only, por lo que puede contener duplicados si se ejecuta la ingesta varias veces. Para generar una tabla final reproducible, la transformacion deduplica por `comment_id` y conserva el registro mas reciente usando `ingestion_timestamp DESC`.

La tabla final renombra:

- `id` a `comment_id`
- `postId` a `post_id`

Y mantiene:

- `comment_id`
- `post_id`
- `name`
- `email`
- `body`
- `source`
- `ingestion_timestamp`
- `ingestion_date`

## Parte 3: Airflow

El DAG implementado se encuentra en `dags/test.py` y se llama exactamente `test`.

Caracteristicas principales:

- Schedule diario a las 03:00 UTC: `0 3 * * *`
- `catchup=False`
- Tareas `start` y `end` usando `EmptyOperator as DummyOperator`
- Tareas dinamicas `task_1`, `task_2`, ..., `task_N`
- Las tareas pares dependen de todas las tareas impares
- `start` precede a las tareas impares
- Las tareas pares preceden a `end`
- Incluye la tarea `time_diff` usando `TimeDiffOperator`

El operador custom `TimeDiffOperator`, definido en `plugins/operators/time_diff_operator.py`, recibe `diff_date`, calcula la diferencia contra la fecha actual UTC y registra:

- `diff_date`
- `current_date`
- diferencia en dias
- diferencia total en segundos

### Hook vs Connection

En Airflow, una Connection almacena configuracion y credenciales de sistemas externos. Un Hook es codigo Python que usa esa Connection para exponer una interfaz reutilizable contra el sistema externo. En resumen: la Connection es configuracion; el Hook es logica de integracion.

## Setup Local

Crear y activar un entorno Conda con Python 3.12:

```bash
conda create -n prueba_tecnica python=3.12
conda activate prueba_tecnica
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Configurar autenticacion local de BigQuery mediante Service Account:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="credentials/service-account.json"
```

En Windows PowerShell:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "credentials/service-account.json"
```

El nombre del archivo de credenciales puede variar. Debe estar dentro de `credentials/` y no debe subirse a Git.

## Comandos Utiles

Validar extraccion desde la API:

```bash
python run_api_check.py
```

Validar carga a BigQuery RAW:

```bash
python run_bigquery_load_check.py
```

Ejecutar `sql/transform.sql` en BigQuery para crear o reemplazar la tabla final:

```text
sql/transform.sql
```

Validar sintaxis de los archivos Airflow principales:

```bash
python -m py_compile dags/test.py plugins/operators/time_diff_operator.py
```

## Seguridad

- `credentials/` esta ignorado por Git.
- `*.json` esta ignorado por Git.
- Las credenciales se gestionan mediante `GOOGLE_APPLICATION_CREDENTIALS`.
- El proyecto esta preparado para usar una Service Account de Google Cloud.
- No se incluyen claves, secretos ni rutas locales absolutas en el codigo.

## Decisiones Tecnicas

- RAW es append-only para preservar los eventos originales de ingesta y evitar mutaciones en la capa de aterrizaje.
- La tabla final es idempotente porque se reconstruye con `CREATE OR REPLACE TABLE`.
- La deduplicacion se aplica en SQL, separando claramente ingesta y transformacion.
- La extraccion API y la carga BigQuery estan desacopladas en clases distintas.
- La configuracion del proyecto se centraliza en `src/config/settings.py`.
- La orquestacion del pipeline vive en `src/pipelines/ingestion_pipeline.py`.
- Airflow se mantiene separado de la logica de negocio para facilitar mantenimiento y pruebas.
