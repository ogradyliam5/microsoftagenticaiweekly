#!/usr/bin/env python3
import argparse
import datetime as dt
import email.utils
import json
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUEUE_LIMIT = 24
DEFAULT_MIX_TARGET = {"independent": 0.60, "official": 0.40}


def text(v):
    return (v or "").strip()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:80]


def fetch_rss(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def parse_feed(raw):
    out = []
    root = ET.fromstring(raw)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    if root.tag.endswith("feed"):
        entries = root.findall("atom:entry", ns)
        for e in entries[:12]:
            title = text(e.findtext("atom:title", default="", namespaces=ns))
            link_el = e.find("atom:link", ns)
            link = link_el.attrib.get("href", "") if link_el is not None else ""
            pub = text(e.findtext("atom:updated", default="", namespaces=ns))
            out.append((title, link, pub))
    else:
        for i in root.findall("./channel/item")[:12]:
            title = text(i.findtext("title", default=""))
            link = text(i.findtext("link", default=""))
            pub = text(i.findtext("pubDate", default=""))
            out.append((title, link, pub))
    return out


def classify(title, source_area):
    t = title.lower()
    tags = []
    if source_area == "Power Platform" or any(k in t for k in ["copilot studio", "power automate", "power apps", "dataverse"]):
        tags.append("Power Platform")
    if source_area == "M365" or any(k in t for k in ["microsoft 365", "teams", "graph"]):
        tags.append("M365")
    if source_area == "Foundry" or any(k in t for k in ["azure ai", "foundry", "agent", "model"]):
        tags.append("Foundry")
    return tags or [source_area]


def parse_date(value):
    if not value:
        return None
    try:
        return email.utils.parsedate_to_datetime(value)
    except Exception:
        pass
    try:
        normalized = value.replace("Z", "+00:00")
        return dt.datetime.fromisoformat(normalized)
    except Exception:
        return None


def recency_score(published_at, now):
    parsed = parse_date(published_at)
    if not parsed:
        return 0.30
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    age_days = (now - parsed.astimezone(dt.timezone.utc)).total_seconds() / 86400
    if age_days <= 3:
        return 1.0
    if age_days <= 7:
        return 0.85
    if age_days <= 14:
        return 0.60
    if age_days <= 30:
        return 0.35
    return 0.15


def quality_score(source, title):
    title_l = title.lower()
    source_priority = min(max(source.get("priority", 5), 1), 10) / 10
    trust = 1.0 if source.get("trust") == "official" else 0.85
    title_penalty = 0.10 if any(k in title_l for k in ["roundup", "link list", "week in review"]) else 0.0
    return max(0.0, min(1.0, (source_priority * 0.65) + (trust * 0.35) - title_penalty))


def total_score(freshness, quality):
    return round((freshness * 0.55) + (quality * 0.45), 4)


def select_mix_scored(items, limit, mix_target):
    official_target = round(limit * mix_target.get("official", DEFAULT_MIX_TARGET["official"]))
    independent_target = limit - official_target

    official_pool = sorted([i for i in items if i["source_mix_bucket"] == "official"], key=lambda x: x["score_total"], reverse=True)
    independent_pool = sorted([i for i in items if i["source_mix_bucket"] == "independent"], key=lambda x: x["score_total"], reverse=True)

    selected = independent_pool[:independent_target] + official_pool[:official_target]
    if len(selected) < limit:
        leftovers = [i for i in sorted(items, key=lambda x: x["score_total"], reverse=True) if i not in selected]
        selected.extend(leftovers[: limit - len(selected)])

    return sorted(selected[:limit], key=lambda x: x["score_total"], reverse=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue-id", required=True)
    args = ap.parse_args()

    source_doc = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
    sources = source_doc["sources"]
    mix_target = source_doc.get("mix_target", DEFAULT_MIX_TARGET)

    items, excluded = [], []
    seen = set()
    now = dt.datetime.now(dt.timezone.utc)

    for s in sources:
        if s["type"] not in {"rss", "github"}:
            excluded.append({"source": s["id"], "reason": "manual/non-fetch source"})
            continue
        try:
            raw = fetch_rss(s["url"])
            for title, link, pub in parse_feed(raw):
                if not title or not link:
                    continue
                key = slug(title)
                if key in seen:
                    excluded.append({"url": link, "reason": "duplicate_title"})
                    continue
                seen.add(key)

                confidence = "High" if s.get("trust") == "official" else "Medium"
                tags = classify(title, s.get("product_area", "Mixed"))
                freshness = recency_score(pub, now)
                quality = quality_score(s, title)
                score = total_score(freshness, quality)
                source_bucket = "official" if s.get("trust") == "official" else "independent"

                items.append({
                    "id": key,
                    "title": title,
                    "url": link,
                    "canonical_url": link,
                    "author": "",
                    "publisher": s["name"],
                    "published_at": pub or now.isoformat(),
                    "fetched_at": now.isoformat(),
                    "product_area": s.get("product_area", "Mixed"),
                    "source_type": s["type"],
                    "summary_bullets": ["Auto-collected candidate. Editorial rewrite required before publishing."],
                    "why_it_matters": "Potentially relevant update for Microsoft Agentic AI builders.",
                    "audience": "Dev",
                    "effort": "TBD during editorial review",
                    "confidence": confidence,
                    "tags": tags + (["Official"] if confidence == "High" else ["Community"]),
                    "evidence": [f"Source title: {title[:90]}"],
                    "source_mix_bucket": source_bucket,
                    "score_freshness": round(freshness, 4),
                    "score_quality": round(quality, 4),
                    "score_total": score,
                })
        except Exception as e:
            excluded.append({"source": s["id"], "reason": f"fetch_error: {e}"})

    top = select_mix_scored(items, QUEUE_LIMIT, mix_target)
    included_official = len([i for i in top if i["source_mix_bucket"] == "official"])
    included_independent = len(top) - included_official

    queue = {
        "issue_id": args.issue_id,
        "generated_at": now.isoformat(),
        "items": top,
        "clusters": [],
        "excluded": excluded,
        "mix_target": mix_target,
        "mix_actual": {
            "official": round(included_official / len(top), 3) if top else 0,
            "independent": round(included_independent / len(top), 3) if top else 0,
            "official_count": included_official,
            "independent_count": included_independent,
        },
        "scoring_notes": {
            "freshness": "Based on published date recency bands (<=3d highest, >30d lowest).",
            "quality": "Based on source priority + trust, with light title noise penalty.",
            "total": "score_total = freshness*0.55 + quality*0.45.",
        },
        "questions_for_liam": [
            "Any sources to add/remove this week? (approval required)",
            "Any item titles that should be down-ranked as noise?"
        ]
    }

    art = ROOT / "artifacts"
    art.mkdir(exist_ok=True)
    q_json = art / f"editorial_queue-{args.issue_id}.json"
    q_md = art / f"editorial_queue-{args.issue_id}.md"
    q_json.write_text(json.dumps(queue, indent=2), encoding="utf-8")

    lines = [
        f"# Weekly Editorial Queue — {args.issue_id}",
        "",
        f"Generated: {queue['generated_at']}",
        f"Total included: {len(top)}",
        f"Excluded: {len(excluded)}",
        "",
        "## Source mix tuning",
        "",
        f"- Target mix: independent {mix_target.get('independent', 0):.0%} / official {mix_target.get('official', 0):.0%}",
        f"- Actual mix: independent {queue['mix_actual']['independent']:.1%} ({queue['mix_actual']['independent_count']}) / official {queue['mix_actual']['official']:.1%} ({queue['mix_actual']['official_count']})",
        "",
        "## Freshness + quality scoring notes",
        "",
        f"- Freshness: {queue['scoring_notes']['freshness']}",
        f"- Quality: {queue['scoring_notes']['quality']}",
        f"- Total: {queue['scoring_notes']['total']}",
        "",
        "## Top candidates",
        ""
    ]
    for i, it in enumerate(top[:15], start=1):
        lines += [
            f"{i}. **{it['title']}**",
            f"   - Publisher: {it['publisher']} ({it['source_mix_bucket']})",
            f"   - Scores: total {it['score_total']:.2f} · freshness {it['score_freshness']:.2f} · quality {it['score_quality']:.2f}",
            f"   - Confidence: {it['confidence']}",
            f"   - URL: {it['canonical_url']}",
        ]
    lines += ["", "## Questions for Liam", ""] + [f"- {q}" for q in queue["questions_for_liam"]]
    q_md.write_text("\n".join(lines), encoding="utf-8")
    print(str(q_json))
    print(str(q_md))


if __name__ == "__main__":
    main()
