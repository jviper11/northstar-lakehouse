# Bronze Layer

The Bronze layer contains raw source data ingested into Databricks with minimal transformation.

## Current ingestion

`ingest_shipments.py` reads the synthetic `shipments.csv` file from the Git-linked repository and writes it to the Delta table:

`bronze.shipments`

## Added metadata

The Bronze ingestion adds these columns for traceability:

- `source_file` — source file path
- `ingested_at` — timestamp when the data was loaded
- `batch_id` — identifies the ingestion batch

## Design

The Bronze layer is intended to preserve the source data as closely as possible.

Business rules, deduplication, data-quality corrections, and dimensional transformations will be handled in later layers.

## Current source

`data-generator/output/shipments.csv`

## Validation

The first load contains 500 shipment records.

The Bronze table was validated with SQL queries to confirm:
- row count
- source file metadata
- ingestion timestamp
- batch ID