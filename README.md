# Shipping

Shipping is a synthetic companion to Northwind for investigating request,
routing, receipt, attempt, and event histories. The fixture includes healthy
order `11038` and blocked baseline orders `11045` and `11062`; the latter two
have separately stored future recovery examples, with the `11062` replay still
pending. It is served read-only through OpenVaultDB at
<https://ovdb.demodb.dev/v1/databases/shipping>
(`capabilities.ovdb.deploymentVerified` in `manifest.json`; the endpoint
answered with its schema on 2026-10-22).

The checked-in SQLite file is copied byte-for-byte from the public
`datatug/datatug-demo-project` fixture at revision
`3f8a040fec8f807175138edd30dc3041bd7f55b8`. It is CC0-1.0 licensed and has
SHA-256 `73f0d871607ee5b24de68b5398c25806f556a3126a31e1865fee79b2881977e0`.
The fixture was introduced at revision
`38a51dda39d988f2d2bcf23703bd1a969d49f4a3`; the source bytes are identical at
that revision and the later pinned source revision. The pinned revision's
fixture manifest (`data-source/fixture-manifest.json`) also lists the additive
synthetic carrier-gateway log files published by `demo-db/shipping-logs`; the
database itself does not import logs.
The database is synthetic training data; it does not describe real shipments
or partner calls.

Provider exports, ModelSpec, MeaningGraph, and the OVDB descriptor are generated
from `manifest.json` and `data-source/base.sqlite` by DemoDB's immutable shared
generator. CI downloads the generator from the pinned DemoDB websites revision,
checks its digest, regenerates every artifact, and rejects any uncommitted
result. `scripts/verify-source.py` independently checks the source bytes,
fixture manifest, SQLite integrity, expected tables/views, and the three
Northwind order IDs.

```sh
python3 scripts/verify-source.py
python3 /path/to/demo-db-websites/scripts/provider-tools/generate.py --root .
git diff --exit-code
```

The read-only OVDB endpoint declares schema, keyed-read, and query
capabilities (observed 2026-10-22). The declared Northwind relationship identifies compatible order
identifiers; it is dataset metadata, not a SQL foreign key or an automatic
cross-database join.
