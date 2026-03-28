# TeamTwin - Plan Zbierania Danych z Kubernetes

## Cel dokumentu

Szczegółowy plan pozyskania danych do zbudowania "cyfrowego klona" kontrybutora Kubernetes. Dokument opisuje konkretne źródła, formaty, narzędzia do ekstrakcji i sposób przygotowania danych dla Gemini + VAPI.

---

## Wybór SIG-u i Kontrybutora

### Rekomendowany SIG: SIG-Network

**Dlaczego SIG-Network:**
- Architektura sieciowa Kubernetes to temat, który każdy juror rozumie, ale jest wystarczająco skomplikowany, żeby "klon" mógł błysnąć wiedzą
- Bogata dokumentacja: Gateway API, Network Policies, Service Mesh - dużo KEPs i design decisions
- Regularne nagrane spotkania (co tydzień)
- Aktywni, rozpoznawalni kontrybutorzy z KubeCon talks

### Jak wybrać konkretnego kontrybutora

1. Wejdź na https://github.com/kubernetes/community/tree/master/sig-network
2. Otwórz README.md - znajdziesz listę chairs, tech leads i subproject owners
3. Wybierz osobę, która spełnia kryteria:
   - Jest aktywna na GitHub (dużo PR-ów, code reviews, issues)
   - Ma KubeCon talks na YouTube (szukaj ich imienia + "KubeCon")
   - Jest aktywna w dyskusjach na KEPs
   - Pojawia się na nagraniach SIG meetings
4. Nie używaj prawdziwego imienia w demo - stwórz fikcyjną persona "Tomka" bazowaną na prawdziwych danych aktywności

**Backup SIG-i** (gdyby SIG-Network miał za mało danych):
- SIG-Node - zarządza kubeletem, runtime, scheduling na poziomie node'a
- SIG-Auth - autentykacja, autoryzacja, security policies
- SIG-Storage - persistent volumes, CSI drivers

---

## Źródła Danych - Mapa Kompletna

### 1. NAGRANIA SPOTKAŃ SIG (Audio/Wideo - Multimodal)

**Co to daje:** Transkrypcje spotkań, w których kontrybutor omawia decyzje techniczne, problemy, propozycje zmian. To jest najbliższe "prawdziwym standup'om i planningom" w firmie.

**Gdzie znaleźć:**
- YouTube: kanał `@kubernetes` - każdy SIG ma dedykowaną playlistę
  - Szukaj: "Kubernetes SIG Network" na YouTube
  - Playlisty: https://www.youtube.com/playlist?list=PL69nYSiGNLP2E8E-RWVaNGP5j5cARFPZE (SIG-Network przykład)
- CNCF YouTube: https://www.youtube.com/@caborundum - KubeCon talks i panele
- Community meetings: https://github.com/kubernetes/community/blob/master/events/community-meeting.md

**Jak wyciągnąć dane:**
- YouTube ma automatyczne transkrypcje (CC) - wyeksportuj je
- Gemini 3.1 może przetworzyć wideo bezpośrednio (multimodal!) - podajesz URL lub plik wideo i prosisz o transkrypcję z identyfikacją mówców
- Narzędzia: `yt-dlp` do pobrania wideo/audio, Whisper do transkrypcji jeśli CC nie wystarczą

**Ile potrzebujesz:** 5-10 nagrań spotkań (po 30-60 min każde) to wystarczy, żeby agent miał bogaty kontekst

**Format wyjściowy:**
```
[SIG-Network Meeting 2025-11-14]
[Timestamp: 12:34]
[Speaker: wybrany-kontrybutor]
"We discussed the Gateway API v1.2 changes. The main concern
is backward compatibility with existing HTTPRoute configs.
I proposed we add a conversion webhook, similar to what we
did for IngressClass migration..."
```

---

### 2. KEPs - KUBERNETES ENHANCEMENT PROPOSALS (Dokumenty techniczne)

**Co to daje:** Głębokie dokumenty opisujące "dlaczego" za decyzjami architektonicznymi. To jest odpowiednik wewnętrznych RFC/ADR w firmie. Każdy KEP ma motivation, proposal, alternatives considered, risks.

**Gdzie znaleźć:**
- Repozytorium: https://github.com/kubernetes/enhancements/tree/master/keps
- KEPs SIG-Network: https://github.com/kubernetes/enhancements/tree/master/keps/sig-network
- Przeglądarka KEPs: https://www.kubernetes.dev/resources/keps/

**Konkretne KEPs do zebrania (SIG-Network):**
- Gateway API KEPs (seria dokumentów o ewolucji API)
- Network Policy KEPs (jak projektowano polityki sieciowe)
- Service Internal Traffic Policy
- EndpointSlice API
- Multi-Network support

**Jak wyciągnąć dane:**
- Git clone repo: `git clone https://github.com/kubernetes/enhancements.git`
- Przejrzyj `keps/sig-network/` - każdy folder to osobny KEP z `README.md`
- Wyciągnij KEPs, gdzie wybrany kontrybutor jest autorem lub reviewerem (sprawdź pole `authors:` i `reviewers:` w metadanych KEP)

**Format wyjściowy:**
```
[KEP-3570: Gateway API - HTTPRoute Timeout]
[Author: wybrany-kontrybutor]
[Status: Implementable]
Motivation: "Timeouts are a critical part of service reliability..."
Design: "We add a new `timeouts` field to HTTPRouteRule..."
Alternatives rejected: "We considered using annotations, but..."
```

---

### 3. GITHUB - PR-y, ISSUES, CODE REVIEWS (Kod + Dyskusje)

**Co to daje:** Realne interakcje - jak kontrybutor tłumaczy swój kod, jak reviewuje innych, jakie problemy raportuje. To jest odpowiednik codziennej pracy w Jira + code reviews.

**Gdzie znaleźć:**
- Główne repo: https://github.com/kubernetes/kubernetes
- Sieciowe subrepo: https://github.com/kubernetes-sigs/gateway-api
- Network Policy: https://github.com/kubernetes-sigs/network-policy-api

**Co zbierać:**
- **PR-y kontrybutora** - opisy, dyskusje w review, odpowiedzi na komentarze
  - GitHub search: `author:USERNAME repo:kubernetes/kubernetes`
- **Code reviews** - komentarze kontrybutora na cudzych PR-ach
  - GitHub search: `commenter:USERNAME repo:kubernetes/kubernetes`
- **Issues** - problemy zgłoszone lub skomentowane
  - GitHub search: `involves:USERNAME repo:kubernetes/kubernetes label:sig/network`
- **Commity** - wiadomości commitów, zmiany w kodzie

**Jak wyciągnąć dane:**
- GitHub API: `gh api search/issues?q=author:USERNAME+repo:kubernetes/kubernetes`
- Albo użyj GitHub GraphQL API do bulk eksportu
- Skrypt Python z `PyGithub` library do pobrania PR-ów z komentarzami

**Ile potrzebujesz:** 20-30 PR-ów/issues z komentarzami da solidny obraz stylu pracy

**Format wyjściowy:**
```
[PR #12345: Add timeout support to HTTPRoute]
[Author: wybrany-kontrybutor]
Description: "This PR implements KEP-3570..."
Review comment from @reviewer: "Why not use context deadline?"
Response: "Context deadline doesn't propagate across proxy
          boundaries. We need explicit header-level timeout
          because the gateway sits between client and backend..."
```

---

### 4. SLACK / DISCORD (Nieformalne rozmowy)

**Co to daje:** Nieformalny kontekst - jak kontrybutor pomaga innym, odpowiada na pytania, dzieli się wiedzą "z głowy". To jest odpowiednik kanałów Slack w firmie.

**Gdzie znaleźć:**
- Kubernetes Slack: https://slack.k8s.io/ (dołącz za darmo)
  - Kanał `#sig-network` - główne dyskusje SIG
  - Kanał `#sig-network-gateway-api` - Gateway API
  - Kanał `#networking` - ogólne pytania o networking
- Kubernetes forum: https://discuss.kubernetes.io/

**Jak wyciągnąć dane:**
- Dołącz do Slack workspace, wejdź na kanały, wyszukaj wiadomości po username kontrybutora
- Slack API (jeśli masz workspace token): `conversations.history` + `search.messages`
- Forum Discuss: scraping lub API Discourse

**Uwaga:** Jeśli nie uda się wyciągnąć wystarczająco dużo danych ze Slacka, to właśnie tu wchodzą dane syntetyczne. Napisz 15-20 realistycznych wątków Slack bazowanych na prawdziwych tematach z issues/KEPs, np:
```
#sig-network
@junior-dev: Hey, I'm seeing weird behavior with NetworkPolicy
             after upgrading to 1.30. Egress rules seem to be
             ignored on some pods.
@tomek: That's likely the known issue with endpoint slice
        controller not reconciling after upgrade. Check if your
        endpointslices have the correct labels. We fixed this
        in #98765 but the fix didn't make it into 1.30.2.
        Workaround: restart kube-proxy on affected nodes.
@junior-dev: That worked! Thanks. Should I file a backport request?
@tomek: Already done - see #99012. Should be in 1.30.3.
```

---

### 5. KUBECON TALKS (Prezentacje - Multimodal: wideo + slajdy)

**Co to daje:** Prezentacje, w których kontrybutor tłumaczy swoją pracę publiczności. Zawierają diagramy, architekturę, demo - idealny content multimodalny dla Gemini.

**Gdzie znaleźć:**
- CNCF YouTube: https://www.youtube.com/@cncf - pełne playlisty z każdego KubeCon
- Szukaj: `"[imię kontrybutora] KubeCon"` na YouTube
- Schedule archive: https://kccncna2024.sched.com/ (i analogiczne dla innych lat)
- Slajdy: często linkowane w opisie YouTube lub na sched.com

**Konkretne playlisty:**
- KubeCon NA 2024: pełna playlista na CNCF YouTube
- KubeCon EU 2025 (London): pełna playlista na CNCF YouTube
- KubeCon NA 2025: pełna playlista na CNCF YouTube

**Jak wyciągnąć dane:**
- `yt-dlp` do pobrania wideo + transkrypcji
- Gemini może bezpośrednio przetworzyć wideo i wyciągnąć informacje z slajdów (multimodal!)
- Jeśli slajdy są na Speaker Deck/SlideShare - pobierz jako PDF

**Ile potrzebujesz:** 2-3 talki po 20-40 min to złoto

---

### 6. DOKUMENTACJA TECHNICZNA (Tekst + Diagramy)

**Co to daje:** Oficjalna dokumentacja, do której kontrybutor przyczyniał się. Pozwala agentowi odpowiadać "z dokumentacji" i łączyć z kontekstem decyzji.

**Gdzie znaleźć:**
- Kubernetes docs: https://kubernetes.io/docs/concepts/services-networking/
- Design docs: https://github.com/kubernetes/community/tree/master/sig-network
- Architecture diagrams: w KEPs i design docs (jako obrazki - multimodal!)
- API reference: https://kubernetes.io/docs/reference/kubernetes-api/

**Co zbierać:**
- Sekcje docs dotyczące networking (Services, Ingress, Gateway API, NetworkPolicy)
- Design proposals z folderu SIG
- Diagramy architektury (PNG/SVG z docs i KEPs)

---

### 7. DANE SYNTETYCZNE (Uzupełnienie luk)

**Co trzeba stworzyć ręcznie**, bo nie istnieje publicznie:

**Tickety Jira (5-10 sztuk):**
```
[KNET-1234] Fix EndpointSlice reconciliation after cluster upgrade
Status: Done | Priority: Critical | Sprint: v1.30.3
Reporter: @pm-lead
Assignee: @tomek
Description: After upgrading from 1.29 to 1.30, EndpointSlice
controller fails to reconcile endpoints for services with
more than 100 backends...
Comments:
  @tomek: Root cause identified. The pagination logic in
          endpointslice_controller.go doesn't handle the case
          where label selector changes between versions...
  @tomek: Fix in PR #98765. Added migration test in e2e suite.
```

**Notatki 1:1 z tech leadem (3-4 spotkania):**
```
[1:1 Notes - 2025-10-20]
Tomek mentioned he's concerned about the Gateway API adoption
timeline. Thinks we need better migration tooling from Ingress.
Action: Tomek to draft KEP for automated Ingress-to-Gateway
migration tool by next sprint.
Personal note: Tomek prefers async communication, best reached
on Slack before 2pm CET. Responds slowly to email.
```

**Wiadomości Slack (15-20 wątków):**
- Odpowiedzi na pytania juniorów
- Dyskusje o design decisions
- Debugging w real-time
- Code review follow-upy
- Nieformalne opinie ("honestly I think we should deprecate this API")

---

## Organizacja Danych - Struktura Folderów

```
/data/
├── raw/                          # Surowe dane
│   ├── meetings/                 # Transkrypcje spotkań SIG
│   │   ├── sig-network-2025-11-14.txt
│   │   ├── sig-network-2025-11-21.txt
│   │   └── ...
│   ├── keps/                     # KEPs napisane/reviewowane
│   │   ├── kep-3570-httproute-timeout.md
│   │   ├── kep-2091-gateway-api-v1.md
│   │   └── ...
│   ├── github/                   # PR-y, issues, reviews
│   │   ├── prs-authored.json
│   │   ├── prs-reviewed.json
│   │   ├── issues-commented.json
│   │   └── commits.json
│   ├── talks/                    # KubeCon prezentacje
│   │   ├── kubecon-eu-2025-gateway-api.txt    # transkrypcja
│   │   ├── kubecon-eu-2025-gateway-api.pdf    # slajdy
│   │   └── ...
│   ├── slack/                    # Wiadomości (real + syntetyczne)
│   │   ├── sig-network-threads.json
│   │   ├── networking-helpdesk.json
│   │   └── ...
│   ├── docs/                     # Dokumentacja techniczna
│   │   ├── networking-concepts.md
│   │   ├── gateway-api-spec.md
│   │   └── architecture-diagrams/
│   │       ├── network-flow.png
│   │       └── gateway-api-architecture.svg
│   └── synthetic/                # Dane syntetyczne
│       ├── jira-tickets.json
│       ├── 1on1-notes.md
│       └── slack-informal.json
│
├── processed/                    # Przetworzone i ustrukturyzowane
│   ├── competency-profile.md     # Profil kompetencyjny "Tomka"
│   ├── personality-brief.md      # Styl komunikacji, preferencje
│   ├── knowledge-graph.json      # Powiązania: temat > źródło > cytat
│   └── timeline.json             # Chronologia aktywności
│
└── agents/                       # Konfiguracje agentów
    ├── knowledge-clone/
    │   ├── system-prompt.md
    │   └── vapi-config.json
    ├── recruitment-generator/
    │   ├── system-prompt.md
    │   ├── job-desc-template.md
    │   ├── task-template.md
    │   └── scoring-rubric-template.md
    └── interviewer/
        ├── system-prompt.md
        ├── question-bank.json
        └── vapi-config.json
```

---

## Pipeline Przygotowania Danych

### Krok 1: Zbieranie danych surowych (2-3h)

| Zadanie | Narzędzie | Kto |
|---------|-----------|-----|
| Pobranie 5-10 nagrań SIG meetings | `yt-dlp` | Dev |
| Transkrypcja nagrań | YouTube CC lub Whisper | Dev |
| Clone repo `kubernetes/enhancements` | `git clone` | Dev |
| Export PR-ów i issues z GitHub API | Skrypt Python / `gh` CLI | Dev |
| Dołączenie do K8s Slack, export wątków | Ręcznie / Slack API | Ty |
| Pobranie 2-3 KubeCon talks + slajdów | `yt-dlp` + manual | Ty |
| Zebranie docs z kubernetes.io | `wget` / copy | Ty |

### Krok 2: Tworzenie danych syntetycznych (1-2h, to jest Twoje zadanie)

| Zadanie | Format | Ilość |
|---------|--------|-------|
| Tickety Jira | JSON | 8-10 ticketów |
| Notatki 1:1 | Markdown | 4 spotkania |
| Wątki Slack (nieformalne) | JSON | 15-20 wątków |
| Daily standups (krótkie notatki) | Markdown | 10 standup'ów |

**Ważne:** Dane syntetyczne muszą być spójne z danymi prawdziwymi. Jeśli w prawdziwym KEP kontrybutor pisze o Gateway API timeout, to w syntetycznym tickecie Jira powinien być task na implementację tego feature'a, a w Slacku powinien pomagać komuś z problemem z timeoutami.

### Krok 3: Budowanie profilu kompetencyjnego (1h)

Na bazie zebranych danych stwórz `competency-profile.md`:

```markdown
# Profil Kompetencyjny - "Tomek"

## Rola
Senior Software Engineer / SIG-Network Tech Lead

## Core Competencies
- Gateway API design & implementation (expert)
- Network Policy architecture (expert)
- EndpointSlice controller (deep knowledge)
- Kubernetes API conventions (strong)
- Go programming (daily use, 4+ years)
- Performance optimization at scale (experienced)

## Knowledge Map
- Wie DLACZEGO Gateway API zastąpiło Ingress (był przy decyzji)
- Zna historię 3 nieudanych prób implementacji multi-network
- Potrafi wyjaśnić każdy workaround w endpointslice controllerce
- Rozumie trade-offy między L4 i L7 load balancing w K8s

## Communication Style
- Bezpośredni, techniczny, lubi analogie do systemów rozproszonych
- Preferuje async (Slack > spotkania)
- Cierpliwy z juniorami, ale irytuje go brak przygotowania
- Często cytuje KEPs w dyskusjach ("as described in KEP-3570...")

## Decision Patterns
- Data-driven: zawsze prosi o benchmarki przed podjęciem decyzji
- Backward compatibility first: nie łamie istniejących API
- Preferuje prostsze rozwiązania ("we don't need another abstraction")
```

### Krok 4: Konfiguracja agentów (Dev, 1-2h)

Na bazie profilu i danych, stwórz system prompty i konfiguracje VAPI. Dane ładujemy do Gemini context window (2M tokenów to dużo - zmieści się profil + 50-100 stron transkryptów/docs).

---

## Checklisty Gotowości

### Dane gotowe do demo - minimum viable:
- [ ] 3+ transkrypcje spotkań SIG z wypowiedziami kontrybutora
- [ ] 2+ KEPs napisane przez kontrybutora (pełne README.md)
- [ ] 10+ PR-ów z komentarzami i review discussions
- [ ] 1 KubeCon talk (transkrypcja + slajdy)
- [ ] 8+ syntetycznych ticketów Jira
- [ ] 10+ wątków Slack (mix real + syntetyczne)
- [ ] Profil kompetencyjny gotowy
- [ ] System prompty dla 3 agentów gotowe

### Nice to have:
- [ ] Diagramy architektury (PNG) - agent może je pokazać w rozmowie
- [ ] Więcej KubeCon talks (głębszy kontekst)
- [ ] Forum Discuss - posty kontrybutora
- [ ] Git blame analysis - jakie części kodu kontrybutor pisał

---

## Szacowany Czas

| Faza | Czas | Kto |
|------|------|-----|
| Zbieranie danych surowych | 2-3h | Dev + Ty |
| Tworzenie danych syntetycznych | 1.5-2h | Ty |
| Budowanie profilu kompetencyjnego | 1h | Ty |
| Przetwarzanie i strukturyzowanie | 1h | Dev |
| Konfiguracja agentów | 1-2h | Dev |
| **Razem** | **6-9h** | |

---

## Źródła - Quick Links

### GitHub
- SIG-Network: https://github.com/kubernetes/community/tree/master/sig-network
- SIG-Node: https://github.com/kubernetes/community/tree/master/sig-node
- KEPs repo: https://github.com/kubernetes/enhancements/tree/master/keps
- KEPs SIG-Network: https://github.com/kubernetes/enhancements/tree/master/keps/sig-network
- Główne repo K8s: https://github.com/kubernetes/kubernetes
- Gateway API: https://github.com/kubernetes-sigs/gateway-api
- Lista SIGów: https://github.com/kubernetes/community/blob/main/sig-list.md
- Community meeting notes: https://github.com/kubernetes/community/blob/master/events/community-meeting.md

### YouTube
- Kubernetes channel: https://www.youtube.com/@kubernetes
- CNCF channel (KubeCon talks): https://www.youtube.com/@cncf

### Slack & Forum
- K8s Slack invite: https://slack.k8s.io/
- Discuss forum: https://discuss.kubernetes.io/
- Google Groups (dev): https://groups.google.com/g/kubernetes-dev

### Dokumentacja
- Networking concepts: https://kubernetes.io/docs/concepts/services-networking/
- API reference: https://kubernetes.io/docs/reference/kubernetes-api/
- KEP browser: https://www.kubernetes.dev/resources/keps/
- Community groups: https://www.kubernetes.dev/community/community-groups/
