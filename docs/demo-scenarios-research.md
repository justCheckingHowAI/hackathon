# Research & Scenariusze Demo — Gemellus

**Data:** 2026-03-28
**Kontekst:** Hackathon — multimodal agents | Stack: Vapi + Gemini 2.5 + Google ADK
**Klon:** Mike Grabowski (CTO Callstack, React Native Core Team)

---

## Część 1: Doprecyzowanie ustaleń

### 1. Dokładne pytania do demo — słowo w słowo

Poniższe pytania odwołują się do **prawdziwych projektów i artefaktów** Mike'a, potwierdzonych w danych z GitHub, konferencji, podcastów i syntetycznych danych wewnętrznych (Slack, Jira, notatki 1:1).

#### Faza 1 — Pozyskanie wiedzy (rozmowa telefoniczna)

**Pytanie 1 (rozgrzewka — naturalne, koleżeńskie):**
> „Hej Mike, sorry że dzwonię — wiem, że masz wolne. Słuchaj, mamy u klienta problem z Module Federation na Hermes. Kontenery nie ładują się na Androidzie, leci błąd z `__webpack_require__.l`. Czy to ten znany issue?"

**Dlaczego to pytanie działa:**
- Brzmi jak prawdziwy telefon do kolegi — nie jak prompt do AI
- Odwołuje się do **realnego buga** (Slack #repack-dev, 2025-02-05 + RPACK-445 w Jira)
- Mike agent może odpowiedzieć z głębokim kontekstem: „Tak, to znany problem. Hermes nie wspiera standardowego mechanizmu chunk loading przez script tagi, bo nie ma DOM-u w React Native. Mamy custom runtime plugin — dodaj `chunkLoading: 'async-node'` w webpack config i włącz `Repack.plugins.ChunkLoadingPlugin` z flagą experimental. Beta pełnego fixa jest gotowa od marca."
- Agent cytuje konkretne rozwiązanie, nie generyczny „spróbuj zaktualizować zależności"

**Pytanie 2 (głębsze — decyzja architektoniczna):**
> „OK, a szerzej — klient pyta czy w ogóle powinni iść w Re.Pack czy zostać na Metro. Mają monorepo, 12 pakietów, współdzielony kod z webem. Co byś im powiedział?"

**Dlaczego to pytanie działa:**
- Dotyczy **konkretnej decyzji architektonicznej**, którą Mike udokumentował w ADR (CORE-155)
- Odpowiedź agenta powinna brzmieć jak ekspert, nie jak dokumentacja: „Przy 12 pakietach i współdzielonym kodzie z webem — Re.Pack, bez dyskusji. Metro nie daje ci Module Federation ani code splittingu. Ale kluczowe pytanie to nie wydajność — oba są wystarczająco szybkie. Chodzi o ekosystem webpacka. Jeśli klient ma już webpack pluginy, loadery, custom build pipeline — Re.Pack pozwala to reużyć na mobile. Nie zmieniasz narzędzi, rozszerzasz je."
- Buduje **narrację prowadzącą do Fazy 2** — bo uwidacznia głębokość wiedzy, którą trzeba by odtworzyć

**Pytanie 3 (most do Fazy 2 — emocjonalne + strategiczne):**
> „Mike, last thing. Wiesz, że myślimy o scenariuszach na wypadek gdybyś... no, gdybyś nie był dostępny długoterminowo. Sam mówiłeś na 1:1 z boardem, że jesteś single point of failure dla kilku krytycznych obszarów. Gdybyś odszedł jutro — kogo powinniśmy szukać?"

**Dlaczego to pytanie działa:**
- Odwołuje się do **prawdziwej rozmowy** Mike'a z boardem (1:1 notes, 2025-03-17): „Re.Pack runtime internals — only I fully understand the chunk loading mechanism. Auto-linking architecture — I wrote the original design. Relationship with Meta's RN team. Release process tribal knowledge."
- Naturalnie otwiera Fazę 2
- Agent powinien odpowiedzieć emocjonalnie ale konkretnie: „Szczerze? Największe ryzyko to cztery obszary..." — i wylistować dokładnie te same 4 punkty z notatek 1:1

#### Faza 2 — Generowanie pakietu rekrutacyjnego

**Pytanie 4 (polecenie akcji):**
> „OK Mike, to zróbmy to porządnie. Przygotuj mi kompletny pakiet rekrutacyjny na twoje zastępstwo. Job description, zadania techniczne, kryteria oceny. Tak jak przygotowałeś format rozmowy dla tej ostatniej rekrutacji tooling engineera."

**Dlaczego to pytanie działa:**
- Odwołuje się do **realnego artefaktu** — Mike faktycznie zdefiniował format interview na Slacku (#hiring, 2025-02-20) i w Jira (HIRE-301)
- Agent nie generuje generic JD — buduje pakiet na podstawie własnej wiedzy o roli
- Moment, w którym agent przechodzi z rozmowy na **generowanie dokumentu** — wizualnie widoczne na ekranie

---

### 2. Momenty „wow" — 3 zidentyfikowane

#### Wow #1: „Agent cytuje swoje własne Slacki i tickety"

**Co się dzieje:** Gdy Mike-agent odpowiada na pytanie o Hermes bug, na dashboardzie pojawia się panel „Sources" z konkretnymi odwołaniami:
- 📎 Slack #repack-dev (2025-02-05) — thread o `__webpack_require__.l`
- 📎 RPACK-445 — Jira ticket o Hermes compatibility layer
- 📎 Commit `a3f7c2d` — fix w chunk loading plugin

**Dlaczego to wow:**
- NotebookLM **nigdy** nie pokazuje, skąd ma informację na tym poziomie granularności
- Zwykły RAG zwraca „based on the documents" — tu widzisz konkretny Slack thread, datę, kontekst
- Jury widzi, że to nie jest generyczna odpowiedź — to odtworzenie **rzeczywistego sposobu myślenia konkretnego człowieka** z konkretnymi dowodami

**Techniczna wykonalność:** Gemini z narzędziem `search_knowledge_base` zwraca chunki z metadanymi (source, date, channel). Frontend wyświetla je jako linked sources. ADK Web UI pokazuje tool call i zwrócone dane.

#### Wow #2: „Hiring pack jest absurdalnie precyzyjny"

**Co się dzieje:** Agent generuje pakiet rekrutacyjny, który pojawia się na ekranie. Jury widzi:

```
STANOWISKO: Senior React Native Build Systems Engineer
(nie "Senior React Native Developer" — to inna rola)

WYMAGANE KOMPETENCJE:
• Webpack internals — rozumienie chunk loading, runtime plugins,
  Module Federation protocol (nie "znajomość webpacka")
• Doświadczenie z native build systems: Xcode toolchain (xcrun, xcodebuild),
  Gradle Plugin API, CocoaPods Podspec DSL
• Hermes bytecode pipeline — kompilacja AOT, debugowanie bytecode
  cache z dynamicznie ładowanymi chunkami
• React Native auto-linking architecture — codegen dla iOS (Podfile)
  i Android (settings.gradle), edge cases: scoped packages,
  monorepo symlinks, TurboModule detection

ZADANIE REKRUTACYJNE:
Kandydat otrzymuje repozytorium z aplikacją React Native korzystającą
z auto-linkingu. Jedna z natywnych bibliotek nie linkuje się poprawnie
na iOS z włączoną New Architecture. Zadanie: zdiagnozuj przyczynę
i zaproponuj fix. Czas: 45 minut.

(Rzeczywisty bug — CLI-892, naprawiony przez Mike'a w lutym 2025.
Testuje zrozumienie pipeline'u RN + umiejętność debugowania.)
```

**Dlaczego to wow:**
- Porównaj z ChatGPT-wygenerowanym JD: „5+ years React Native, strong problem-solving skills, team player" — **generyczna papka**
- Tu masz opis stanowiska, który **tylko Mike mógłby napisać**, bo wynika z jego doświadczenia z konkretnymi bugami, projektami i decyzjami
- Zadanie rekrutacyjne oparte na **realnym incydencie** — to coś, czego żaden ATS ani HR tool nie wygeneruje

**Techniczna wykonalność:** Gemini generuje structured output (JSON → renderowany jako dokument). Dane o bugu CLI-892 i formacie interview z Jira/Slack są w knowledge base.

#### Wow #3: „Głos Mike'a + natychmiastowe źródła na ekranie = multimodalność in action"

**Co się dzieje:** Prezenter dzwoni do agenta przez prawdziwy telefon (Vapi). Mike-agent odpowiada **głosem sklonowanym z podcastów Mike'a** (ElevenLabs instant clone). Jednocześnie na ekranie dashboardu widać:
- Transkrypcję rozmowy w czasie rzeczywistym
- Panel ADK: jakie narzędzia agent wywołał (search_knowledge → generate_hiring_pack)
- Panel źródeł: dokumenty, z których agent czerpie
- Generowany hiring pack pojawiający się sekcja po sekcji

**Dlaczego to wow:**
- **Trzy modalności jednocześnie:** głos (telefon) + tekst (transkrypcja + źródła) + structured document (hiring pack)
- NotebookLM generuje podcast do odsłuchania — tu masz **interaktywną rozmowę z wizualizacją procesu rozumowania**
- Dashboard „pod maską" pokazuje, że to nie jest script — agent naprawdę myśli, szuka, generuje

**Techniczna wykonalność:**
- Vapi: STT + routing do Gemini + TTS z ElevenLabs clone (1-2 min audio z React Native Show podcast)
- ADK Web UI: events tab z tool calls (search_knowledge_base, analyze_skills, generate_hiring_pack)
- Frontend React: WebSocket listener na events z ADK, renderuje panel źródeł i hiring pack w real-time

---

## Część 2: Scenariusze demo

---

### Scenariusz A — „Człowiek, którego nie można zastąpić" (podejście emocjonalne)

**Czas:** ~4 minuty
**Ton:** historia → empatia → wartość → call to action

---

#### Hook otwierający (0:00–0:25)

**PREZENTER** *(stoi na scenie, bez slajdów, mówi do publiczności)*:

> „W marcu 2025 Mike Grabowski — CTO Callstack, członek React Native Core Team, maintainer Re.Pack i CLI — powiedział na spotkaniu z boardem: *'Jestem single point of failure dla zbyt wielu rzeczy. Jeśli odejdę jutro, macie problem.'*
>
> Trzy tygodnie później dostał ofertę, której nie mógł odrzucić.
>
> Co robi firma, gdy odchodzi człowiek, który ma w głowie architekturę, kontekst każdej decyzji i relacje z Meta?"

**EKRAN:** Czarny ekran → pojawia się profil Mike'a Grabowskiego (zdjęcie, nazwa, rola: CTO Callstack) z listą jego kluczowych projektów: Re.Pack (1.9k ⭐), React Native CLI (2.9k ⭐), rnpm (merged into RN core).

---

#### Faza 1: Rozmowa z klonem (0:25–2:00)

**PREZENTER** *(wyciąga telefon)*:

> „Pokażę wam. Zadzwonimy do Mike'a. A raczej — do jego cyfrowego klona, stworzonego z jego GitHub PR-ów, transkrypcji konferencji, podcastów, wewnętrznych Slacków i notatek projektowych."

**EKRAN:** Dashboard Gemellus. Lewa strona: dialer z napisem „Calling Mike Grabowski (clone)...". Prawa strona: pusty panel „Agent Activity" i „Sources".

*Telefon dzwoni. Agent odbiera głosem Mike'a.*

**AGENT-MIKE** *(głos sklonowany z podcastów)*:

> „Hej, co tam? Czym mogę pomóc?"

**PREZENTER:**

> „Mike, mamy problem u klienta. Module Federation na Hermes — kontenery nie ładują się na Androidzie. Leci coś z webpack require. Wiesz o co chodzi?"

**EKRAN:** Panel „Agent Activity" się animuje — pojawia się: `🔍 search_knowledge_base("Module Federation Hermes Android error")` → ładuje się przez ~1s → wyniki: Slack #repack-dev thread, RPACK-445 Jira ticket.

**AGENT-MIKE:**

> „Tak, to znany issue. Hermes nie wspiera standardowego chunk loadingu przez script tagi — bo w React Native nie ma DOM-u. Leci error z `__webpack_require__.l` — to webpack próbuje załadować chunk tak jak w przeglądarce, a na mobile to nie działa.
>
> Mamy na to custom runtime plugin. Powiedz klientowi żeby w webpack configu dodał `chunkLoading: async-node` i włączył nasz `ChunkLoadingPlugin` z flagą experimental. Beta pełnego fixa jest w branchu od marca. Mogę podrzucić linka do PR-a."

**EKRAN:** Panel „Sources" wyświetla:
- 📎 Slack #repack-dev (2025-02-05) — wątek o `__webpack_require__.l`
- 📎 RPACK-445 — Hermes compatibility layer
- 📎 PR #1247 — custom chunk loading implementation

**PREZENTER:**

> „Mike, a szerzej — ten klient ma monorepo, 12 pakietów, współdzielony kod z webem. Powinni zostać na Metro czy iść w Re.Pack?"

**AGENT-MIKE:**

> „Przy 12 pakietach i współdzielonym kodzie z webem — Re.Pack, nie ma dyskusji. Metro nie da im Module Federation ani code splittingu. Ale kluczowe tu nie jest wydajność — oba bundlery są wystarczająco szybkie. Chodzi o ekosystem webpacka. Jeśli klient ma już swoje pluginy, loadery, custom build pipeline — Re.Pack pozwala to reużyć na mobile. Nie zmieniasz narzędzi, rozszerzasz je na nową platformę."

**EKRAN:** Panel „Sources" dodaje: 📎 ADR CORE-155 — „Metro vs Re.Pack for enterprise monorepo clients"

---

#### Faza 2: Generowanie hiring packu (2:00–3:30)

**PREZENTER** *(zmienia ton na poważniejszy)*:

> „Mike, last thing. Jesteś single point of failure dla Re.Pack runtime, auto-linkingu, relacji z Meta i release process. Gdybyś odszedł jutro — przygotuj mi pakiet rekrutacyjny na twoje zastępstwo. Job description, zadania, kryteria. Pełny hiring pack."

**AGENT-MIKE** *(krótka pauza — jakby się zastanawiał)*:

> „Rozumiem. OK, to nie jest prosta rekrutacja, bo to nie jest 'Senior React Native Developer' — to osoba, która musi rozumieć build systems od środka. Daję ci pełen pakiet. Pojawi się na dashboardzie za chwilę."

**EKRAN:** Panel „Agent Activity" pokazuje sekwencję narzędzi:
1. `🔍 analyze_skills("mike")` — analiza kompetencji Mike'a
2. `📊 identify_knowledge_gaps()` — identyfikacja luk
3. `📝 generate_hiring_pack()` — generowanie pakietu

Na prawej stronie ekranu zaczyna się pojawiać **hiring pack**, sekcja po sekcji:

```
═══════════════════════════════════════════════════
  PAKIET REKRUTACYJNY — Zastępstwo Mike Grabowski
  Wygenerowano przez Gemellus | Źródła: 185 PR-ów,
  8 konferencji, 10 ticketów Jira, 8 wątków Slack
═══════════════════════════════════════════════════

STANOWISKO: Senior React Native Build Systems Engineer

NIE SZUKAMY:
  × "Full-stack React Native developera"
  × "Kogoś kto zna webpacka"

SZUKAMY:
  → Osoby rozumiejącej bundler internals: chunk loading,
    runtime plugins, Module Federation protocol
  → Doświadczenia z native build systems: Xcode toolchain
    (xcrun, xcodebuild), Gradle Plugin API, CocoaPods
  → Znajomości Hermes bytecode pipeline — kompilacja AOT,
    cache invalidation z dynamicznymi chunkami
  → Open source maturity — triaging 200+ issues, release
    process, community management

ZADANIE REKRUTACYJNE:
  Repozytorium z aplikacją RN + auto-linking.
  Jedna natywna biblioteka nie linkuje się z New Architecture.
  Zadanie: zdiagnozuj i zaproponuj fix. (45 min)
  ↳ Bazowane na CLI-892 — real bug, naprawiony 2025-02-04

SCORING (0-5):
  • Bundler internals .............. waga 30%
  • Native build systems .......... waga 25%
  • Module Federation ............. waga 20%
  • Open source & communication ... waga 15%
  • Hermes / performance .......... waga 10%
```

---

#### Zamknięcie (3:30–4:00)

**PREZENTER** *(odkłada telefon, mówi do jury)*:

> „To, co właśnie widzieliście, to nie jest chatbot. To nie jest RAG z ładnym głosem. To system, który zamienia wiedzę jednej osoby — zbudowaną przez lata commitów, rozmów, decyzji — w konkretne, akcyjne dokumenty.
>
> 42 procent wiedzy instytucjonalnej w firmach jest posiadane przez jedną osobę. Gdy ta osoba odchodzi, firma traci miesiące na odbudowę. Gemellus sprawia, że ta wiedza nie odchodzi razem z nią.
>
> **Gemellus** — *your team's knowledge, always on call.*"

**EKRAN:** Logo Gemellus + tagline. Pod spodem: `gemellus.app`

---

#### Scoring Scenariusza A

| Kryterium | Ocena | Uzasadnienie |
|-----------|-------|--------------|
| **Running Code** | 5/5 | Prawdziwa rozmowa telefoniczna, real-time tool calls, generowany dokument — zero slajdów, 100% working code |
| **Innovation & Creativity** | 4/5 | Voice clone + knowledge extraction + actionable output to nowe połączenie, ale poszczególne elementy (RAG, voice, hiring) istnieją osobno |
| **Real-world Impact** | 5/5 | Problem 31,5 mld $/rok, 42% wiedzy u jednej osoby — bezpośrednio adresowany, z wymiernym outputem (hiring pack) |
| **Theme Alignment** | 5/5 | Multimodal = głos (Vapi/ElevenLabs) + tekst (knowledge base) + structured documents (hiring pack) + wizualizacja (ADK). Pełna multimodalność |
| **Łącznie** | **19/20** | |

---

### Scenariusz B — „Pod maską" (podejście techniczne)

**Czas:** ~4 minuty
**Ton:** problem techniczny → architektura → live demo → rozwiązanie

---

#### Hook otwierający (0:00–0:20)

**PREZENTER** *(slajd z architekturą na ekranie)*:

> „Zbudowaliśmy system, który w 6 godzin zjada 185 pull requestów, 8 transkrypcji konferencji, 10 ticketów Jira i 8 wątków Slacka — i zamienia to w agenta głosowego, który odpowiada jak człowiek, który te rzeczy napisał. Pokażę wam jak to działa pod spodem."

**EKRAN:** Diagram architektury:
```
┌──────────┐    STT     ┌──────────┐   HTTP    ┌──────────────┐
│  Telefon │ ────────→  │   Vapi   │ ────────→ │  FastAPI +   │
│  (User)  │ ←──────── │ (Voice)  │ ←──────── │  Google ADK  │
└──────────┘    TTS     └──────────┘   JSON    │  + Gemini    │
                (ElevenLabs                     │  2.5 Flash   │
                 clone)                         └──────┬───────┘
                                                       │
                                                       ▼
                                                ┌──────────────┐
                                                │ Knowledge    │
                                                │ Base (40K    │
                                                │ tokens)      │
                                                └──────────────┘
```

---

#### Faza 1: Pokaz architektury na żywo (0:20–1:50)

**PREZENTER:**

> „Trzy warstwy. Vapi obsługuje telefon — speech-to-text i text-to-speech z głosem sklonowanym z 2 minut podcastu Mike'a Grabowskiego. Google ADK orkiestruje agenta — widać dokładnie co robi. Gemini 2.5 Flash dostaje cały kontekst Mike'a w jednym prompcie — 40 tysięcy tokenów, zero chunkowania, zero RAG-owej halucynacji."

**PREZENTER** *(wskazuje na ekran)*:

> „Dzwonię do agenta. Obserwujcie prawą stronę ekranu."

*Telefon dzwoni.*

**AGENT-MIKE** *(głos Mike'a)*:

> „Siema, o co chodzi?"

**PREZENTER:**

> „Mike, klient pyta dlaczego wybraliśmy Re.Pack zamiast Metro dla ich projektu z Module Federation. Co im powiedzieć?"

**EKRAN — ADK Web UI (events tab):**
```
▶ user_message: "klient pyta dlaczego wybraliśmy Re.Pack..."
▶ thinking: "User asks about Metro vs Re.Pack decision
   for Module Federation use case..."
▶ tool_call: search_knowledge_base({
     query: "Metro vs Re.Pack Module Federation decision",
     sources: ["jira", "slack", "talks"]
   })
▶ tool_result: [
     CORE-155: ADR Metro vs Re.Pack,
     Slack #general 2025-02-15: "Why does Callstack maintain Re.Pack",
     Talk: Chain React 2017 "The Dark Art of Bundlers"
   ]
▶ generating_response...
```

**AGENT-MIKE:**

> „Metro jest świetny dla 80 procent projektów — szybki, dobrze zintegrowany, utrzymywany przez Meta. Ale jeśli klient potrzebuje Module Federation — to koniec dyskusji, Metro tego nie umie. Re.Pack daje im: dynamiczne ładowanie kodu, code splitting, integrację z istniejącym build pipeline webpackowym. Pisałem o tym ADR-a na bazie pracy z pięcioma klientami enterprise. Kluczowa różnica to nie wydajność — to ekosystem."

**PREZENTER** *(wskazuje na ekran)*:

> „Widzicie? Agent nie zgaduje. Wywołał narzędzie `search_knowledge_base`, znalazł trzy źródła — ADR, Slacka i talk z 2017 — i skonstruował odpowiedź. Każdy krok jest transparentny. A teraz... moment, na który czekaliście."

---

#### Faza 2: Generowanie hiring packu — live (1:50–3:20)

**PREZENTER:**

> „Mike, potrzebujemy twojego zastępstwa. Wygeneruj hiring pack — kompletny, z zadaniem technicznym i scoring rubric."

**EKRAN — ADK Web UI pokazuje łańcuch agentów:**
```
▶ tool_call: analyze_skills({person: "mike_grabowski"})
  → Result: {
      primary: ["bundler_internals", "module_federation",
                "native_build_systems", "hermes_engine",
                "open_source_maintenance"],
      unique: ["repack_runtime_architecture",
               "autolinking_codegen",
               "meta_relationship"],
      transferable: ["react_native_paper", "ai_incubator"]
    }

▶ tool_call: generate_hiring_pack({
    role: "replacement_for_mike",
    skills: [analyzed_skills],
    existing_interview_formats: "HIRE-301"
  })
  → Generating...
```

*Na ekranie, obok panelu ADK, zaczyna się renderować dokument hiring pack:*

**AGENT-MIKE:**

> „OK, słuchaj — to nie jest stanowisko 'React Native Developer'. To osoba, która musi rozumieć jak bundler komunikuje się z natywnym build systemem. Generuję ci pełen pakiet z zadaniem rekrutacyjnym opartym na prawdziwym bugu, który naprawiałem w lutym..."

**EKRAN:** Hiring pack renderuje się na żywo — sekcja po sekcji (identyczna treść jak w Scenariuszu A, ale tu jury widzi **cały proces generowania** w ADK events tab, nie tylko output).

Kluczowy moment: gdy pojawia się sekcja „ZADANIE REKRUTACYJNE" z adnotacją `↳ Bazowane na CLI-892`, w ADK events widać:
```
▶ tool_call: search_knowledge_base({
    query: "real bugs suitable for interview task",
    filter: {type: "bug", assignee: "mike", status: "done"}
  })
▶ tool_result: CLI-892 — Auto-linking breaks with New Architecture
```

**PREZENTER** *(wskazuje)*:

> „Widzicie? Agent nie wymyślił zadania rekrutacyjnego z powietrza. Przeszukał bazę bugów Mike'a, znalazł naprawiony critical — i użył go jako podstawy testu. To jest coś, czego żaden ATS na rynku nie robi."

---

#### Zamknięcie (3:20–4:00)

**PREZENTER:**

> „Trzy modalności: głos, tekst, structured documents. Trzy warstwy: Vapi na telefonie, Google ADK do orkiestracji, Gemini 2.5 Flash do rozumowania z pełnym kontekstem 40 tysięcy tokenów. I transparentny łańcuch — widzicie każdy tool call, każde źródło, każdą decyzję.
>
> To nie jest chatbot. To cyfrowy bliźniak, który rozumie dlaczego decyzje zostały podjęte — i potrafi tę wiedzę zamienić w konkretne akcje HR.
>
> **Gemellus** — *clone minds, not just data.*"

**EKRAN:** Logo Gemellus + `gemellus.app`. Pod spodem statystyki: `185 PRs | 8 talks | 10 tickets | 8 Slack threads → 1 actionable hiring pack in 30 seconds`

---

#### Scoring Scenariusza B

| Kryterium | Ocena | Uzasadnienie |
|-----------|-------|--------------|
| **Running Code** | 5/5 | Live demo z widocznym procesem agenta — ADK events, tool calls, source matching. Nie da się sfejkować |
| **Innovation & Creativity** | 5/5 | Transparentny łańcuch rozumowania agenta na żywo + knowledge-to-action pipeline — innowacyjne podejście do explainability |
| **Real-world Impact** | 4/5 | Problem realny, ale techniczne podejście może nie rezonować z jury biznesowym — mniej emocji, więcej architektury |
| **Theme Alignment** | 5/5 | Multimodalność widoczna w architekturze: głos (Vapi) + tekst (knowledge base) + structured output (hiring pack) + wizualizacja procesu (ADK UI) |
| **Łącznie** | **19/20** | |

---

### Scenariusz C — „31 miliardów dolarów" (podejście biznesowe)

**Czas:** ~4 minuty
**Ton:** dane → problem → rozwiązanie → ROI → scale

---

#### Hook otwierający (0:00–0:25)

**PREZENTER** *(slajd z jedną liczbą: $31.5B)*:

> „31 i pół miliarda dolarów. Tyle rocznie tracą amerykańskie firmy na nieefektywne dzielenie się wiedzą — dane IDC.
>
> 42 procent wiedzy instytucjonalnej w organizacjach jest posiadane wyłącznie przez jedną osobę. Gdy ta osoba odchodzi, firma potrzebuje 5 do 8 miesięcy, żeby ktoś nowy osiągnął pełną produktywność. Koszt? 33 do 200 procent rocznego wynagrodzenia.
>
> A co gdyby tę wiedzę można było sklonować — nie jako PDF, nie jako wiki, ale jako agenta, któremu możesz zadzwonić i poprosić o konkretną akcję?"

**EKRAN:**
```
$31.5B/rok  — koszt utraconej wiedzy (IDC)
42%         — wiedza u jednej osoby (Panopto)
5-8 mies.   — czas do pełnej produktywności nowego pracownika
87%         — firm raportuje luki kompetencyjne (McKinsey)
```

---

#### Faza 1: Demonstracja na żywym case (0:25–1:45)

**PREZENTER:**

> „Pokażę wam to na przykładzie. Mike Grabowski — CTO Callstack, React Native Core Team, maintainer Re.Pack i CLI. 185 pull requestów, 8 konferencji, dziesiątki wewnętrznych dyskusji. Sklonowaliśmy jego wiedzę w 6 godzin i zamieniliśmy w agenta, do którego można zadzwonić."

*Wyciąga telefon, dzwoni.*

**AGENT-MIKE:**

> „Hej, w czym mogę pomóc?"

**PREZENTER:**

> „Mike, nasz klient ma problem z Module Federation na Hermes — kontenery nie ładują się na Androidzie. Potrzebujemy szybkiego workaround. Co robimy?"

**AGENT-MIKE:**

> „To znany problem — Hermes nie wspiera chunk loadingu przez script tagi. Powiedz klientowi: `chunkLoading: async-node` w webpack configu, włącz `ChunkLoadingPlugin` z flagą experimental. Pełny fix jest w betcie od marca, testuję go z dwoma klientami enterprise. Podeślę ci reference do PR-a."

**EKRAN:** Dashboard z transkrypcją + panelem źródeł (Slack, Jira ticket, PR).

**PREZENTER** *(do publiczności)*:

> „Odpowiedź w 8 sekund. Wcześniej musielibyście czekać aż Mike wróci z urlopu — albo przeszukać 200 ticketów Jira i 50 wątków Slacka. Ale to dopiero rozgrzewka..."

---

#### Faza 2: Wartość biznesowa — hiring pack (1:45–3:15)

**PREZENTER:**

> „Mike, wyobraź sobie, że odchodzisz. Przygotuj mi kompletny pakiet rekrutacyjny na zastępstwo — job description, zadanie techniczne, rubryk oceny."

**AGENT-MIKE:**

> „Jasne. To nie jest standardowa rekrutacja. Potrzebujesz osoby, która rozumie bundler internals od środka — nie 'Senior React Native Developera'. Generuję ci pełny pakiet."

**EKRAN:** Hiring pack generuje się na żywo (jak w scenariuszach A/B). Ale tu prezenter komentuje z perspektywy ROI:

**PREZENTER** *(podczas gdy hiring pack się generuje)*:

> „Zobaczcie co się tu dzieje. Firma bez Gemellus: Mike odchodzi, HR pisze generyczny opis stanowiska, 3 miesiące rekrutacji, 2 miesiące onboardingu, łączny koszt — 150 do 200 procent rocznej pensji.
>
> Z Gemellus: Mike odchodzi, ale jego klon generuje **ultra-precyzyjny** opis stanowiska — nie 'znasz webpacka', ale 'rozumiesz chunk loading runtime i Hermes bytecode pipeline'. Zadanie rekrutacyjne oparte na prawdziwym bugu. Scoring rubric z wagami. To nie jest HR tool — to ekspertowa wiedza zamieniona w proces."

**EKRAN:** Hiring pack w pełni wygenerowany. Obok niego — porównanie:

```
┌─────────────────────┬─────────────────────────┐
│ BEZ GEMELLUS        │ Z GEMELLUS              │
├─────────────────────┼─────────────────────────┤
│ Generic JD          │ Role-specific JD        │
│ "5+ lat RN"         │ "Hermes bytecode        │
│                     │  pipeline + CocoaPods   │
│                     │  Podspec DSL"           │
├─────────────────────┼─────────────────────────┤
│ Zadanie: "Zbuduj    │ Zadanie: "Napraw real   │
│ TODO app w RN"      │ auto-linking bug        │
│                     │ z New Architecture"     │
├─────────────────────┼─────────────────────────┤
│ 3-5 mies. do hire   │ Tydzień do shortlisty   │
│ 5-8 mies. do prod.  │ 2-3 mies. do prod.     │
├─────────────────────┼─────────────────────────┤
│ Koszt: $150-200K    │ Koszt: $50-80K          │
│ (przy $100K salary) │ (60% oszczędności)      │
└─────────────────────┴─────────────────────────┘
```

---

#### Zamknięcie (3:15–4:00)

**PREZENTER:**

> „Gemellus to nie chatbot z ładnym głosem. To platforma, która zamienia wiedzę kluczowych ludzi w konkretne aktywa organizacji — aktywa, które nie odchodzą razem z pracownikiem.
>
> Dla szybko rosnących startupów, które muszą skalować zespoły precyzyjnie. Dla firm tracących seniorów, które nie wiedzą czego właśnie straciły. Dla organizacji, w których HR nie potrafi opisać stanowiska, bo potrzebuje do tego eksperta, który właśnie odszedł.
>
> 87 procent firm ma luki kompetencyjne. Gemellus je identyfikuje i zamienia w plan działania.
>
> **Gemellus** — *turn expertise into organizational assets.*"

**EKRAN:** Logo Gemellus + `gemellus.app`
Statystyki:
```
$31.5B problem → $0 knowledge loss
42% single-person risk → 0% with Gemellus
5-8 months ramp-up → 2-3 months
```

---

#### Scoring Scenariusza C

| Kryterium | Ocena | Uzasadnienie |
|-----------|-------|--------------|
| **Running Code** | 4/5 | Demo działa identycznie, ale prezenter poświęca więcej czasu na mówienie niż na pokaz kodu — jury techniczne może chcieć więcej |
| **Innovation & Creativity** | 4/5 | Podejście ROI-driven jest innowacyjne w kontekście hackathonu (rzadko kto liczy economics), ale mniej „techno-wow" |
| **Real-world Impact** | 5/5 | Najpełniejsze uzasadnienie real-world impact — dane rynkowe, porównanie kosztów, jasny value proposition |
| **Theme Alignment** | 4/5 | Multimodalność widoczna, ale mniej eksponowana — focus na biznesie, nie na architekturze |
| **Łącznie** | **17/20** | |

---

## Rekomendacja: Optymalny scenariusz

### Wariant hybrydowy A+B (rekomendowany)

Najsilniejszy scenariusz łączy **emocjonalny hook** ze Scenariusza A z **transparentnym procesem agenta** ze Scenariusza B:

1. **Hook z A**: „Mike powiedział boardowi: *jestem single point of failure*..." (emocje + kontekst)
2. **Architektura z B**: Pokazanie diagramu i ADK events tab (wiarygodność techniczna)
3. **Rozmowa z A**: Naturalne pytania, głos Mike'a (wow factor)
4. **Hiring pack z B**: Widoczny łańcuch tool calls + generowanie na żywo (proof that it works)
5. **Zamknięcie z A**: Emocjonalne + statystyka „42% wiedzy..." (zapamiętywalne)

**Dane z C** (31,5 mld $, 87% firm) warto mieć na slajdzie **backup** — użyć jeśli jury pyta o business case.

### Kluczowe zasady:
- **Nigdy nie tłumacz co się dzieje** — pokaż i pozwól jury zobaczyć samodzielnie
- **Pauzy są OK** — 2-3 sekundy na odpowiedź agenta budują napięcie, nie tracą uwagi
- **Jedna awaria = koniec** — miej backup nagranie rozmowy, które puścisz jeśli Vapi padnie
- **Hiring pack jest punchline** — nie pokazuj go wcześniej, niech jury zobaczy jak się generuje

---

## Backup: Kluczowe dane o Mike'u do promptu agenta

Gdy agent odpowiada, powinien naturalnie odwoływać się do tych artefaktów:

| Źródło | Konkret |
|--------|---------|
| Slack #repack-dev | Bug `__webpack_require__.l` na Hermes — workaround z `chunkLoading: async-node` |
| Slack #general | „Metro is CRA, Re.Pack is custom webpack config" — 80/20 podział |
| Slack #hiring | Format interview: debugging task (30 min) + design discussion (30 min) + OS scenarios (15 min) |
| Jira CLI-892 | Auto-linking bug z New Architecture — root cause: codegen nie sprawdzał flagi TurboModule |
| Jira CORE-155 | ADR Metro vs Re.Pack — „kluczowy differentiator to ekosystem, nie wydajność" |
| Jira HIRE-301 | Kryteria hiring: bundler internals, native build systems, Hermes, open source maturity |
| 1:1 2025-03-17 | „Single point of failure": Re.Pack runtime, auto-linking, relacje z Meta, release process |
| 1:1 2025-02-10 | „OS work is our best marketing and hiring pipeline" |
| Talk Chain React 2017 | „The Dark Art of Bundlers" — geneza Haul → Re.Pack |
| GitHub Profile | „Passionate about cross platform technologies. When not working, find me on a race track." |
