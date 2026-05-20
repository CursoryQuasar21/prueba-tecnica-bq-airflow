# prueba-tecnica-data-engineering

Proyecto base de Data Engineering para una prueba tecnica profesional con Python 3.12, Apache Airflow, Google BigQuery, ingesta desde API REST y transformaciones SQL.

## Objetivo

Este repositorio contiene un esqueleto inicial limpio y mantenible. La logica de negocio, la ingesta real, las cargas a BigQuery y las transformaciones SQL se implementaran en fases posteriores.

## Estructura

```text
dags/                 DAGs de Airflow
plugins/operators/    Operadores custom de Airflow
sql/                  Transformaciones SQL para BigQuery
src/api/              Cliente para API REST
src/bigquery/         Componentes de carga a BigQuery
src/config/           Configuracion del proyecto
src/pipelines/        Orquestacion de pipelines
src/utils/            Utilidades compartidas
tests/                Tests automatizados
credentials/          Credenciales locales ignoradas por Git
```

## Configuracion inicial

1. Crear un entorno virtual con Python 3.12.
2. Instalar dependencias desde `requirements.txt`.
3. Copiar `.env.example` a `.env` y completar las variables necesarias.
4. Guardar credenciales locales en `credentials/`. Este directorio esta ignorado por Git.

## Estado

Base inicial del proyecto creada. Pendiente de implementar:

- Cliente de API REST.
- Carga de datos en BigQuery.
- DAGs productivos de Airflow.
- Transformaciones SQL.
- Tests automatizados.
