#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def fail(msg):
    print(f"VALIDATION_ERROR: {msg}")
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue-id", required=True)
    args = ap.parse_args()

    queue_path = ROOT / "artifacts" / f"editorial_queue-{args.issue_id}.json"
    if not queue_path.exists():
      fail(f"Missing queue file: {queue_path}")

    q = json.loads(queue_path.read_text(encoding="utf-8"))
    items = q.get("items", [])
    if not items:
      fail("No items in editorial queue")

    for i, it in enumerate(items, start=1):
      if not it.get("title"):
        fail(f"Item {i} missing title")
      if not it.get("canonical_url"):
        fail(f"Item {i} missing canonical_url")
      if not it.get("published_at"):
        fail(f"Item {i} missing published_at")
      for b in it.get("summary_bullets", []):
        if len(b) > 220:
          fail(f"Item {i} bullet too long (>220 chars)")
      for ev in it.get("evidence", []):
        if len(ev.split()) > 25:
          fail(f"Item {i} evidence snippet exceeds 25 words")

    print(f"Validation OK: {len(items)} items")


if __name__ == "__main__":
    main()
