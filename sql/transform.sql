-- Build the final integration table from the append-only RAW layer.
--
-- RAW is intentionally append-only because ingestion jobs should preserve the
-- original landing events and avoid mutating source extracts during loading.
-- As a result, repeated API loads can create multiple RAW rows for the same
-- functional comment id.
--
-- This final table is idempotent because it is fully rebuilt with
-- CREATE OR REPLACE TABLE on every execution. Given the same RAW input, the
-- output table is recreated with the same deduplicated result.
--
-- Duplicates are removed by keeping only the most recent RAW record per comment
-- id, ordered by ingestion_timestamp descending.

CREATE OR REPLACE TABLE
  `prueba-tecnica-496919.INTEGRATION.integration_prueba_tecnica`
AS
SELECT
  id AS comment_id,
  postId AS post_id,
  name,
  email,
  body,
  source,
  ingestion_timestamp,
  ingestion_date
FROM
  `prueba-tecnica-496919.SANDBOX_prueba_tecnica.comments_raw`
QUALIFY
  ROW_NUMBER() OVER (
    PARTITION BY id
    ORDER BY ingestion_timestamp DESC
  ) = 1;
