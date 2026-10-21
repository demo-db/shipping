# Shipping

Shipping is a synthetic companion to Northwind for investigating request,
routing, receipt, attempt, and event histories. The published fixture includes
the healthy order `11038`, blocked order `11045`, and pending order `11062`.
Explore it at <https://shipping.demodb.dev/>.

The checked-in SQLite file is copied byte-for-byte from the public
`datatug/datatug-demo-project` fixture at revision
`cb841345e88d01229857b2bdb51cc07f4ef4bec7`. It is CC0-1.0 licensed and has
SHA-256 `73f0d871607ee5b24de68b5398c25806f556a3126a31e1865fee79b2881977e0`.
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

The read-only OVDB endpoint supports schema, keyed reads, and queries. The
declared Northwind relationship identifies compatible order identifiers; it is
dataset metadata, not a SQL foreign key or an automatic cross-database join.
