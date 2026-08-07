# Snowflake decisions for the Informatica PySpark migration

## Recovered legacy behavior

- Physical lookup order is semantically observable. `Use Last Value` and `Use Any Value` are not allowed to depend on Snowflake table storage order.
- Empty fields read by the local Spark CSV path represent SQL `NULL`, and leading spaces are data for the Informatica trim semantics.
- The workflow remains the same transformation code in local and Snowflake modes; Snowflake-specific behavior is isolated to IO and loading.

## `__ROW_ORD` materialization

**Requirement.** Informatica lookup behavior can depend on the physical source row order. Spark and Snowflake do not promise that a table scan returns insertion order.

**Choice.** The loader writes a real `__ROW_ORD` column containing the zero-based physical CSV row index. `SnowflakeIO.read_source` carries it through as `LongType`, rejects any NULL row order, and rejects a row-order count that differs from the source row count. Local reads attach the corresponding ordering column after reading the single CSV file. Baseline target tables deliberately omit `__ROW_ORD`, because it is internal source ordering metadata and would make raw target `MINUS` structurally incomparable.

**Rejected.** Depending on Snowflake physical insertion order, micro-partition order, or an implicit connector ordering would make `Use Last Value` nondeterministic and could silently produce the wrong result.

## Identifier casing

**Requirement.** Existing Snowflake objects use native uppercase, unquoted identifiers, while mapping code expects the declared mixed-case Informatica names.

**Choice.** Reads project uppercase Snowflake columns back to declared Spark names. Writes uppercase target columns and use uppercase unquoted table names.

**Rejected.** Quoted mixed-case identifiers would preserve spelling but create a second naming convention, require quoting in every downstream query, and diverge from existing Snowflake objects.

## Spark-to-Snowflake types

The target registry uses actual mapping output names, order, and Spark data types rather than XML Oracle declarations. The DDL mapping is:

| Spark type | Snowflake type |
|---|---|
| `LongType` | `NUMBER(38,0)` |
| `IntegerType` | `NUMBER(38,0)` |
| `DoubleType` | `FLOAT` |
| `StringType` | `VARCHAR` |
| `DateType` | `DATE` |
| `TimestampType` | `TIMESTAMP_NTZ` |

The deliberate exception to XML-driven typing is decimal amounts: `demo_target6.TX_AMT` and `demo_target5.BAL_AMT` remain floating-point because the mapping outputs decimal values. Using XML’s `number(p,s)` / scale-zero domain would truncate those values. The same registry drives migrated and baseline DDL, which makes warehouse-side comparison structurally fair but means a shared registry error is not detected by that comparison alone.

## Timezone

**Choice.** The connector receives `sfTimezone=UTC`, and the Spark session is UTC. Timestamps are written as `TIMESTAMP_NTZ` under this discipline.

**Why.** A timezone conversion that shifts a business timestamp while preserving a superficially valid value would be a silent parity lie. The run uses the fixed business date `2024-01-31`; no mapping reads the wall clock.

## CSV NULL and whitespace fidelity

The loader uses pandas with empty-field NA handling and `skipinitialspace=False`. Empty CSV fields become SQL `NULL`; values such as `demo_source4.CRDT_LN = '  8000'` retain their leading spaces. The captured evidence checks both behaviors and the duplicate lookup order.

## Explicit DDL and append writes

**Choice.** The loader and Snowflake writer use `CREATE OR REPLACE TABLE` with explicit columns from the registry. The Spark connector writes with `append` after DDL creation.

**Rejected.** Connector type inference with `overwrite` could replace the deliberate DDL with inferred types or connector-specific nullability/precision. Explicit DDL makes migrated and baseline table structures inspectable and stable.

## Snowflake JDBC version deviation

The brief specified `snowflake-jdbc-3.24.2.jar`. Running the Spark connector with that jar failed with this actual error:

```text
java.lang.NoClassDefFoundError:
net/snowflake/client/internal/jdbc/SnowflakeLoggedFeatureNotSupportedException
```

The 3.24.2 jar contained `net/snowflake/client/jdbc/SnowflakeLoggedFeatureNotSupportedException`, while the Spark connector expected the `internal.jdbc` class. The Spark connector POM declares JDBC `4.0.2`; the committed default in `session.py` therefore uses `/home/ubuntu/spark-jars/snowflake-jdbc-4.0.2.jar`, downloaded from Maven Central (`net.snowflake:snowflake-jdbc:4.0.2`). The requested 3.24.2 jar remains present for the reconnaissance requirement. `INFORMATICA_SPARK_JARS` overrides the committed default when a caller supplies a compatible jar set.

## What could still be wrong

- The warehouse proof compares two tables built from one registry and one seed dataset; it cannot detect errors shared by both.
- The source ordering assertion verifies the loader’s own row-order materialization. An independent byte-level CSV comparison would be stronger.
- The Snowflake `ABORT()` failure path was not exercised. The successful run verified all seven target instances only.
- The dataset is too small to establish scale, partitioning, or spill behavior.
