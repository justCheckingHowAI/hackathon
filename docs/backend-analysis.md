# Gemellus — Analiza backendu i kontekst dla frontendu

## Czym jest Gemellus?

Multimodalny agent AI, który po odejsciu kluczowego pracownika:
1. **Klonuje jego wiedze** — tworzy cyfrowego bliźniaka na bazie danych z GitHub, transkrypcji, dokumentacji, Slacka
2. **Generuje pakiet rekrutacyjny** — opis stanowiska, scorecard, pytania do rozmowy, kryteria oceny
3. **Screenuje kandydatów** — rozmowa głosowa przez Vapi + matching score

---

## Obecny stan backendu

### API (`/api/main.py`)
- **Framework:** FastAPI 0.116.1 + Uvicorn
- **Porty:** 8001 (dev), 80 (Docker)
- **Endpointy:**

| Metoda | Route | Odpowiedź |
|--------|-------|-----------|
| GET | `/` | `{"message": "Hello from FastAPI"}` |
| GET | `/health` | `{"status": "ok"}` |

Backend jest **szkieletem** — logika biznesowa jeszcze nie zaimplementowana.

### Zależności
```
fastapi==0.116.1
uvicorn[standard]==0.35.0
```

Brakujące (do dodania): Google Gemini SDK, Vapi SDK, Google Agent SDK/ADK.

---

## Architektura docelowa

```
┌──────────────────────────────────────────────┐
│           Frontend (React + Vite)             │
│  3 ekrany: Intake → Hiring Pack → Screening  │
└──────────────────┬───────────────────────────┘
                   │ REST API
┌──────────────────▼───────────────────────────┐
│           Backend (FastAPI)                    │
│  ├─ Endpointy agenta                         │
│  ├─ Generowanie pakietu rekrutacyjnego       │
│  └─ Zarządzanie wiedzą/kontekstem            │
└──────────┬──────────────┬────────────────────┘
           │              │
┌──────────▼──────┐ ┌────▼─────────────────────┐
│  Google Gemini  │ │  Vapi (voice layer)       │
│  + Agent SDK    │ │  telefon / audio / STT    │
│  2M context     │ └──────────────────────────┘
└─────────────────┘
```

---

## Dane i baza wiedzy

### Zebrane dane (Mike Grabowski — persona testowa)

| Źródło | Format | Lokalizacja |
|--------|--------|-------------|
| GitHub PRs, commity, issues, reviews | JSON | `/data/mike-data/raw/github/` |
| Transkrypcje konferencji | TXT | `/data/mike-data/raw/talks/` |
| Transkrypcje podcastów | TXT | `/data/mike-data/raw/podcast/` |
| Dokumentacja techniczna | MD | `/data/mike-data/raw/docs/` |
| Posty, Q&A | MD | `/data/mike-data/raw/written/` |
| Syntetyczne: Slack, Jira, 1:1 | JSON/MD | `/data/mike-data/raw/synthetic/` |

### Pipeline danych
```
fetch_*.py → JSON/TXT/MD → assemble_context.py → full-context.md → Gemini (2M tokens)
```

Finalny plik: `/data/mike-data/processed/full-context.md` — jeden duży dokument ładowany do kontekstu Gemini.

---

## 3 ekrany frontendu (z planu demo)

### Ekran 1: Team Knowledge Intake
**Cel:** Wskazanie osoby odchodzącej i jej artefaktów wiedzy.

Potrzebne elementy UI:
- Upload / podgląd 2-3 artefaktów (repozytoria, transkrypcje, dokumenty)
- Wskazanie osoby, która odchodzi (profil Mike'a)
- Przycisk "Uruchom analizę"
- Status/progress analizy

**Oczekiwane API:**
- `POST /analyze` — uruchomienie analizy osoby (przesłanie artefaktów lub wskazanie osoby)
- `GET /persons` — lista dostępnych osób/klon

### Ekran 2: Backfill Hiring Pack
**Cel:** Prezentacja wyników analizy i wygenerowanego pakietu.

Potrzebne elementy UI:
- **Skill Evidence Map** — wykryte kompetencje z cytatami ze źródeł
- **Gap Summary** — jakie kompetencje/odpowiedzialności znikają po odejściu
- **Recommended Role** — rekomendowana rola do zatrudnienia
- **Scorecard** — kryteria oceny z wagami
- **Interview Questions** — bank pytań do rozmowy
- **Must-have vs Nice-to-have** — profil idealnego kandydata
- **Red Flags** — sygnały ostrzegawcze

Kluczowe: każda rekomendacja musi mieć **evidence snippets** (cytaty ze źródeł), nie tylko wygenerowany tekst.

**Oczekiwane API:**
- `GET /hiring-pack/{person_id}` — pobranie wygenerowanego pakietu
- Struktura odpowiedzi:
```json
{
  "person": { "name": "Mike Grabowski", "role": "..." },
  "skills": [
    { "name": "React Native", "evidence": ["PR #123: ...", "Talk: ..."], "level": "expert" }
  ],
  "gap_summary": "...",
  "recommended_role": { "title": "...", "description": "..." },
  "scorecard": [
    { "criterion": "...", "weight": 0.3, "description": "..." }
  ],
  "interview_questions": ["..."],
  "must_have": ["..."],
  "nice_to_have": ["..."],
  "red_flags": ["..."]
}
```

### Ekran 3: Candidate Screen
**Cel:** Screening kandydata (CV + rozmowa głosowa).

Potrzebne elementy UI:
- Upload CV (PDF)
- Przycisk uruchamiający rozmowę głosową przez Vapi
- Wizualizacja rozmowy w trakcie (transkrypcja live lub po fakcie)
- **Match Score** — procentowe dopasowanie kandydata
- **Fit Summary** — structured summary dopasowania
- Evidence-based uzasadnienie oceny

**Oczekiwane API:**
- `POST /candidates/upload-cv` — upload CV kandydata
- `POST /candidates/start-screening` — uruchomienie sesji voice screening
- `GET /candidates/{id}/result` — wynik screeningu

---

## Przepływ demo (3 minuty)

| Czas | Co się dzieje | Ekran |
|------|---------------|-------|
| 0:00–0:40 | Przedstawienie problemu + pokazanie załadowanych danych Mike'a | Ekran 1 |
| 0:40–1:30 | Analiza → skill gap → wygenerowany hiring pack | Ekran 2 |
| 1:30–2:20 | Upload CV kandydata + voice screening przez Vapi | Ekran 3 |
| 2:20–3:00 | Match score + rekomendacja dla hiring teamu | Ekran 3 |

---

## Kluczowe wymagania dla frontendu

1. **Evidence-first** — każdy output musi pokazywać źródło (cytat z PR, transkrypcji itp.)
2. **Multimodalność widoczna** — UI musi jasno pokazywać różne typy danych wejściowych (tekst, głos, PDF)
3. **Wizualizacja procesu agenta** — opcjonalnie: panel "pod maską" pokazujący jakie narzędzia agent wywołał
4. **Responsywność** — loading states, progress bary (analiza może trwać kilka-kilkanaście sekund)
5. **Prostota** — 3 ekrany, liniowy flow, bez rozbudowanej nawigacji
6. **Framing** — "assists hiring teams", nigdy "decides who to hire"

---

## Docker

```yaml
# dev-docker-compose.yml
services:
  app:   # Frontend — port 8000
    build: ./app
    ports: ["8000:80"]
  api:   # Backend — port 8001
    build: ./api
    ports: ["8001:80"]
```

Frontend buildowany przez Vite → serwowany przez Nginx. Backend przez Uvicorn.

---

## Tech stack frontendu (aktualny)

- React 19 + TypeScript
- Vite 8 (build + HMR)
- ESLint + TypeScript ESLint
- Aktualnie: boilerplate Vite (counter demo), do zastąpienia

---

## Co jeszcze warto wiedzieć

- **Persona testowa:** Mike Grabowski (prawdziwa osoba, prawdziwe publiczne dane)
- **Nazwa produktu:** Gemellus (gemellus.app)
- **Wyróżnik vs NotebookLM:** generowanie pakietu rekrutacyjnego (nie tylko Q&A)
- **Zespół:** Max + Janusz (backend/dev), Adam (dane), Przemek + Mieszko (produkt/narracja/UI)
- **Baza danych:** na razie brak — wszystko w kontekście Gemini (2M tokenów). Przyszłość: Neo4j
