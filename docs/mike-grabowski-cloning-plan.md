# TeamTwin - Plan Klonowania Mike'a Grabowskiego

## Kim jest Mike Grabowski (@grabbou)

- **Rola:** CTO & Co-Founder, Callstack
- **GitHub:** github.com/grabbou
- **Specjalizacja:** React Native Core Team member, odpowiedzialny za release process RN, twórca rnpm (merged into RN core), architekt Re.Pack i Module Federation dla RN, CLI i auto-linking
- **Konferencje:** React Native EU (współorganizator), React Summit, Chain React, App.js Conf
- **Podcast:** The React Native Show / React Universe On Air (host)
- **Styl:** Praktyczny, nastawiony na DX (Developer Experience), myśli w kategoriach ekosystemu i toolingu

---

## Strategia Klonowania - Co Dokładnie Kopiujemy

### WARSTWA 1: Wiedza techniczna (co Mike wie)

To jest fundament - zbieramy dowody na to, jakie decyzje techniczne Mike podejmował, co budował, jakie problemy rozwiązywał.

**Źródła:**
- PR-y i issues w facebook/react-native (core contributor)
- PR-y w react-native-community/cli (jego dziecko - auto-linking, konfiguracja)
- Architektura Re.Pack (callstack/repack) - Module Federation, webpack for RN
- Historia rnpm - jak i dlaczego został wchłonięty przez RN core
- KEP-podobne dokumenty: RFC-ki, design docs w repo Callstack

### WARSTWA 2: Styl myślenia i decyzje architektoniczne (jak Mike myśli)

To jest to, czego nie znajdziesz w dokumentacji - dlaczego wybrał webpack zamiast Metro, dlaczego auto-linking wygląda tak a nie inaczej.

**Źródła:**
- KubeCon-equivalent talks: React Summit, Chain React, React Native EU
- Podcast episodes (React Native Show) - tu Mike mówi nieformalnie o decyzjach
- Reactiflux Q&A transcript - głęboka rozmowa o RN core
- GitHub discussions i długie komentarze na PR-ach

### WARSTWA 3: Styl komunikacji i "osobowość" (jak Mike mówi)

Żeby agent brzmiał jak Mike, a nie jak generic chatbot.

**Źródła:**
- Twitter/X (@grabbou) - krótkie, ostre opinie
- Medium (@grabbou) - dłuższa forma pisemna
- Transkrypcje talks - jak tłumaczy skomplikowane rzeczy
- Komentarze na GitHub - jak reviewuje, jak odpowiada na pytania

### WARSTWA 4: Kontekst organizacyjny (Mike w Callstack)

Wiedza o tym, jak Mike zarządza Callstack, jakie podejmuje decyzje biznesowo-techniczne.

**Źródła:**
- Callstack blog posts (callstack.com/blog)
- Callstack open source strategy (callstack.com/open-source)
- Super App examples, enterprise approach
- Dane syntetyczne: wewnętrzne decyzje, Slack, 1:1

---

## Mapa Źródeł Danych - Wszystko Co Zbieramy

### A. GITHUB - Kod i Dyskusje

#### A1. Pull Requesty i Issues w React Native Core

```
Repo: facebook/react-native
Username: grabbou
Co zbieramy: PR-y authored, PR-y reviewed, issues authored, issues commented
Szacowana ilość: 50-100+ PR-ów, dziesiątki issues
```

**Konkretne PR-y do znalezienia:**
- Merge rnpm into react-native (historyczny moment)
- Auto-linking implementation
- Release process automation
- Build fixes (np. PR #30543 - building in release mode for simulator)

**Komenda:**
```bash
gh search prs --author=grabbou --repo=facebook/react-native --limit=50 \
  --json number,title,url,createdAt,state
```

#### A2. React Native Community CLI

```
Repo: react-native-community/cli
Username: grabbou
Co zbieramy: PR-y, issues, design decisions
Kluczowe: PR #254 (Standardise configuration mechanism)
          PR #1537 (remove deprecated link/unlink)
```

**To repo jest kluczowe** - Mike zaprojektował architekturę CLI, auto-linking i cały system konfiguracji. Tutaj jest najwięcej jego "tribal knowledge".

**Komenda:**
```bash
gh search prs --author=grabbou --repo=react-native-community/cli --limit=50 \
  --json number,title,url,body,createdAt
```

#### A3. Callstack Re.Pack

```
Repo: callstack/repack
Username: grabbou
Co zbieramy: PR-y, issues, design discussions, release notes
Kontekst: Dlaczego webpack zamiast Metro? Jak Module Federation działa w RN?
```

**Komenda:**
```bash
gh search prs --author=grabbou --repo=callstack/repack --limit=30 \
  --json number,title,url,body,createdAt
```

#### A4. Callstack React Native Paper

```
Repo: callstack/react-native-paper
Co zbieramy: PR-y, architectural decisions, theming system design
Kontekst: Material Design w RN, komponentowy system, enterprise adoption
```

#### A5. rnpm (archiwalne, ale kluczowe dla historii)

```
Repo: rnpm/rnpm (archived)
      rnpm/rnpm-plugin-link
      rnpm/rnpm-plugin-upgrade
Co zbieramy: Cały kod + issues + PR-y - to jest "origin story" Mike'a w RN
```

#### A6. Callstack Haul (poprzednik Re.Pack)

```
Repo: callstack/haul
Username: grabbou
Co zbieramy: Commity, design decisions
Kontekst: Ewolucja myślenia: Haul -> Re.Pack -> Module Federation
```

#### A7. Callstack Incubator

```
Repo: callstackincubator/ai (on-device LLM w React Native)
      callstackincubator/rock (modular toolkit)
Co zbieramy: Nowe kierunki, w które Mike prowadzi Callstack
```

#### A8. React Native Releases

```
Repo: react-native-community/releases
Co zbieramy: Mike's involvement in release coordination
Kluczowe: Issues i PR-y dotyczące 0.59, 0.60, 0.61, 0.62
```

**Pełna lista repozytoriów do scrapowania:**
```python
REPOS = [
    "facebook/react-native",
    "react-native-community/cli",
    "callstack/repack",
    "callstack/react-native-paper",
    "callstack/haul",
    "callstack/super-app-example",
    "callstackincubator/ai",
    "callstackincubator/rock",
    "rnpm/rnpm",
    "rnpm/rnpm-plugin-link",
    "react-native-community/releases",
]
```

---

### B. KONFERENCJE I TALKS (Wideo + Transkrypcje)

#### B1. GitNation / React Summit

```
URL: gitnation.com/person/mike_grabowski
Talks:
- "Building Cross-Platform Federated Modules With React, React Native and Re.Pack"
  (React Summit 2025)
- Discussion room: "Future of Native" z Evan Bacon, Xuan Huang, Kræn Hansen
  (React Summit 2025)
Jak pobrać: yt-dlp z YouTube lub GitNation platform
```

#### B2. React Native EU

```
Mike jest współorganizatorem - ma talks z każdej edycji
URL: react-native.eu/talks/
Szukaj: "Mike Grabowski" site:youtube.com OR site:react-native.eu
Znane: React Native EU 2019 Intro, RNEU 2020 Q&A Panel, kolejne edycje
```

#### B3. Chain React Conference

```
URL: chainreactconf.com/speakers/mike-grabowski
Znane: Talk 2019 (Portland, OR)
Szukaj na YouTube: "Mike Grabowski Chain React"
```

#### B4. App.js Conf

```
Callstack organizuje tę konferencję
Szukaj: "Mike Grabowski App.js" na YouTube
```

#### B5. Inne

```
Szukaj na YouTube:
- "Mike Grabowski react native"
- "grabbou conference talk"
- "grabbou keynote"
```

**Komenda do masowego wyszukiwania:**
```bash
SEARCH_QUERIES=(
    "Mike Grabowski React Summit"
    "Mike Grabowski React Native EU"
    "Mike Grabowski Chain React"
    "Mike Grabowski App.js conf"
    "Mike Grabowski KubeCon"
    "Mike Grabowski callstack talk"
    "grabbou conference"
    "Mike Grabowski module federation react native"
    "Mike Grabowski repack"
)

for query in "${SEARCH_QUERIES[@]}"; do
    echo "=== $query ==="
    yt-dlp --flat-playlist "ytsearch5:$query" \
        --print "%(title)s | %(url)s | %(duration_string)s"
    echo ""
done
```

---

### C. PODCAST - React Native Show / React Universe On Air

```
URL: callstack.com/podcast-react-native-show
     callstack.com/podcast
Apple Podcasts: podcasts.apple.com/podcast/the-react-native-show-podcast/id1525543072
```

**Co zbieramy:** Odcinki, w których Mike jest hostem lub gościem. Szczególnie te, gdzie mówi o architekturze, decyzjach, przyszłości RN.

**Znane odcinki z Mike'em:**
- Re.Pack episode (z Paweł Trysła)
- Brownfield development (z Michał Chudziak)
- React Native FastIO
- React Native on Windows (ep. 8)
- Expert Talks on Current and Future Trends

**Jak pobrać:**
```bash
# Szukaj na YouTube
yt-dlp --flat-playlist "ytsearch20:React Native Show podcast callstack" \
    --print "%(title)s | %(url)s | %(duration_string)s"

# Albo pobierz transkrypcje z Apple Podcasts/Spotify (narzędzia third-party)
```

---

### D. PISEMNE ŹRÓDŁA

#### D1. Reactiflux Q&A Transcript (ZŁOTO)

```
URL: github.com/reactiflux/q-and-a/blob/master/mike-grabowski_react-native-core.md
Format: Markdown - gotowy do pobrania
Zawartość: Głęboka rozmowa o RN core, decyzjach, wyzwaniach, planach
```

**Komenda:**
```bash
curl -sL \
    "https://raw.githubusercontent.com/reactiflux/q-and-a/master/mike-grabowski_react-native-core.md" \
    -o raw/written/reactiflux-qa.md
```

#### D2. Medium Blog

```
URL: medium.com/@grabbou
Co zbieramy: Wszystkie artykuły techniczne
Jak: yt-dlp lub manual scraping artykułów
```

#### D3. Callstack Blog (artykuły z Mike'em)

```
URL: callstack.com/blog
Kluczowe artykuły:
- Module Federation with Re.Pack 3
- Super App architecture
- Open source strategy
Jak: curl poszczególnych artykułów
```

#### D4. grabbou.com (osobista strona)

```
URL: grabbou.com
     dev.grabbou.xyz (nowy framework RN?)
Co zbieramy: Bio, artykuły, portfolio
```

#### D5. Twitter/X (@grabbou)

```
URL: twitter.com/grabbou
Co zbieramy: Hot takes, opinie, reakcje na newsy z ekosystemu RN
Format: Najważniejsze wątki i tweety (manual selection)
Przykłady znalezione:
- "React Native 0.45.0-rc.0 is finally out, changelog coming soon!"
- "React Native 0.59.0 is out! Check out what's new..."
```

---

### E. DOKUMENTACJA TECHNICZNA

#### E1. React Native Docs (sekcje relevantne dla Mike'a)

```bash
DOCS_URLS=(
    "https://raw.githubusercontent.com/facebook/react-native-website/main/docs/native-modules-intro.md"
    "https://raw.githubusercontent.com/facebook/react-native-website/main/docs/linking-libraries-ios.md"
    "https://raw.githubusercontent.com/facebook/react-native-website/main/docs/new-architecture-intro.md"
)
```

#### E2. Re.Pack Docs

```
URL: re-pack.dev lub callstack.github.io/repack
GitHub: github.com/callstack/repack/tree/main/website/docs
```

#### E3. React Native Paper Docs

```
URL: callstack.github.io/react-native-paper/
GitHub: github.com/callstack/react-native-paper/tree/main/docs
```

#### E4. React Native CLI Docs

```
GitHub: github.com/react-native-community/cli/tree/main/docs
```

---

### F. DANE SYNTETYCZNE (Twoje zadanie)

#### F1. Wewnętrzne wiadomości Slack/Discord (15-20 wątków)

Tematy, które muszą być spójne z prawdziwymi danymi:

```json
[
    {
        "channel": "#react-native-core",
        "topic": "Dyskusja o migracji z Haul na Re.Pack - dlaczego, tradeoffs, timeline",
        "mike_role": "Tłumaczy architekturę, odpowiada na wątpliwości zespołu"
    },
    {
        "channel": "#repack-dev",
        "topic": "Module Federation nie działa z Hermes - debugging session",
        "mike_role": "Diagnozuje problem, proponuje workaround"
    },
    {
        "channel": "#cli-team",
        "topic": "Auto-linking łamie kompatybilność z starszymi bibliotekami",
        "mike_role": "Wyjaśnia design decision, proponuje deprecation path"
    },
    {
        "channel": "#general",
        "topic": "Nowy dev pyta dlaczego nie używamy Metro wszędzie",
        "mike_role": "Wyjaśnia historię: Metro limitations -> Haul -> Re.Pack"
    },
    {
        "channel": "#react-native-releases",
        "topic": "Release 0.73 - co blokuje, jakie breaking changes",
        "mike_role": "Koordynuje, wyjaśnia zależności, podejmuje decyzje go/no-go"
    },
    {
        "channel": "#enterprise-clients",
        "topic": "Klient pyta o Super App architecture z Module Federation",
        "mike_role": "CTO perspective - architektura, risks, recommendations"
    },
    {
        "channel": "#hiring",
        "topic": "Szukamy senior RN developera do core tooling",
        "mike_role": "Definiuje wymagania, pyta o doświadczenie z bundlerami"
    },
    {
        "channel": "#paper-design",
        "topic": "Material You migration strategy dla React Native Paper",
        "mike_role": "High-level direction, deleguje detale"
    }
]
```

#### F2. Tickety Jira/Linear (8-10 sztuk)

```json
[
    {
        "key": "RPACK-401",
        "type": "Epic",
        "summary": "Module Federation v2 - Cross-platform support (Web + RN)",
        "assignee": "mike",
        "status": "In Progress",
        "context": "Bazuj na prawdziwym talk z React Summit 2025"
    },
    {
        "key": "CLI-892",
        "type": "Bug",
        "summary": "Auto-linking breaks with React Native New Architecture on iOS",
        "assignee": "mike",
        "status": "Done",
        "context": "Bazuj na prawdziwych issues z react-native-community/cli"
    },
    {
        "key": "CORE-155",
        "type": "Technical Decision",
        "summary": "Evaluate Metro vs Re.Pack for enterprise monorepo clients",
        "assignee": "mike",
        "status": "Done",
        "context": "Decyzja architektoniczna - dlaczego oba narzędzia mają sens"
    },
    {
        "key": "RPACK-445",
        "type": "Story",
        "summary": "Hermes compatibility layer for webpack chunks",
        "assignee": "mike",
        "status": "In Review",
        "context": "Techniczne wyzwanie z Hermes engine + dynamic imports"
    },
    {
        "key": "CS-2401",
        "type": "Initiative",
        "summary": "On-device LLM integration in React Native (callstackincubator/ai)",
        "assignee": "mike",
        "status": "In Progress",
        "context": "Nowy kierunek - AI w mobile apps"
    }
]
```

#### F3. Notatki 1:1 z boardem/CTO coach (4 spotkania)

Tematy:
1. Strategia open source Callstack - jak balansować między OS a revenue
2. Re.Pack adoption challenges - enterprise vs community
3. React Native New Architecture - jak się pozycjonować
4. Team scaling - kogo zatrudniać do core tooling

#### F4. Internal tech talks / Architecture Decision Records

Tematy:
1. ADR: "Why we chose webpack over Metro for Re.Pack"
2. ADR: "Module Federation as the foundation for Super Apps"
3. ADR: "rnpm deprecation and migration to auto-linking"
4. Internal talk: "The future of React Native tooling" (slides + notes)

---

## Pipeline Implementacji

### Faza 1: Automated Data Collection (Dev - 2-3h)

```bash
# 1. Setup
export TARGET_USERNAME="grabbou"
mkdir -p teamtwin/{raw/{github,talks,written,docs,podcast,synthetic},processed,agents}

# 2. GitHub scraping (największy chunk)
# Użyj skryptu fetch_github_prs.py z implementation-guide.md
# ale zmień REPOS na listę z sekcji A

# 3. Reactiflux Q&A (instant)
curl -sL "https://raw.githubusercontent.com/reactiflux/q-and-a/master/mike-grabowski_react-native-core.md" \
    -o raw/written/reactiflux-qa.md

# 4. YouTube talks (transkrypcje)
# Użyj skryptu z implementation-guide.md z search queries z sekcji B

# 5. Dokumentacja
# curl docs z sekcji E
```

### Faza 2: Manual/Semi-automated Collection (Dev + Ty - 1-2h)

```
- Medium artykuły (manual export lub web scraping)
- Callstack blog posts (curl)
- Podcast episodes identification (which ones feature Mike)
- Twitter/X best tweets selection (manual)
```

### Faza 3: Synthetic Data Creation (Ty - 2-3h)

```
- Slack threads (15-20) bazujące na sekcji F1
- Jira tickets (8-10) bazujące na sekcji F2
- 1:1 notes (4 spotkania) bazujące na sekcji F3
- ADRs (3-4) bazujące na sekcji F4
```

### Faza 4: Profile Building & Assembly (Dev - 1-2h)

```
- Compile all data into raw-profile-input.md
- Send to Gemini for competency profile generation
- Build system prompts for 3 agents
- Configure VAPI
```

---

## Demo Narrative z Mike'em

### Pitch na scenie

"Mike Grabowski, CTO Callstack i jeden z architektów ekosystemu React Native, odchodzi z firmy. Zabiera ze sobą wiedzę, która powstawała przez lata: dlaczego Re.Pack istnieje, jak działa auto-linking pod spodem, jakie trade-offy stały za każdą decyzją architektoniczną. Ale my mamy TeamTwin."

### Akt 1: Rozmowa z klonem Mike'a

"Hej Mike, nowy CTO pyta dlaczego używamy Re.Pack zamiast Metro dla enterprise klientów?"

Agent odpowiada z kontekstem: historia Haul -> Re.Pack, limitations Metro (brak tree shaking, brak Module Federation), cytuje swój talk z React Summit, odwołuje się do ADR-a.

"A pokaż mi ten diagram z prezentacji o Module Federation."

Na ekranie pojawia się slajd z talks.

### Akt 2: Rekrutacja następcy

"Mike odchodzi za miesiąc. Przygotuj materiały na jego zastępstwo."

Agent generuje job description, które brzmi inaczej niż generic "Senior React Native Developer needed":
- "Must understand webpack internals and bundler architecture for mobile"
- "Experience with Module Federation or micro-frontend patterns"
- "Ability to navigate Facebook/Meta's React Native release process"
- "Track record in open source maintenance at scale (10k+ stars repos)"

### Akt 3: Rozmowa rekrutacyjna

Agent pyta kandydata: "Metro bundler ma ograniczenie X. Jak byś podszedł do rozwiązania tego dla klienta enterprise z monorepo? Mike rozwiązał to przez webpack i Re.Pack - ale chcemy usłyszeć Twoje podejście."

---

## Checklist Gotowości

### Dane minimalne do działającego demo:
- [ ] 20+ PR-ów z GitHub (facebook/react-native + react-native-community/cli)
- [ ] 10+ code reviews z komentarzami Mike'a
- [ ] Reactiflux Q&A transcript
- [ ] 2-3 transkrypcje talks (React Summit, Chain React)
- [ ] Re.Pack docs i README
- [ ] 1-2 artykuły z Medium/Callstack Blog
- [ ] 8+ syntetycznych ticketów Jira
- [ ] 10+ syntetycznych wątków Slack
- [ ] 4 syntetyczne notatki 1:1
- [ ] 3+ ADR-y syntetyczne
- [ ] Profil kompetencyjny wygenerowany przez Gemini

### Nice to have:
- [ ] Podcast episodes z transkrypcjami
- [ ] Twitter thread export
- [ ] Callstack Super App example code analysis
- [ ] callstackincubator/ai repo analysis (newest direction)
