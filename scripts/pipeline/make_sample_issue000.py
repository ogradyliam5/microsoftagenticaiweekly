#!/usr/bin/env python3
import datetime as dt
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

issue_id = "000"
now = dt.datetime.utcnow().isoformat() + "Z"

sample_items = [
  {
    "id": "sample-official-copilot-studio",
    "title": "Sample: Copilot Studio capability update",
    "url": "https://example.com/official-copilot-update",
    "canonical_url": "https://example.com/official-copilot-update",
    "author": "",
    "publisher": "Microsoft (sample)",
    "published_at": now,
    "fetched_at": now,
    "product_area": "Power Platform",
    "source_type": "rss",
    "summary_bullets": ["Sample draft item for pipeline verification only."],
    "why_it_matters": "Demonstrates issue generation format.",
    "audience": "Architect",
    "effort": "Low",
    "confidence": "High",
    "tags": ["Power Platform", "Official"],
    "evidence": ["Sample source title for validation."]
  },
  {
    "id": "sample-community-foundry",
    "title": "Sample: Foundry agent ops pattern",
    "url": "https://example.com/foundry-pattern",
    "canonical_url": "https://example.com/foundry-pattern",
    "author": "",
    "publisher": "Community (sample)",
    "published_at": now,
    "fetched_at": now,
    "product_area": "Foundry",
    "source_type": "rss",
    "summary_bullets": ["Sample community item for queue + issue rendering."],
    "why_it_matters": "Shows confidence and attribution fields.",
    "audience": "Dev",
    "effort": "Medium",
    "confidence": "Medium",
    "tags": ["Foundry", "Community"],
    "evidence": ["Sample evidence snippet."]
  }
]

queue = {
  "issue_id": issue_id,
  "generated_at": now,
  "items": sample_items,
  "clusters": [],
  "excluded": [],
  "questions_for_liam": ["Sample run only: approve moving to live ingestion."]
}

(ART / f"editorial_queue-{issue_id}.json").write_text(json.dumps(queue, indent=2), encoding="utf-8")
(ART / f"editorial_queue-{issue_id}.md").write_text(
  "# Weekly Editorial Queue — 000\n\nSample pipeline artifact for verification.", encoding="utf-8"
)

posts = ROOT / "posts"
drafts = ROOT / "drafts"
posts.mkdir(exist_ok=True)
drafts.mkdir(exist_ok=True)

(posts / "issue-000.md").write_text(
  "# Microsoft Agentic AI Weekly — Issue 000\n\nSample issue generated for pipeline verification.",
  encoding="utf-8"
)
(drafts / "email-000.md").write_text(
  "# Microsoft Agentic AI Weekly — Issue 000\n\nSample email draft. Approval required.",
  encoding="utf-8"
)

print("Generated sample Issue 000 artifacts")
