# Source Shortlist (Stage 1 Stabilization)

_Last updated: 2026-03-01 06:30 UTC_

Stage 1 remains in approval-first mode: discovery updates were applied only to `data/sources.json -> candidates`, with no direct changes to approved `sources[]`.

## Discovery update (2026-03-01)

### Added to `candidates.add` (pending approval)

1. **Future Work (Vesa Nopanen)** (`futurework-blog`) — https://futurework.blog/feed/
   - Why: strong individual-practitioner signal across Copilot Studio + Microsoft Foundry + M365 Copilot changes.
   - Evidence:
     - https://futurework.blog/2025/11/21/multi-agent-workflows-in-microsoft-copilot-studio/
     - https://futurework.blog/2026/02/10/claude-opus-4-6-now-available-in-microsoft-foundry/

2. **Reshmee Auckloo** (`reshmee-auckloo`) — https://reshmeeauckloo.com/posts/index.xml
   - Why: practical M365 extensibility + Copilot Studio implementation content (Agents Toolkit, Power Automate HTTP triggers, SharePoint MCP).
   - Evidence:
     - https://reshmeeauckloo.com/posts/agentstoolkit-invoking-powerautomate/
     - https://reshmeeauckloo.com/posts/copilot-sharepoint-mcp-tools/

3. **Geert Baeke** (`baeke`) — https://baeke.info/feed/
   - Why: advanced Azure AI/agent engineering depth (Agent Framework, MCP, multi-agent deployment on Azure).
   - Evidence:
     - https://baeke.info/2025/12/07/building-an-ai-agent-server-with-ag-ui-and-microsoft-agent-framework/
     - https://baeke.info/2025/07/18/deploying-a-multi-agent-solution-with-mcp-and-a2a-to-azure-container-apps/

### Removed from `candidates.add`

- None in this run.

### De-duplication / validation notes

- Candidate IDs were deduped by `id`; no pre-existing collisions with the three additions.
- Feed endpoints validated as reachable and parseable during discovery.
- No promotions into `sources[]` were made (approval-first policy preserved).

## Pending candidates (current)

- `forwardforever`
- `megan-v-walker`
- `nishant-rana`
- `readyxrm`
- `eliostruyf`
- `sharepains`
- `michelcarlo`
- `futurework-blog`
- `reshmee-auckloo`
- `baeke`

## Existing known feed issue (unchanged)

- `azure-updates` — XML parse failure (`not well-formed (invalid token): line 5, column 31`)
