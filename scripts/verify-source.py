#!/usr/bin/env python3
"""Verify the immutable Shipping source and its public provenance."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data-source/base.sqlite"
FIXTURE_MANIFEST = ROOT / "data-source/fixture-manifest.json"
EXPECTED_SHA256 = "73f0d871607ee5b24de68b5398c25806f556a3126a31e1865fee79b2881977e0"
EXPECTED_SIZE = 110592
EXPECTED_LICENSE_SHA256 = "a2010f343487d3f7618affe54f789f5487602331c0a8d03f49e9a7c547cf0499"
EXPECTED_MANIFEST_SHA256 = "fd9c22c47ea5ab589e4e0b00a6bb2b86de6046a678d078684f7feb8422878ab1"
EXPECTED_INTRODUCED_REVISION = "38a51dda39d988f2d2bcf23703bd1a969d49f4a3"
EXPECTED_OBJECTS = {
    "assignments",
    "attempts",
    "configurations",
    "current_routes",
    "events",
    "latest_attempts",
    "partners",
    "publications",
    "receipts",
    "requests",
    "routes",
    "workspace_state",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    provider = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    require(
        provider["source"]["introducedRevision"] == EXPECTED_INTRODUCED_REVISION,
        "fixture introduction revision differs",
    )
    license_digest = hashlib.sha256((ROOT / "LICENSE").read_bytes()).hexdigest()
    require(license_digest == EXPECTED_LICENSE_SHA256, f"unexpected CC0 license sha256: {license_digest}")
    manifest_digest = hashlib.sha256(FIXTURE_MANIFEST.read_bytes()).hexdigest()
    require(manifest_digest == EXPECTED_MANIFEST_SHA256, f"unexpected fixture manifest sha256: {manifest_digest}")
    source = SOURCE.read_bytes()
    require(len(source) == EXPECTED_SIZE, f"unexpected source size: {len(source)}")
    digest = hashlib.sha256(source).hexdigest()
    require(digest == EXPECTED_SHA256, f"unexpected source sha256: {digest}")

    fixture = json.loads(FIXTURE_MANIFEST.read_text(encoding="utf-8"))
    require(fixture["database"]["bytes"] == EXPECTED_SIZE, "fixture size pin differs")
    require(fixture["database"]["sha256"] == EXPECTED_SHA256, "fixture hash pin differs")
    require(fixture["synthetic"] is True, "fixture must remain explicitly synthetic")

    with sqlite3.connect(f"file:{SOURCE}?mode=ro", uri=True) as db:
        require(db.execute("PRAGMA integrity_check").fetchone() == ("ok",), "integrity check failed")
        objects = {
            name
            for (name,) in db.execute(
                "SELECT name FROM sqlite_schema WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%'"
            )
        }
        require(objects == EXPECTED_OBJECTS, f"unexpected schema objects: {sorted(objects)}")
        orders = [row[0] for row in db.execute(
            "SELECT order_id FROM requests WHERE order_id IN (11038,11045,11062) ORDER BY order_id"
        )]
        require(orders == [11038, 11045, 11062], f"missing investigation orders: {orders}")
        try:
            db.execute("CREATE TABLE must_not_write(value TEXT)")
        except sqlite3.OperationalError as error:
            require("readonly" in str(error).lower(), f"unexpected write refusal: {error}")
        else:
            raise SystemExit("read-only source connection unexpectedly accepted a write")

    print(f"verified immutable Shipping source {digest} ({len(source)} bytes)")


if __name__ == "__main__":
    main()

