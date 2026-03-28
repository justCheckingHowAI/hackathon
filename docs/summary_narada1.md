# Meeting 1 Summary — 2026-03-28

**Source:** `narada1_transkrypcja.txt` (recording 20260328-131721-Rec39.hda)
**Duration:** ~17 minutes
**Participants:** Max, Janusz, Adam, Przemek, Mieszko

---

## Team Composition & Roles

| Person | Role | Hackathon Responsibility |
|--------|------|-------------------------|
| **Max** | Developer (core) | API setup (Google, Vapi), backend development, dev environment |
| **Janusz** | Developer (core) | API setup (Google, Vapi), backend development, dev environment |
| **Adam** | Product / VC experience / vibecodering | Data collection & organization (already has most of it from pre-work) |
| **Przemek** | Product / VC experience / vibecodering | Demo story & narrative, product name, presentation, website, UI |
| **Mieszko** | Creative / artistic | Demo story & narrative (with Przemek), UI design, presentation visuals |

---

## Key Decisions Made

### 1. Clone Target: Mike Grabowski Only

The team agreed to focus exclusively on **Mike Grabowski** for the hackathon MVP. Multi-person cloning is explicitly marked as a **future feature**, not for today.

> "We limit it for now, we don't focus on the whole team, we only support Mike."

Long-term vision discussed: each team member would have their own persona/clone, and you could ask any of them. But for the demo — Mike only.

### 2. Demo Flow — Two-Phase Structure

The team converged on a two-question demo approach:

**Question 1 — Knowledge retrieval:**
> "Mike, you're on vacation, but tell me — what happened in project X and why was that decision made?"

This demonstrates the knowledge clone capability — the agent responds with project context, architectural decisions, and institutional knowledge.

**Question 2 — Hiring / competency gap:**
> "Mike won't be contributing to this project anymore. Who do we need to find? Prepare a hiring pack."

This demonstrates actionable output beyond simple Q&A — the agent generates job descriptions, recruitment tasks, evaluation criteria, and candidate scoring.

### 3. Architecture: Two Core Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Voice layer** | Vapi | Phone call interface, speech-to-text, text-to-speech |
| **Agent brain** | Google Agent SDK (ADK) | Reasoning, knowledge base queries, structured output generation |

The backend process running in ADK can be **visualized during demo** to show what's happening under the hood (tools being called, data being retrieved).

### 4. Data Strategy

- Adam already has **most data collected** from pre-hackathon work (GitHub PRs, podcasts, synthetic data templates)
- Data needs to be organized into a consumable format (Markdown or JSON)
- Data ingestion should have a **refresh function** (not just one-time import)
- For the demo: data is pre-ingested, but the system should show it can update

### 5. Multimodality — Minimum Viable

Team agreed that **two modalities are sufficient** for the hackathon:
- **Voice** (Vapi phone call interaction)
- **Text** (ingested documents, Slack messages, GitHub data)

Optional extras discussed but not committed:
- Video/audio ingestion (e.g., podcast MP4 files)
- Graphics/diagrams processing
- These can be added as features if time permits

### 6. Task Division

| Track | People | Focus |
|-------|--------|-------|
| **Core development** | Max + Janusz | Google API setup, Vapi integration, Agent SDK, backend, dev environment |
| **Data** | Adam | Organize collected data, format for ingestion, knowledge base setup |
| **Product & story** | Przemek + Mieszko | Demo narrative, product name, presentation deck, website, UI design |
| **UI support** | Max + Janusz (later) | Help with frontend/UI for whatever the backend needs to display |

---

## Critical Discussion: NotebookLM Objection

A significant portion of the meeting addressed the concern that the product could be dismissed as **"just NotebookLM with voice"**. This is the most important strategic risk identified.

### The Objection
> "You know what NotebookLM is? You can throw everything in there — GitHub, meetings, transcripts — and it will talk to you just like Mike."

### Counter-Arguments Developed

| Differentiator | NotebookLM | Our System |
|---------------|------------|------------|
| **Auto-updating** | Static — you manually upload sources | Continuously ingests and reindexes new data |
| **Multi-person** | Single knowledge blob, no person separation | Distinct personas per team member, can route questions to the right person |
| **Actionable output** | Conversational Q&A only | Generates hiring packs, job descriptions, recruitment tasks, evaluation criteria |
| **Competency mapping** | No skill extraction | Maps skills to people, identifies gaps, recommends who should handle what |
| **Context window** | Limited (tested with podcast — ran into limits) | Designed for organization-scale data across multiple people |

### Conclusion
The team agreed that **the hiring pack / competency gap feature is the key differentiator**. Without it, the product is vulnerable to the NotebookLM comparison. With it, there's clear additional value.

---

## Product Vision Refined

### Positioning (emerged from discussion)

> A platform for C-level that supports organizational growth by identifying the best competency investments — who to hire, what skills are missing, and how to find the right people.

### Target Users
- **Fast-growing startups** that need to scale teams quickly and precisely
- **Organizations losing key people** who need to understand what knowledge walks out the door
- **Teams without dedicated HR/Chief of Staff** that lack the expertise to define specialized roles

### Use Cases Discussed

| Use Case | Description |
|----------|------------|
| **Key person leaves** | Identify competency gaps, generate hiring pack, find replacement |
| **Key person on vacation** | Query their clone for project knowledge, redistribute tasks |
| **Scaling team** | Analyze roadmap + current capabilities, recommend next hire |
| **Competency gap in project** | "We need evals for React Native — who on the team can do this?" → Routes to the right person's clone |
| **Can't name what you need** | System analyzes work patterns and articulates the role you can't describe yourself |

### The "Can't Name It" Insight

One of the most compelling moments in the discussion:

> "Sometimes you can't name what you're missing. You just say 'I need a good developer who's agile.' But to clone Witek and figure out how to search for someone like him — that's an amazing challenge."

This positions the product as solving a meta-problem: **organizations that don't have the vocabulary to describe the competencies they need**.

---

## Demo Scenario (Agreed Direction)

### Act 1: Knowledge Query
- Call Mike's clone via phone
- Ask about a specific project decision or technical problem
- Mike responds with deep context, referencing real artifacts

### Act 2: Hiring Pack Generation
- Tell Mike: "You won't be contributing anymore. We need someone to handle X. Prepare a hiring pack."
- Mike generates:
  - Job description (specific to actual project needs, not generic)
  - Recruitment tasks (based on real project challenges)
  - Evaluation criteria / scoring rubric
  - Candidate profile with must-have vs nice-to-have skills

### Supporting Visuals
- Show the ADK process (what tools the agent called, what data it retrieved)
- On presentation slides: show the full architecture and data sources
- Generated hiring pack displayed as a polished output

---

## Unresolved / Deferred Items

| Item | Status | Notes |
|------|--------|-------|
| Product name | **Not decided** | Needs to be created (Przemek + Mieszko) |
| Exact demo script with timing | **Not finalized** | Will iterate in ~1 hour after task split |
| Multi-person clone support | **Deferred (future)** | Only Mike for hackathon |
| Auto-ingestion pipeline | **Deferred (future)** | Pre-ingested data for demo, refresh function as stretch goal |
| Website | **To be created** | Przemek + Mieszko responsibility |
| Presentation deck | **To be created** | Przemek + Mieszko responsibility |
| UI for backend display | **To be designed** | Max + Janusz will help once product team defines what's needed |

---

## Next Steps (Immediate)

1. **Max + Janusz** — Set up dev environment, Google API keys, Vapi account, start Agent SDK integration
2. **Adam** — Organize collected Mike Grabowski data into structured format for ingestion
3. **Przemek + Mieszko** — Define demo story, start on product name, begin presentation
4. **All** — Reconvene in ~1 hour to review progress and iterate on demo flow
