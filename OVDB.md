---
ovdb: 1
publish:
  - ./ovdb.yaml
  - ./ovdb-database.json
---

# Shipping OVDB publication

The descriptors above configure the intended publication of the immutable,
read-only Shipping sample through OpenVaultDB. The endpoint is deployed and
verified (`deploymentVerified` in `manifest.json`); a new revision is served
after the OpenVaultDB provider pin moves to it. Generated schema and recordset
metadata come from the pinned SQLite source rather than a separately maintained
schema.

