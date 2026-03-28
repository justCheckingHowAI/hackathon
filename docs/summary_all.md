# Hackathon Plans - Summary & Comparison

## Overview

This document summarizes and compares five hackathon planning documents and one team meeting transcript. All plans converge on a single core idea — a **multimodal voice agent that preserves departing employee knowledge and accelerates backfill hiring** — but differ in scope, architecture, data strategy, and demo approach.

**After Meeting 1 (2026-03-28), several open decisions have been resolved.** See the "Decisions from Meeting 1" section below.

### Documents Analyzed

| File | Author | Focus |
|------|--------|-------|
| `maks-demo-plan.md` | Maks | Product framing, scope control, demo structure |
| `adam-hackathon-plan.md` | Adam | TeamTwin — 3 voice agents, technical architecture |
| `przemek-hackathon-plan.md` | Przemek | OrgBrain — market research, competitive analysis, full-stack architecture |
| `mike-grabowski-cloning-plan.md` | (data plan) | Real-person cloning strategy for Mike Grabowski (CTO Callstack) |
| `kubernetes-data-sourcing-plan.md` | (data plan) | Data sourcing pipeline for Kubernetes SIG-Network contributor |
| `narada1_transkrypcja.txt` | All | Team meeting transcript — key decisions and task division |
| `summary_narada1.md` | (summary) | Detailed meeting summary with decisions, task split, and next steps |

### Team Composition

| Person | Role | Hackathon Focus |
|--------|------|----------------|
| **Max** | Developer (core) | Google API, Vapi, Agent SDK, backend |
| **Janusz** | Developer (core) | Google API, Vapi, Agent SDK, backend |
| **Adam** | Product / VC / vibecoder | Data collection & organization |
| **Przemek** | Product / VC / vibecoder | Demo story, presentation, UI, product name |
| **Mieszko** | Creative / artistic | Demo narrative, UI design, presentation visuals |

---

## Common Ground (all or most plans agree)

### 1. Core Problem

All plans address the same business problem: **critical knowledge loss when key employees leave**. This is the universal trigger, the emotional hook, and the demo entry point.

Key framing across plans:
- Maks: "When a key employee leaves, our multimodal agent turns messy organizational knowledge into a backfill hiring plan in minutes."
- Adam: "What if you could call a colleague who left the company six months ago and ask them anything?"
- Przemek: "Organizations lose over $30,000 per departing employee in knowledge transfer costs."

### 2. Technology Stack

Unanimous agreement on two core technologies:

- **Google Gemini** — multimodal reasoning engine, document/text/code analysis, structured output generation
- **Vapi** — voice agent orchestration platform, telephony, low-latency speech interaction

Both are hackathon sponsor technologies, which strengthens theme alignment scoring.

### 3. Three-Phase Product Flow

Every plan (Maks, Adam, Przemek) describes a variant of the same end-to-end pipeline:

| Phase | Maks | Adam (TeamTwin) | Przemek (OrgBrain) |
|-------|------|-----------------|-------------------|
| **1. Knowledge analysis** | Analyze team artifacts, identify competency gap | Knowledge Clone agent — talk to the "digital twin" | Skills heatmap + departure impact simulation |
| **2. Hiring pack generation** | Gap summary, JD, scorecard, interview questions | Recruitment Generator agent — ultra-specific JD, task, rubric | Role recommendation, transfer plan, hiring materials |
| **3. Candidate screening** | Voice screening via Vapi, match score | AI Interviewer agent — adaptive technical interview | Voice query + real-time scoring dashboard |

### 4. Multimodal Input Requirement

All plans agree: the demo must show at least **3 input modalities** to defend "multimodal agent" theme alignment:
- Text (Slack messages, transcripts, docs)
- Documents/PDFs (CVs, architecture diagrams, KEPs)
- Voice (live conversation with the agent)

### 5. Evidence-Based Output

Strong consensus that agent outputs must include **concrete evidence** (source citations, snippets, confidence scores), not just generated text. This addresses jury skepticism about hallucination and builds trust.

- Maks: "3 concrete evidence snippets are better than 2 pages of generated role description"
- Adam: Agent cites specific meetings ("remember when I said on the March 12 standup...")
- Przemek: "Based on 47 Slack messages and 3 design documents, Sarah Chen has deep expertise"

### 6. Mock / Synthetic Data Strategy

All plans assume **pre-prepared mock data** rather than building a real-time ingestion pipeline during the hackathon. The data plans (Mike, K8s) provide detailed sourcing strategies for realistic content.

### 7. Demo Safety Net

Both Adam and Przemek explicitly recommend: **record a backup demo video** before the live presentation. Maks implicitly supports this through scope minimization.

---

## Divergence Points

### 1. Scope Philosophy

| Plan | Approach | Risk Profile |
|------|----------|-------------|
| **Maks** | Brutally minimal — 3 screens, 3 data sources, one linear flow. Explicitly warns against "building multiple products at once" | Low risk, potentially lower wow factor |
| **Adam (TeamTwin)** | 3 full voice agents, each with distinct personality and function. More ambitious but still focused | Medium risk, strong wow if all agents work |
| **Przemek (OrgBrain)** | Broadest scope — adds Neo4j knowledge graph, D3.js heatmap, WebSocket sync, FastAPI backend, React frontend | Highest risk, highest potential impact |

**Key tension:** Maks explicitly identifies broad scope as the #1 risk, while Przemek proposes the most components. Adam sits in the middle.

### 2. Technical Architecture

| Component | Maks | Adam | Przemek |
|-----------|------|------|---------|
| **AI backbone** | Gemini (unspecified details) | Gemini 3.1 with 2M context window (no RAG needed) | Gemini 2.5 Flash (voice) + Gemini 3 Pro (analysis) |
| **Knowledge storage** | Not specified | Direct context loading into Gemini | Neo4j AuraDB graph database |
| **Backend** | Not specified | Not specified | FastAPI with API endpoints |
| **Frontend** | 3 simple screens | Optional dashboard | React + D3.js visualizations + WebSocket |
| **Voice** | Vapi (basic) | Vapi with 3 configured agents (Squads) | Vapi with synchronized voice + dashboard updates |
| **Embedding** | Not discussed | Not discussed | Gemini Embedding 2 (multimodal embeddings) |

**Key divergence:** Adam bets on Gemini's massive context window to avoid RAG complexity entirely. Przemek builds a proper graph database. Maks intentionally avoids architecture decisions to focus on product.

### 3. Clone Persona / Data Source

| Plan | Who Gets Cloned | Data Type |
|------|----------------|-----------|
| **Maks** | "Ania" — fictional senior backend engineer | Generic mock data |
| **Adam** | "Tomek" — fictional developer | Realistic mock data |
| **Mike plan** | **Mike Grabowski** — real person, CTO of Callstack, React Native core team | Real public data (GitHub PRs, conference talks, podcasts, blog posts) |
| **K8s plan** | Anonymous Kubernetes SIG-Network contributor | Real open-source community data (KEPs, SIG meetings, GitHub, KubeCon talks) |

**Key divergence:** The Mike/K8s plans use **real, publicly available data** from recognizable figures, making the demo far more impressive but raising privacy considerations. The other plans use fictional personas with synthetic data.

### 4. Demo Format

| Plan | Duration | Physical Setup | Key Moment |
|------|----------|---------------|------------|
| **Maks** | 3 min (timed to the second: 0:00-0:40 ingest, 0:40-1:30 gap, 1:30-2:20 screening, 2:20-3:00 result) | Not specified | Match score + recommendation at the end |
| **Adam** | 5 min (3 acts) | **Two physical phones on a table** + screen with dashboard | Agent quotes a specific standup meeting from memory |
| **Przemek** | 3 min | Screen with dashboard | **"Simulate departure"** button triggers instant impact analysis while voice responds simultaneously |

### 5. Product Naming & Pitch

| Plan | Product Name | Pitch Style |
|------|-------------|-------------|
| **Maks** | No name proposed | Functional: "We turn messy company knowledge into hiring action" |
| **Adam** | **TeamTwin** | Emotional: "What if you could call a colleague who left?" |
| **Przemek** | **OrgBrain** (alternatives: KnowledgeGraph.ai, Hivemind) | Data-driven: "$31.5B lost annually to poor knowledge sharing" |

### 6. Market Research Depth

| Plan | Research Level |
|------|---------------|
| **Maks** | None — pure product/demo focus |
| **Adam** | None — pure technical/UX focus |
| **Przemek** | **Extensive** — TechWolf ($53M raised), Eightfold ($2.1B valuation), Gloat ($1B), Interloom ($16.5M), Aware, Glean ($4.6B). McKinsey stats, IDC data, WEF Future of Jobs 2025, Deloitte 2025. Specific pitch numbers: $31.5B (IDC), 42% (Panopto), 87% firms (McKinsey) |

### 7. Privacy & Ethics Stance

| Plan | Position |
|------|----------|
| **Maks** | Warns: never promise automatic hiring, say "assists hiring teams", "final decision remains with the hiring team" |
| **Adam** | Brief closing: "TeamTwin is not a replacement for people" |
| **Przemek** | Specific: needs a "privacy by design" slide, references Aware media backlash from 2024 |
| **Mike plan** | Not addressed — uses real person's public data without explicit consent discussion |

### 8. Data Sourcing Depth

| Plan | Data Strategy |
|------|--------------|
| **Maks** | Abstract — "3 types of data: repo/docs, transcripts, CV" |
| **Adam** | 6 components listed (data ingestion, context builder, agent configs, Gemini integration, output generator, frontend) |
| **Mike plan** | **Extremely detailed** — 4 cloning layers, 11+ GitHub repos with exact commands, 9 YouTube search queries, podcast episodes by name, Reactiflux Q&A transcript URL, Medium/Twitter sources, synthetic data templates (Slack threads, Jira tickets, 1:1 notes, ADRs) |
| **K8s plan** | **Equally detailed** — 7 data categories, folder structure, pipeline steps with time estimates, concrete Slack thread examples, Jira ticket templates, competency profile template, checklist with minimum viable data requirements |

### 9. Unique Contributions Per Plan

| Plan | Unique Element |
|------|---------------|
| **Maks** | Systematic **scoring framework** (Running Code / Innovation / Impact / Theme Alignment) applied to 3 alternative directions. Only plan that explicitly ranks options with criteria |
| **Adam** | **Agent personality** concept — extracting communication style from transcripts to make the clone sound like the real person, not a generic chatbot. Strongest "wow" element |
| **Przemek** | **Synchronized voice + visualization** moment — voice response plays while dashboard updates in real-time via WebSocket. Also: extensive **post-hackathon vision** (M&A due diligence, incident response, onboarding buddy, AI readiness assessment) |
| **Mike plan** | Only plan using a **real, recognizable public figure** — Mike Grabowski is known in the React Native ecosystem. Demo would be immediately credible |
| **K8s plan** | Best-defined **data pipeline and folder structure** — ready to implement with copy-paste commands. Includes time estimates per phase and clear ownership (Dev vs. non-dev tasks) |

---

## Scoring Comparison

All three main plans (Maks, Adam, Przemek) provide self-assessments against hackathon criteria:

| Criterion | Maks (after narrowing) | Adam (TeamTwin) | Przemek (OrgBrain) |
|-----------|----------------------|-----------------|-------------------|
| **Running Code** | 4/5 | 4-5/5 | Not scored (implies 4-5 based on plan) |
| **Innovation & Creativity** | 4/5 | 4-5/5 | Not scored (implies 4-5) |
| **Real-world Impact** | 4/5 | 5/5 | Not scored (extensive market validation) |
| **Theme Alignment** | 4/5 (with voice + multimodal inputs) | 5/5 (3 voice agents on Gemini + Vapi) | 9/10 (voice-first + graph viz + multimodal) |

---

## Task Allocation Comparison

### Maks — No Explicit Allocation
Focuses on what to cut, not who does what. Defines scope constraints as the primary planning tool.

### Adam (TeamTwin) — 5 Phases

| Phase | Time | Focus |
|-------|------|-------|
| Foundation | 2-3h | Mock data prep, Gemini + Vapi setup, proof of concept |
| Knowledge Clone | 2-3h | Context builder, system prompt with personality, multimodal integration |
| Recruitment Generator | 2h | Templates, prompt engineering, voice iteration |
| Interview Agent | 2h | Question bank, adaptive logic, real-time scoring |
| Polish + Demo | 1-2h | Dashboard, end-to-end rehearsal, backup plan |

### Przemek (OrgBrain) — 7-Hour Plan

| Phase | Time | Focus |
|-------|------|-------|
| Setup | 0-1h | Repo init, Vapi account, API keys, React boilerplate, demo script, mock data |
| Core Build | 1-3h | Vapi agent + 3 tools (Dev 1), FastAPI + Neo4j (Dev 2), React dashboard + D3.js (Dev 3) |
| Integration | 3-5h | Voice → API → graph → voice response, frontend → API, end-to-end test |
| Polish | 5-6.5h | Bug fixes, demo path hardening, 3x demo rehearsal |
| Insurance | 6.5h | Record backup video |
| Present | 7-8h | Freeze code, clean browser, present |

### Data Plans — Separate Timelines

| Phase | Mike Plan | K8s Plan |
|-------|-----------|----------|
| Automated data collection | 2-3h | 2-3h |
| Manual/semi-automated collection | 1-2h | — |
| Synthetic data creation | 2-3h | 1.5-2h |
| Profile building | — | 1h |
| Processing & structuring | — | 1h |
| Agent configuration | — | 1-2h |
| **Total** | **5-8h** | **6-9h** |

---

## Risk Matrix (Aggregated)

| Risk | Identified By | Mitigation |
|------|--------------|------------|
| Scope too broad | Maks, Adam | Cut ruthlessly — one flow, 3 inputs max |
| Cannot defend recommendation accuracy | Maks | Evidence layer with source citations |
| Demo looks like "just another RAG SaaS" | Maks | Voice interaction + multimodal inputs make it feel different |
| **"It's just NotebookLM"** | **Meeting 1** | **Hiring pack generation is the must-have differentiator. Also: auto-update, multi-person, competency mapping** |
| Latency issues (Vapi + Gemini) | Adam | Test early, fallback to Gemini Flash |
| Agent sounds robotic | Adam | Tune system prompt with "personality", test voice settings |
| Live demo failure | Adam, Przemek | Record backup video at hour 6.5 |
| Mock data quality | Adam, K8s plan | Invest time in realistic, internally consistent data |
| Privacy backlash | Maks, Przemek | "Privacy by design" slide, "assists" not "decides" framing |
| Too many integrations | Maks | Limit to 2-3 data sources, well-connected in one flow |
| Neo4j adds complexity | (implicit in Przemek) | Consider dropping graph DB if behind schedule — Gemini context window may suffice |

---

## Synthesis: Strengths to Combine

The strongest possible hackathon entry would combine:

1. **From Maks** — Scope discipline, 3-minute demo timing, scoring framework, product framing ("assists hiring teams")
2. **From Adam (TeamTwin)** — Agent personality concept, "call your former colleague" hook, two-phone stage setup, 3-agent architecture
3. **From Przemek (OrgBrain)** — Market research numbers for the pitch ($31.5B, 87%, 42%), synchronized voice + dashboard moment, competitive positioning, post-hackathon vision
4. **From Mike plan** — Real-person data sourcing strategy (adaptable to chosen persona), 4-layer cloning model (knowledge, thinking style, communication style, organizational context)
5. **From K8s plan** — Folder structure, data pipeline commands, checklist-driven readiness, clear Dev/non-dev task ownership

---

## Decisions from Meeting 1 (2026-03-28)

The team meeting resolved most of the previously open decisions. See `summary_narada1.md` for full details.

### Resolved Decisions

| # | Question | Decision |
|---|----------|----------|
| 1 | **Who do we clone?** | **Mike Grabowski** — real person, real public data. Multi-person support is deferred to future. |
| 2 | **Architecture** | **Vapi** (voice layer) + **Google Agent SDK / ADK** (agent brain). No Neo4j — ADK handles knowledge. ADK process can be visualized during demo. |
| 3 | **Demo flow** | Two-phase: (1) Knowledge query — call Mike, ask about a project decision; (2) Hiring pack — ask Mike to generate JD, tasks, criteria for his replacement. |
| 4 | **Multimodality** | Minimum: **voice + text**. Optional extras (video, graphics) if time permits. Two modalities are considered sufficient. |
| 5 | **Data preparation** | Adam organizes pre-collected data (GitHub, podcasts, synthetic). Data must be in Markdown/JSON. Refresh function desired but not required for demo. |
| 6 | **Task division** | Max+Janusz → core dev; Adam → data; Przemek+Mieszko → story, name, presentation, UI. |
| 7 | **What makes it not NotebookLM?** | The hiring pack / competency gap feature is the key differentiator. Auto-updating data and multi-person routing are secondary differentiators. |

### Still Open

| # | Question | Status |
|---|----------|--------|
| 1 | **Product name** | Not decided — Przemek + Mieszko to propose |
| 2 | **Exact demo script with timing** | To be iterated after ~1 hour |
| 3 | **Demo duration** | Not explicitly set (plans range from 3 to 5 min) |
| 4 | **UI specifics** | Product team to define, then devs help implement |
| 5 | **Website** | To be created by Przemek + Mieszko |

### Critical Risk Identified: NotebookLM Comparison

The team spent significant time discussing the risk that a jury member could say: *"This is just NotebookLM with a phone number."*

**Agreed mitigation strategy:**

| Differentiator | NotebookLM | Our System |
|---------------|------------|------------|
| Auto-updating | Static, manual upload | Continuous ingestion and reindexing |
| Multi-person | Single knowledge blob | Distinct per-person personas (future, but shown in architecture) |
| Actionable output | Q&A only | Hiring packs, JDs, recruitment tasks, evaluation criteria |
| Competency mapping | None | Skill extraction, gap identification, person-routing |
| Scale | Limited context | Organization-scale across multiple people |

The hiring pack generation is the **must-have** feature that defends against this objection. Without it, the product is vulnerable.

### Product Vision (Refined in Meeting)

The meeting sharpened the positioning beyond the original plans:

> A platform for C-level that supports organizational growth by identifying the best competency investments — who to hire, what skills are missing, and how to find the right people.

Key insight from discussion: the product solves a **meta-problem** — organizations that can't articulate what competencies they need. The system analyzes work artifacts and translates tacit knowledge into structured hiring requirements.

Target users: fast-growing startups, teams losing key people, organizations without dedicated HR/Chief of Staff.
