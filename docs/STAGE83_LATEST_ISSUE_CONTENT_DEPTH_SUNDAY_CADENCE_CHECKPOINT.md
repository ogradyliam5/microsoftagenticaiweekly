# Stage 83 — Latest-Issue Content Depth + Sunday-Night Cadence Checkpoint

## What changed
- Updated latest-issue generators (`generate_issue.py`, `render_issue_html.py`) so issue metadata uses **Sunday-night** publication framing derived from ISO week (`Sunday night, DD Month YYYY`).
- Reworked per-item narrative summary logic to produce **concrete 4-sentence summaries** with implementation-oriented framing (less generic filler, clearer why-now signal).
- Updated latest-issue HTML shell to match homepage parity:
  - shared theme stylesheet include (`theme-shared.css`)
  - nav label parity (`Latest edition`)
  - footer trust-copy parity (`Source-first methodology in About`)
- Regenerated latest issue artifacts for `2026-10`.

## Checkpoint verification
Commands run:

```bash
python3 scripts/pipeline/generate_issue.py --issue-id 2026-10
python3 scripts/pipeline/render_issue_html.py --issue-id 2026-10
python3 - <<'PY'
from pathlib import Path
import re
md=Path('posts/issue-2026-10.md').read_text()
print('item_count', len(re.findall(r'^### ', md, flags=re.M)))
print('has_coverage_window', 'Coverage window (UTC)' in md)
PY
```

Observed:
- `item_count 8` (meets `>3`; within target range when available)
- `has_coverage_window False` (removed from visible issue output)
- Latest issue now shows: `Published: Sunday night, 08 March 2026`

## Scope guard
Per queue instruction, this stage is a **latest-issue checkpoint only**.

- No sitewide legacy/global copy rollout performed in this stage.
- Stage 84 remains blocked pending human approval checkpoint.
