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
QUEUE_LIMIT = 15
MIN_QUEUE_ITEMS = 8
DEFAULT_MIX_TARGET = {"independent": 0.60, "official": 0.40}
RELEVANCE_MIN_SCORE = 0.55
MAX_FEED_ITEMS = 40
FALLBACK_LOOKBACK_DAYS = 21


CONTENT_TYPE_WEIGHTS = {
    "update": 1.0,
    "guide": 0.95,
    "howto": 0.92,
    "demo": 0.88,
    "build_report": 0.85,
    "release_notes": 0.82,
    "analysis": 0.72,
    "news": 0.58,
    "marketing": 0.35,
    "other": 0.55,
}


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
        for e in entries[:MAX_FEED_ITEMS]:
            title = text(e.findtext("atom:title", default="", namespaces=ns))
            link_el = e.find("atom:link", ns)
            link = link_el.attrib.get("href", "") if link_el is not None else ""
            pub = text(e.findtext("atom:updated", default="", namespaces=ns))
            out.append((title, link, pub))
    else:
        for i in root.findall("./channel/item")[:MAX_FEED_ITEMS]:
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


def classify_content_type(title):
    t = title.lower()

    if any(k in t for k in ["release notes", "changelog", "what's new", "whats new", "version", "ga", "general availability", "public preview"]):
        return "update"
    if any(k in t for k in ["step-by-step", "walkthrough", "how to", "how-to", "tutorial"]):
        return "howto"
    if any(k in t for k in ["guide", "playbook", "best practices", "reference architecture"]):
        return "guide"
    if any(k in t for k in ["demo", "sample", "example", "showcase"]):
        return "demo"
    if any(k in t for k in ["we built", "case study", "in production", "implementation", "lessons learned"]):
        return "build_report"
    if any(k in t for k in ["release wave", "monthly update", "patch notes"]):
        return "release_notes"
    if any(k in t for k in ["analysis", "deep dive", "benchmark", "comparison"]):
        return "analysis"
    if any(k in t for k in ["announcing", "launch", "news", "recap"]):
        return "news"
    if any(k in t for k in ["webinar", "event", "register", "sponsored", "keynote"]):
        return "marketing"
    return "other"


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


def weekly_window(now):
    week_start = (now - dt.timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    previous_week_start = week_start - dt.timedelta(days=7)
    return previous_week_start, week_start


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

    content_type = classify_content_type(title)
    content_type_weight = CONTENT_TYPE_WEIGHTS.get(content_type, CONTENT_TYPE_WEIGHTS["other"])
    content_adjustment = (content_type_weight - 0.50) * 0.30

    quality = (source_priority * 0.55) + (trust * 0.30) + (content_type_weight * 0.15) + content_adjustment - title_penalty
    return max(0.0, min(1.0, quality)), content_type, round(content_type_weight, 4)


def total_score(freshness, quality, relevance):
    return round((freshness * 0.35) + (quality * 0.35) + (relevance * 0.30), 4)


def relevance_score(title, source_area, content_type):
    t = (title or "").lower()
    area = (source_area or "").lower()

    ai_core = [
        "agent", "agentic", "copilot", "copilot studio", "foundry", "azure ai",
        "semantic kernel", "autogen", "mcp", "llm", "prompt", "rag", "grounding"
    ]
    ai_ops = [
        "governance", "guardrail", "policy", "eval", "evaluation", "orchestration",
        "automation", "ai", "genai"
    ]
    platform_context = [
        "power platform", "power apps", "power automate", "dataverse", "m365", "microsoft 365", "teams", "graph"
    ]
    off_topic = [
        "windows", "xbox", "surface", "gaming", "holiday", "conference recap",
        "career", "job", "culture", "merch", "investor", "ceo", "leadership change"
    ]

    has_ai_core = any(k in t for k in ai_core)
    has_ai_ops = any(k in t for k in ai_ops)
    has_platform_context = any(k in t for k in platform_context) or any(k in area for k in ["power platform", "m365", "foundry"])

    # Hard gate: keep Microsoft ecosystem context, but require explicit AI/agent signal.
    if not (has_ai_core or has_ai_ops):
        return 0.0

    score = 0.0
    score += 0.60 if has_ai_core else 0.0
    score += 0.20 if has_ai_ops else 0.0
    score += 0.15 if has_platform_context else 0.0

    if content_type in {"marketing", "news"}:
        score -= 0.20
    if any(k in t for k in off_topic):
        score -= 0.55

    return max(0.0, min(1.0, round(score, 4)))


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
    fallback_items = []
    seen = set()
    now = dt.datetime.now(dt.timezone.utc)
    window_start, window_end = weekly_window(now)
    fallback_start = window_start - dt.timedelta(days=FALLBACK_LOOKBACK_DAYS)

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

                parsed_pub = parse_date(pub)
                if not parsed_pub:
                    excluded.append({"url": link, "reason": "missing_or_invalid_published_at"})
                    continue
                if parsed_pub.tzinfo is None:
                    parsed_pub = parsed_pub.replace(tzinfo=dt.timezone.utc)
                parsed_pub_utc = parsed_pub.astimezone(dt.timezone.utc)

                confidence = "High" if s.get("trust") == "official" else "Medium"
                tags = classify(title, s.get("product_area", "Mixed"))
                freshness = recency_score(pub, now)
                quality, content_type, content_type_weight = quality_score(s, title)
                relevance = relevance_score(title, s.get("product_area", "Mixed"), content_type)
                if relevance < RELEVANCE_MIN_SCORE:
                    excluded.append({"url": link, "reason": "low_relevance", "relevance": relevance})
                    continue
                score = total_score(freshness, quality, relevance)
                source_bucket = "official" if s.get("trust") == "official" else "independent"

                item = {
                    "id": key,
                    "title": title,
                    "url": link,
                    "canonical_url": link,
                    "author": "",
                    "publisher": s["name"],
                    "published_at": pub or now.isoformat(),
                    "published_at_utc": parsed_pub_utc.isoformat(),
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
                    "content_type": content_type,
                    "score_freshness": round(freshness, 4),
                    "score_quality": round(quality, 4),
                    "score_content_type": content_type_weight,
                    "score_relevance": relevance,
                    "score_total": score,
                }

                if window_start <= parsed_pub_utc < window_end:
                    items.append(item)
                elif fallback_start <= parsed_pub_utc < window_start:
                    item["fallback_reason"] = "recent_pre_window_backfill"
                    fallback_items.append(item)
                else:
                    excluded.append({
                        "url": link,
                        "reason": "outside_collection_window",
                        "published_at": parsed_pub_utc.isoformat(),
                    })
        except Exception as e:
            excluded.append({"source": s["id"], "reason": f"fetch_error: {e}"})

    top = select_mix_scored(items, QUEUE_LIMIT, mix_target)
    fallback_used = 0
    if len(top) < MIN_QUEUE_ITEMS and fallback_items:
        needed = MIN_QUEUE_ITEMS - len(top)
        fallback_ranked = sorted(fallback_items, key=lambda x: x["score_total"], reverse=True)
        top.extend(fallback_ranked[:needed])
        fallback_used = min(needed, len(fallback_ranked))

    top = sorted(top, key=lambda x: x["score_total"], reverse=True)[:QUEUE_LIMIT]
    included_official = len([i for i in top if i["source_mix_bucket"] == "official"])
    included_independent = len(top) - included_official

    queue = {
        "issue_id": args.issue_id,
        "generated_at": now.isoformat(),
        "window_start_utc": window_start.isoformat(),
        "window_end_utc": window_end.isoformat(),
        "fallback_start_utc": fallback_start.isoformat(),
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
        "selection_stats": {
            "in_window_count": len(items),
            "fallback_pool_count": len(fallback_items),
            "fallback_used_count": fallback_used,
            "target_min_items": MIN_QUEUE_ITEMS,
            "queue_limit": QUEUE_LIMIT,
        },
        "scoring_notes": {
            "freshness": "Based on published date recency bands (<=3d highest, >30d lowest).",
            "quality": "Based on source priority + trust + title noise penalty.",
            "content_type": "Weighted toward updates/guides/how-tos/demos/build reports; down-ranks marketing/news-noise.",
            "relevance": "Boosts agentic AI/Copilot/Foundry/automation/governance topics and filters low-signal items.",
            "total": "score_total = freshness*0.35 + quality*0.35 + relevance*0.30.",
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
        f"Date window (UTC): {queue['window_start_utc']} to {queue['window_end_utc']} (end exclusive)",
        f"Fallback lookback (UTC): {queue['fallback_start_utc']} to {queue['window_start_utc']} (used when in-window volume < {MIN_QUEUE_ITEMS})",
        "",
        "## Source mix tuning",
        "",
        f"- Target mix: independent {mix_target.get('independent', 0):.0%} / official {mix_target.get('official', 0):.0%}",
        f"- Actual mix: independent {queue['mix_actual']['independent']:.1%} ({queue['mix_actual']['independent_count']}) / official {queue['mix_actual']['official']:.1%} ({queue['mix_actual']['official_count']})",
        f"- In-window candidates: {queue['selection_stats']['in_window_count']} · fallback candidates: {queue['selection_stats']['fallback_pool_count']} · fallback used: {queue['selection_stats']['fallback_used_count']}",
        "",
        "## Freshness + quality scoring notes",
        "",
        f"- Freshness: {queue['scoring_notes']['freshness']}",
        f"- Quality: {queue['scoring_notes']['quality']}",
        f"- Content type: {queue['scoring_notes']['content_type']}",
        f"- Relevance: {queue['scoring_notes']['relevance']}",
        f"- Total: {queue['scoring_notes']['total']}",
        "",
        "## Top candidates",
        ""
    ]
    for i, it in enumerate(top[:15], start=1):
        lines += [
            f"{i}. **{it['title']}**",
            f"   - Publisher: {it['publisher']} ({it['source_mix_bucket']})",
            f"   - Type: {it['content_type']} (weight {it['score_content_type']:.2f})",
            f"   - Scores: total {it['score_total']:.2f} · freshness {it['score_freshness']:.2f} · quality {it['score_quality']:.2f} · relevance {it['score_relevance']:.2f}",
            f"   - Confidence: {it['confidence']}",
            f"   - URL: {it['canonical_url']}",
        ]
    lines += ["", "## Questions for Liam", ""] + [f"- {q}" for q in queue["questions_for_liam"]]
    q_md.write_text("\n".join(lines), encoding="utf-8")
    print(str(q_json))
    print(str(q_md))


if __name__ == "__main__":
    main()
