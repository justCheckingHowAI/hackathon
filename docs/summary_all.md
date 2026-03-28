# Plany hackathonowe — podsumowanie i porównanie

## Przegląd

Ten dokument podsumowuje i porównuje pięć dokumentów planistycznych hackathonu oraz jedną transkrypcję spotkania zespołu. Wszystkie plany zbiegają się na jednym głównym pomyśle — **multimodalny agent głosowy, który zachowuje wiedzę odchodzących pracowników i przyspiesza rekrutację na ich miejsce** — ale różnią się zakresem, architekturą, strategią danych i podejściem do demo.

**Po spotkaniu 1 (2026-03-28) większość otwartych decyzji została rozwiązana.** Zobacz sekcję „Decyzje ze spotkania 1" poniżej.

### Analizowane dokumenty

| Plik | Autor | Fokus |
|------|-------|-------|
| `maks-demo-plan.md` | Maks | Ramowanie produktowe, kontrola zakresu, struktura demo |
| `adam-hackathon-plan.md` | Adam | TeamTwin — 3 agenty głosowe, architektura techniczna |
| `przemek-hackathon-plan.md` | Przemek | OrgBrain — badanie rynku, analiza konkurencji, architektura full-stack |
| `mike-grabowski-cloning-plan.md` | (plan danych) | Strategia klonowania prawdziwej osoby — Mike Grabowski (CTO Callstack) |
| `kubernetes-data-sourcing-plan.md` | (plan danych) | Pipeline pozyskiwania danych dla kontrybutora Kubernetes SIG-Network |
| `narada1_transkrypcja.txt` | Wszyscy | Transkrypcja spotkania zespołu — kluczowe decyzje i podział zadań |
| `summary_narada1.md` | (podsumowanie) | Szczegółowe podsumowanie spotkania z decyzjami, podziałem zadań i następnymi krokami |

### Skład zespołu

| Osoba | Rola | Fokus na hackathonie |
|-------|------|---------------------|
| **Max** | Developer (core) | Google API, Vapi, Agent SDK, backend |
| **Janusz** | Developer (core) | Google API, Vapi, Agent SDK, backend |
| **Adam** | Produkt / VC / vibecoder | Zbieranie i organizacja danych |
| **Przemek** | Produkt / VC / vibecoder | Historia demo, prezentacja, UI, nazwa produktu |
| **Mieszko** | Kreatywny / artystyczny | Narracja demo, projekt UI, wizualizacje prezentacji |

---

## Wspólny grunt (wszystkie lub większość planów się zgadza)

### 1. Główny problem

Wszystkie plany adresują ten sam problem biznesowy: **krytyczna utrata wiedzy, gdy kluczowi pracownicy odchodzą**. To uniwersalny wyzwalacz, emocjonalny hak i punkt wejścia do demo.

Kluczowe ujęcia w poszczególnych planach:
- Maks: „Gdy kluczowy pracownik odchodzi, nasz multimodalny agent zamienia chaotyczną wiedzę organizacyjną w plan rekrutacyjny w kilka minut."
- Adam: „A gdybyś mógł zadzwonić do kolegi, który odszedł z firmy pół roku temu i zapytać go o cokolwiek?"
- Przemek: „Organizacje tracą ponad 30 000$ na odchodzącym pracowniku w kosztach transferu wiedzy."

### 2. Stack technologiczny

Jednomyślna zgoda na dwie kluczowe technologie:

- **Google Gemini** — multimodalny silnik wnioskowania, analiza dokumentów/tekstu/kodu, generowanie strukturalnych wyników
- **Vapi** — platforma orkiestracji agentów głosowych, telefonia, interakcja głosowa z niskim opóźnieniem

Obie są technologiami sponsorów hackathonu, co wzmacnia ocenę zgodności z tematem.

### 3. Trójfazowy przepływ produktu

Każdy plan (Maks, Adam, Przemek) opisuje wariant tego samego pipeline'u end-to-end:

| Faza | Maks | Adam (TeamTwin) | Przemek (OrgBrain) |
|------|------|-----------------|-------------------|
| **1. Analiza wiedzy** | Analiza artefaktów zespołu, identyfikacja luki kompetencyjnej | Agent Knowledge Clone — rozmowa z „cyfrowym bliźniakiem" | Heatmapa umiejętności + symulacja wpływu odejścia |
| **2. Generowanie pakietu rekrutacyjnego** | Podsumowanie luki, JD, scorecard, pytania rekrutacyjne | Agent Recruitment Generator — ultra-specyficzny JD, zadanie, rubryk | Rekomendacja roli, plan transferu, materiały rekrutacyjne |
| **3. Screening kandydatów** | Screening głosowy przez Vapi, score dopasowania | Agent AI Interviewer — adaptacyjna rozmowa techniczna | Zapytanie głosowe + dashboard scoringowy w czasie rzeczywistym |

### 4. Wymóg multimodalnego wejścia

Wszystkie plany zgadzają się: demo musi pokazać co najmniej **3 modalności wejścia**, aby obronić zgodność z tematem „multimodalny agent":
- Tekst (wiadomości Slack, transkrypcje, dokumenty)
- Dokumenty/PDF (CV, diagramy architektoniczne, KEP-y)
- Głos (rozmowa na żywo z agentem)

### 5. Output oparty na dowodach

Silny konsensus, że wyniki agenta muszą zawierać **konkretne dowody** (cytowania źródeł, fragmenty, oceny pewności), a nie tylko wygenerowany tekst. To odpowiada na sceptycyzm jury wobec halucynacji i buduje zaufanie.

- Maks: „3 konkretne fragmenty-dowody są lepsze niż 2 strony wygenerowanego opisu roli"
- Adam: Agent cytuje konkretne spotkania („pamiętasz, jak powiedziałem na standupie 12 marca...")
- Przemek: „Na podstawie 47 wiadomości Slack i 3 dokumentów projektowych, Sarah Chen ma głęboką ekspertyzę"

### 6. Strategia mock / danych syntetycznych

Wszystkie plany zakładają **wstępnie przygotowane dane mockowe** zamiast budowania pipeline'u ingestion w czasie rzeczywistym podczas hackathonu. Plany danych (Mike, K8s) dostarczają szczegółowe strategie pozyskiwania realistycznej zawartości.

### 7. Siatka bezpieczeństwa demo

Adam i Przemek jawnie rekomendują: **nagraj zapasowe wideo demo** przed prezentacją na żywo. Maks pośrednio wspiera to przez minimalizację zakresu.

---

## Punkty rozbieżności

### 1. Filozofia zakresu

| Plan | Podejście | Profil ryzyka |
|------|-----------|---------------|
| **Maks** | Brutalnie minimalistyczny — 3 ekrany, 3 źródła danych, jeden liniowy przepływ. Wyraźnie ostrzega przed „budowaniem wielu produktów naraz" | Niskie ryzyko, potencjalnie niższy efekt wow |
| **Adam (TeamTwin)** | 3 pełne agenty głosowe, każdy z odrębną osobowością i funkcją. Ambitniejszy, ale wciąż skupiony | Średnie ryzyko, silny wow jeśli wszystkie agenty działają |
| **Przemek (OrgBrain)** | Najszerszy zakres — dodaje Neo4j knowledge graph, D3.js heatmapę, WebSocket sync, FastAPI backend, React frontend | Najwyższe ryzyko, najwyższy potencjalny impact |

**Kluczowe napięcie:** Maks jawnie identyfikuje szeroki zakres jako ryzyko #1, podczas gdy Przemek proponuje najwięcej komponentów. Adam jest pośrodku.

### 2. Architektura techniczna

| Komponent | Maks | Adam | Przemek |
|-----------|------|------|---------|
| **Backbone AI** | Gemini (brak szczegółów) | Gemini 3.1 z oknem kontekstu 2M (RAG niepotrzebny) | Gemini 2.5 Flash (głos) + Gemini 3 Pro (analiza) |
| **Przechowywanie wiedzy** | Nie określono | Bezpośrednie ładowanie kontekstu do Gemini | Neo4j AuraDB graph database |
| **Backend** | Nie określono | Nie określono | FastAPI z endpointami API |
| **Frontend** | 3 proste ekrany | Opcjonalny dashboard | React + wizualizacje D3.js + WebSocket |
| **Głos** | Vapi (podstawowy) | Vapi z 3 skonfigurowanymi agentami (Squads) | Vapi ze zsynchronizowanym głosem + aktualizacjami dashboardu |
| **Embedding** | Nie omówiono | Nie omówiono | Gemini Embedding 2 (multimodalne embeddingi) |

**Kluczowa rozbieżność:** Adam stawia na ogromne okno kontekstu Gemini, by uniknąć złożoności RAG. Przemek buduje pełną graph database. Maks celowo unika decyzji architektonicznych, skupiając się na produkcie.

### 3. Persona klona / źródło danych

| Plan | Kto jest klonowany | Typ danych |
|------|-------------------|------------|
| **Maks** | „Ania" — fikcyjna senior backend engineer | Generyczne dane mockowe |
| **Adam** | „Tomek" — fikcyjny developer | Realistyczne dane mockowe |
| **Plan Mike** | **Mike Grabowski** — prawdziwa osoba, CTO Callstack, React Native core team | Prawdziwe publiczne dane (GitHub PR-y, konferencje, podcasty, posty blogowe) |
| **Plan K8s** | Anonimowy kontrybutor Kubernetes SIG-Network | Prawdziwe dane społeczności open-source (KEP-y, spotkania SIG, GitHub, KubeCon talks) |

**Kluczowa rozbieżność:** Plany Mike/K8s używają **prawdziwych, publicznie dostępnych danych** od rozpoznawalnych osób, co czyni demo znacznie bardziej imponującym, ale rodzi kwestie prywatności. Pozostałe plany używają fikcyjnych person z danymi syntetycznymi.

### 4. Format demo

| Plan | Czas trwania | Konfiguracja fizyczna | Kluczowy moment |
|------|-------------|----------------------|-----------------|
| **Maks** | 3 min (czas co do sekundy: 0:00-0:40 ingest, 0:40-1:30 luka, 1:30-2:20 screening, 2:20-3:00 wynik) | Nie określono | Score dopasowania + rekomendacja na koniec |
| **Adam** | 5 min (3 akty) | **Dwa fizyczne telefony na stole** + ekran z dashboardem | Agent cytuje konkretny standup z pamięci |
| **Przemek** | 3 min | Ekran z dashboardem | Przycisk **„Symuluj odejście"** uruchamia natychmiastową analizę wpływu, podczas gdy głos odpowiada jednocześnie |

### 5. Nazwa produktu i pitch

| Plan | Nazwa produktu | Styl pitcha |
|------|---------------|-------------|
| **Maks** | Brak proponowanej nazwy | Funkcjonalny: „Zamieniamy chaotyczną wiedzę firmową w akcję rekrutacyjną" |
| **Adam** | **TeamTwin** | Emocjonalny: „A gdybyś mógł zadzwonić do kolegi, który odszedł?" |
| **Przemek** | **OrgBrain** (alternatywy: KnowledgeGraph.ai, Hivemind) | Oparty na danych: „31,5 mld $ traconych rocznie na słabe dzielenie się wiedzą" |

### 6. Głębokość badań rynkowych

| Plan | Poziom badań |
|------|-------------|
| **Maks** | Brak — czysty fokus na produkcie/demo |
| **Adam** | Brak — czysty fokus techniczny/UX |
| **Przemek** | **Rozbudowany** — TechWolf (53 mln $ pozyskane), Eightfold (wycena 2,1 mld $), Gloat (1 mld $), Interloom (16,5 mln $), Aware, Glean (4,6 mld $). Statystyki McKinsey, dane IDC, WEF Future of Jobs 2025, Deloitte 2025. Konkretne liczby do pitcha: 31,5 mld $ (IDC), 42% (Panopto), 87% firm (McKinsey) |

### 7. Stanowisko wobec prywatności i etyki

| Plan | Pozycja |
|------|---------|
| **Maks** | Ostrzega: nigdy nie obiecuj automatycznego zatrudniania, mów „asystuje zespołom rekrutacyjnym", „finalna decyzja należy do zespołu rekrutacyjnego" |
| **Adam** | Krótkie zamknięcie: „TeamTwin nie jest zamiennikiem dla ludzi" |
| **Przemek** | Konkretny: potrzeba slajdu „privacy by design", odwołanie do backlashu medialnego Aware z 2024 |
| **Plan Mike** | Nie adresowany — używa publicznych danych prawdziwej osoby bez jawnej dyskusji o zgodzie |

### 8. Głębokość pozyskiwania danych

| Plan | Strategia danych |
|------|-----------------|
| **Maks** | Abstrakcyjna — „3 typy danych: repo/docs, transkrypcje, CV" |
| **Adam** | 6 komponentów wymienionych (ingestion danych, context builder, konfiguracje agentów, integracja Gemini, generator wyników, frontend) |
| **Plan Mike** | **Niezwykle szczegółowy** — 4 warstwy klonowania, 11+ repozytoriów GitHub z dokładnymi poleceniami, 9 zapytań wyszukiwania YouTube, odcinki podcastów po nazwie, URL transkrypcji Q&A Reactiflux, źródła Medium/Twitter, szablony danych syntetycznych (wątki Slack, tickety Jira, notatki 1:1, ADR-y) |
| **Plan K8s** | **Równie szczegółowy** — 7 kategorii danych, struktura folderów, kroki pipeline'u z estymacjami czasu, konkretne przykłady wątków Slack, szablony ticketów Jira, szablon profilu kompetencji, checklista z minimalnymi wymaganiami danych |

### 9. Unikalne wkłady każdego planu

| Plan | Unikalny element |
|------|-----------------|
| **Maks** | Systematyczny **framework scoringowy** (Running Code / Innovation / Impact / Theme Alignment) zastosowany do 3 alternatywnych kierunków. Jedyny plan, który jawnie rankuje opcje z kryteriami |
| **Adam** | Koncept **osobowości agenta** — ekstrakcja stylu komunikacji z transkrypcji, żeby klon brzmiał jak prawdziwa osoba, nie generyczny chatbot. Najsilniejszy element „wow" |
| **Przemek** | Moment **zsynchronizowanego głosu + wizualizacji** — odpowiedź głosowa gra, podczas gdy dashboard aktualizuje się w czasie rzeczywistym przez WebSocket. Także: rozbudowana **wizja post-hackathonowa** (due diligence M&A, incident response, buddy onboardingowy, ocena gotowości AI) |
| **Plan Mike** | Jedyny plan używający **prawdziwej, rozpoznawalnej publicznej postaci** — Mike Grabowski jest znany w ekosystemie React Native. Demo byłoby natychmiast wiarygodne |
| **Plan K8s** | Najlepiej zdefiniowany **pipeline danych i struktura folderów** — gotowy do implementacji z poleceniami copy-paste. Zawiera estymacje czasu na fazę i jasny podział zadań Dev/non-dev |

---

## Porównanie scoringu

Wszystkie trzy główne plany (Maks, Adam, Przemek) dostarczają samooceny wobec kryteriów hackathonu:

| Kryterium | Maks (po zawężeniu) | Adam (TeamTwin) | Przemek (OrgBrain) |
|-----------|---------------------|-----------------|-------------------|
| **Running Code** | 4/5 | 4-5/5 | Bez oceny (plan sugeruje 4-5) |
| **Innovation & Creativity** | 4/5 | 4-5/5 | Bez oceny (sugeruje 4-5) |
| **Real-world Impact** | 4/5 | 5/5 | Bez oceny (rozbudowana walidacja rynkowa) |
| **Theme Alignment** | 4/5 (z głosem + multimodalnymi wejściami) | 5/5 (3 agenty głosowe na Gemini + Vapi) | 9/10 (voice-first + graph viz + multimodal) |

---

## Porównanie alokacji zadań

### Maks — brak jawnej alokacji
Skupia się na tym, co wyciąć, nie na tym, kto co robi. Definiuje ograniczenia zakresu jako główne narzędzie planistyczne.

### Adam (TeamTwin) — 5 faz

| Faza | Czas | Fokus |
|------|------|-------|
| Fundament | 2-3h | Przygotowanie danych mockowych, setup Gemini + Vapi, proof of concept |
| Knowledge Clone | 2-3h | Context builder, system prompt z osobowością, integracja multimodalna |
| Recruitment Generator | 2h | Szablony, prompt engineering, iteracja głosu |
| Interview Agent | 2h | Bank pytań, logika adaptacyjna, scoring w czasie rzeczywistym |
| Polerowanie + Demo | 1-2h | Dashboard, próba end-to-end, plan awaryjny |

### Przemek (OrgBrain) — plan 7-godzinny

| Faza | Czas | Fokus |
|------|------|-------|
| Setup | 0-1h | Init repo, konto Vapi, klucze API, boilerplate React, skrypt demo, dane mockowe |
| Core Build | 1-3h | Agent Vapi + 3 narzędzia (Dev 1), FastAPI + Neo4j (Dev 2), dashboard React + D3.js (Dev 3) |
| Integracja | 3-5h | Głos → API → graph → odpowiedź głosowa, frontend → API, test end-to-end |
| Polerowanie | 5-6.5h | Bugfixy, utwardzanie ścieżki demo, 3x próba demo |
| Ubezpieczenie | 6.5h | Nagranie zapasowego wideo |
| Prezentacja | 7-8h | Zamrożenie kodu, czysty browser, prezentacja |

### Plany danych — oddzielne timeline'y

| Faza | Plan Mike | Plan K8s |
|------|-----------|----------|
| Automatyczne zbieranie danych | 2-3h | 2-3h |
| Zbieranie ręczne/półautomatyczne | 1-2h | — |
| Tworzenie danych syntetycznych | 2-3h | 1.5-2h |
| Budowanie profilu | — | 1h |
| Przetwarzanie i strukturyzacja | — | 1h |
| Konfiguracja agenta | — | 1-2h |
| **Łącznie** | **5-8h** | **6-9h** |

---

## Macierz ryzyk (zagregowana)

| Ryzyko | Zidentyfikowane przez | Mitygacja |
|--------|----------------------|-----------|
| Zbyt szeroki zakres | Maks, Adam | Tnij bezlitośnie — jeden przepływ, max 3 wejścia |
| Nie da się obronić dokładności rekomendacji | Maks | Warstwa dowodów z cytowaniami źródeł |
| Demo wygląda jak „kolejny RAG SaaS" | Maks | Interakcja głosowa + multimodalne wejścia sprawiają, że czuje się inaczej |
| **„To po prostu NotebookLM"** | **Spotkanie 1** | **Generowanie pakietu rekrutacyjnego to must-have wyróżnik. Także: auto-aktualizacja, wiele osób, mapowanie kompetencji** |
| Problemy z latencją (Vapi + Gemini) | Adam | Testuj wcześnie, fallback na Gemini Flash |
| Agent brzmi robotycznie | Adam | Dostrój system prompt z „osobowością", testuj ustawienia głosu |
| Awaria demo na żywo | Adam, Przemek | Nagraj zapasowe wideo o godz. 6.5 |
| Jakość danych mockowych | Adam, plan K8s | Zainwestuj czas w realistyczne, wewnętrznie spójne dane |
| Backlash prywatności | Maks, Przemek | Slajd „privacy by design", framing „asystuje" a nie „decyduje" |
| Za dużo integracji | Maks | Ogranicz do 2-3 źródeł danych, dobrze połączonych w jednym przepływie |
| Neo4j dodaje złożoność | (pośrednio w planie Przemka) | Rozważ porzucenie graph DB jeśli opóźnienie — okno kontekstu Gemini może wystarczyć |

---

## Synteza: mocne strony do połączenia

Najsilniejszy możliwy wpis hackathonowy łączyłby:

1. **Od Maksa** — Dyscyplina zakresu, 3-minutowy timing demo, framework scoringowy, ramowanie produktowe („asystuje zespołom rekrutacyjnym")
2. **Od Adama (TeamTwin)** — Koncept osobowości agenta, hak „zadzwoń do byłego kolegi", setup z dwoma telefonami na scenie, architektura 3 agentów
3. **Od Przemka (OrgBrain)** — Liczby z badań rynkowych do pitcha (31,5 mld $, 87%, 42%), moment zsynchronizowanego głosu + dashboardu, pozycjonowanie konkurencyjne, wizja post-hackathonowa
4. **Od planu Mike** — Strategia pozyskiwania danych prawdziwej osoby (adaptowalny do wybranej persony), 4-warstwowy model klonowania (wiedza, styl myślenia, styl komunikacji, kontekst organizacyjny)
5. **Od planu K8s** — Struktura folderów, polecenia pipeline'u danych, gotowość oparta na checkliście, jasny podział zadań Dev/non-dev

---

## Decyzje ze spotkania 1 (2026-03-28)

Spotkanie zespołu rozwiązało większość wcześniej otwartych decyzji. Szczegóły w `summary_narada1.md`.

### Rozwiązane decyzje

| # | Pytanie | Decyzja |
|---|---------|---------|
| 1 | **Kogo klonujemy?** | **Mike Grabowski** — prawdziwa osoba, prawdziwe publiczne dane. Wsparcie wielu osób odłożone na przyszłość. |
| 2 | **Architektura** | **Vapi** (warstwa głosowa) + **Google Agent SDK / ADK** (mózg agenta). Bez Neo4j — ADK obsługuje wiedzę. Proces ADK można wizualizować podczas demo. |
| 3 | **Przebieg demo** | Dwie fazy: (1) Zapytanie o wiedzę — zadzwoń do Mike'a, zapytaj o decyzję projektową; (2) Pakiet rekrutacyjny — poproś Mike'a o wygenerowanie JD, zadań, kryteriów na jego zastępstwo. |
| 4 | **Multimodalność** | Minimum: **głos + tekst**. Opcjonalne dodatki (wideo, grafika) jeśli starczy czasu. Dwie modalności uznane za wystarczające. |
| 5 | **Przygotowanie danych** | Adam organizuje wstępnie zebrane dane (GitHub, podcasty, syntetyczne). Dane muszą być w Markdown/JSON. Funkcja odświeżania pożądana, ale nie wymagana na demo. |
| 6 | **Podział zadań** | Max+Janusz → core dev; Adam → dane; Przemek+Mieszko → narracja, nazwa, prezentacja, UI. |
| 7 | **Co odróżnia to od NotebookLM?** | Pakiet rekrutacyjny / funkcja luki kompetencyjnej jest kluczowym wyróżnikiem. Auto-aktualizacja danych i routing wielu osób to wyróżniki drugorzędne. |

### Wciąż otwarte

| # | Pytanie | Status |
|---|---------|--------|
| 1 | **Nazwa produktu** | Nie zdecydowano — Przemek + Mieszko mają zaproponować |
| 2 | **Dokładny skrypt demo z timingiem** | Do iteracji po ~1 godzinie |
| 3 | **Czas trwania demo** | Nie ustalono jawnie (plany wahają się od 3 do 5 min) |
| 4 | **Szczegóły UI** | Zespół produktowy ma zdefiniować, potem devs pomagają implementować |
| 5 | **Strona WWW** | Do stworzenia przez Przemka + Mieszka |

### Zidentyfikowane krytyczne ryzyko: porównanie z NotebookLM

Zespół poświęcił znaczną ilość czasu na omówienie ryzyka, że członek jury powie: *„To po prostu NotebookLM z numerem telefonu."*

**Uzgodniona strategia mitygacji:**

| Wyróżnik | NotebookLM | Nasz system |
|-----------|------------|-------------|
| Auto-aktualizacja | Statyczny, ręczne wgrywanie | Ciągłe pozyskiwanie i reindeksowanie |
| Wiele osób | Jeden blob wiedzy | Odrębne persony per osoba (przyszłość, ale pokazane w architekturze) |
| Wartość akcyjna | Tylko Q&A | Pakiety rekrutacyjne, JD, zadania rekrutacyjne, kryteria oceny |
| Mapowanie kompetencji | Brak | Ekstrakcja umiejętności, identyfikacja luk, routing do właściwej osoby |
| Skala | Ograniczony kontekst | Skala organizacji, wiele osób |

Generowanie pakietu rekrutacyjnego jest **must-have** funkcją broniącą przed tym zarzutem. Bez niej produkt jest podatny.

### Wizja produktu (doprecyzowana na spotkaniu)

Spotkanie wyostrzyło pozycjonowanie wykraczające poza oryginalne plany:

> Platforma dla C-level, która wspiera wzrost organizacyjny poprzez identyfikację najlepszych inwestycji kompetencyjnych — kogo zatrudnić, jakich umiejętności brakuje i jak znaleźć właściwych ludzi.

Kluczowy insight z dyskusji: produkt rozwiązuje **meta-problem** — organizacje, które nie potrafią artykułować jakich kompetencji potrzebują. System analizuje artefakty pracy i przekłada wiedzę ukrytą (tacit knowledge) na ustrukturyzowane wymagania rekrutacyjne.

Docelowi użytkownicy: szybko rosnące startupy, zespoły tracące kluczowe osoby, organizacje bez dedykowanego HR/Chief of Staff.
