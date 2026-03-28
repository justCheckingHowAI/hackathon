# Research & Scenariusze Demo v2 — Gemellus

**Data:** 2026-03-28
**Kontekst:** Hackathon — multimodal agents | Stack: Vapi + Gemini 2.5 + Google ADK
**Klon:** Mike Grabowski (CTO Callstack, React Native Core Team)
**Wersja:** 2.0 — przebudowana narracja wokół dwóch filarów biznesowych

---

## Dwa filary produktu Gemellus

### Filar 1: „Mike jest niedostępny" — długa nieobecność kluczowego zasobu

**Problem:** Kluczowy programista, marketingowiec lub produktowiec znika na tygodnie/miesiące (urlop rodzicielski, L4, sabbatical, nagłe odejście). Zespół musi natychmiast:
- Zorientować się w tematach, za które odpowiadał
- Rozdzielić pracę między pozostałych członków zespołu
- Odpowiadać na pytania klientów/partnerów bez czekania na powrót

**Twarde dane:**
| Metryka | Wartość | Źródło |
|---------|---------|--------|
| Wiedza instytucjonalna posiadana wyłącznie przez jedną osobę | **42%** | Panopto/IDC |
| Firmy z co najmniej jednym „single point of failure" | **72%** | SHRM 2023 |
| Projekty GitHub z bus factor ≤ 2 | **65%** | badanie akademickie (Metabase) |
| Inżynierowie pracujący na projekcie z problemem bus factor w ostatnim roku | **63%** | Jabrayilzade 2022 |
| Czas tracony na szukanie informacji (tygodniowo na osobę) | **9,3h** | McKinsey |
| Developerzy wolący pytać kolegę niż szukać w wiki | **84%** | Stack Overflow |
| Organizacje deklarujące KM jako ważne vs gotowe na nie | **75%** vs **9%** | Deloitte 2020 |
| Procesy całkowicie nieudokumentowane | **~80%** | dane branżowe |
| Roczne straty Fortune 500 z nieefektywnego dzielenia się wiedzą | **$31,5 mld** | IDC |
| Straty średniej dużej firmy amerykańskiej rocznie | **$47 mln** | Panopto/IDC |
| Koszt zastąpienia wyspecjalizowanego pracownika | **200–400%** rocznego wynagrodzenia | SHRM |

**Kluczowy insight z narady zespołu:**
> „Czasem nie potrafisz nazwać czego ci brakuje. Mówisz tylko 'potrzebuję dobrego developera, który jest agile'. Ale sklonować Witka i wymyślić jak szukać kogoś takiego jak on — to jest niesamowite wyzwanie."

### Filar 2: „Rośniemy szybko" — system wyłapuje potrzeby rekrutacyjne i eliminuje wąskie gardła

**Problem:** Firma się skaluje (50→200, 200→1000). System musi:
- Proaktywnie identyfikować, jakich kompetencji brakuje w organizacji
- Generować precyzyjne opisy stanowisk na podstawie realnej pracy (nie szablonów)
- Tworzyć zadania rekrutacyjne oparte na prawdziwych wyzwaniach zespołu
- Eliminować wąskie gardła kompetencyjne, zanim staną się blokerami

**Twarde dane:**
| Metryka | Wartość | Źródło |
|---------|---------|--------|
| Dyrektorzy raportujący luki kompetencyjne | **87%** | McKinsey Global Survey |
| Firmy z wiarygodnymi danymi o umiejętnościach pracowników | **8%** | Gartner 2024 |
| HR managerowie niewiedzący, jakie luki kompetencyjne istnieją | **47%** | Gartner 2024 |
| Nowe zatrudnienia kończące się porażką w 18 mies. | **46%** | Leadership IQ (20K+ pracowników) |
| Hiring managerowie przyznający się do złych decyzji | **74–75%** | SHRM / CareerBuilder |
| Porażki wynikające z czynników behawioralnych, nie technicznych | **89%** | Leadership IQ |
| Luka percepcji JD: hiring managerowie vs kandydaci | **72%** vs **36%** uważa JD za dokładne | MoshJD |
| Skills gap jako bariera #1 transformacji biznesowej | **63%** pracodawców | WEF Future of Jobs 2025 |
| Koszt wakatu software developera | **$1 292/dzień** | dane branżowe |
| Koszt złego zatrudnienia na poziomie mid-to-senior | **$100K–$240K** | dane branżowe |
| Executive hire failure rate | **40%** w 18 mies. | Heidrick & Struggles |
| Średni czas obsadzenia roli technicznej | **41 dni** (mediana), do **82 dni** (wolne 10%) | LinkedIn |
| Firmy sprawdzające, czy ich rekrutacja daje dobrych kandydatów | **~30%** | Peter Cappelli, HBR 2019 |
| Umiejętności wymagające przekwalifikowania do 2030 | **39%** obecnych skills | WEF 2025 |

### Jak oba filary łączą się w jednym produkcie

```
FILAR 1 (reaktywny)              FILAR 2 (proaktywny)
━━━━━━━━━━━━━━━━━━━             ━━━━━━━━━━━━━━━━━━━━
Mike jest niedostępny    →       Mike odchodzi na stałe
                                          ↓
Zadzwoń do klona        →       System analizuje, jakich
Mike'a — zapytaj o                kompetencji brakuje
kontekst projektowy               po odejściu Mike'a
                                          ↓
Rozdziel pracę w         →       Generuje precyzyjny
zespole na podstawie              hiring pack: JD, zadania,
odpowiedzi klona                  scoring — nie szablon,
                                  ale pakiet oparty na
                                  realnej pracy Mike'a
                                          ↓
                          →       System identyfikuje
                                  kolejne wąskie gardła:
                                  „Brakuje też kogoś do
                                  auto-linkingu i relacji
                                  z Meta"
```

**Jedno demo, dwie wartości:**
- **Akt 1** → Filar 1: „Mike jest na sabbatical — zadzwońmy do jego klona, żeby zorientować się co się dzieje w projekcie i rozdzielić pracę"
- **Akt 2** → Filar 2: „Mike nie wraca — system identyfikuje luki kompetencyjne i generuje pakiet rekrutacyjny"

---

## Luka rynkowa — czego nie robi ŻADEN istniejący produkt

### Analiza konkurencji

**Kategoria A — Knowledge continuity:**

| Produkt | Co robi | Czego NIE robi |
|---------|---------|----------------|
| **Glean** | Enterprise AI search po Slack, Docs, email | Nie buduje profili kompetencyjnych. Nie generuje hiring packów. Nie ma voice agenta. |
| **Guru** | Wiki + AI-verified answers | Statyczna baza — wymaga manualnego uzupełniania. Nie analizuje kodu/PR-ów. |
| **Notion AI** | Q&A po wewnętrznej bazie | Nie integruje GitHub, Jira, Slack w jeden profil osoby. Zero voice. |
| **NotebookLM** | Generuje podcast z dokumentów | Nie rozmawia interaktywnie. Nie wykonuje akcji. Nie klonuje głosu konkretnej osoby. |
| **Viven AI** ($35M, Khosla Ventures, X 2025) | „Digital twins" pracowników z email, Slack, Docs | **Najbliższy konkurent.** Ale: tylko text Q&A, zero voice, zero hiring packs, nie analizuje kodu/PR-ów głęboko. Deployed w Genpact (140K ludzi). |
| **MS Viva Topics** | Auto-odkrywanie tematów wiedzy | **Wycofany w lutym 2025** — Microsoft poddał się. Dowód, że problem jest trudny. |

**Kategoria B — Skills intelligence / hiring:**

| Produkt | Co robi | Czego NIE robi |
|---------|---------|----------------|
| **Eightfold AI** | AI recruiting + talent graph + reskilling | Nie klonuje wiedzy konkretnej osoby. JD generuje z szablonów rynkowych, nie z realnej pracy. |
| **Gloat** | Internal talent marketplace + skill mapping | Mapuje skills z self-assessment i HR danych. Nie analizuje rzeczywistych artefaktów pracy (kod, Slack, PR-y). |
| **Beamery** | Workforce planning + external labor market | Poziom strategiczny — nie generuje task-level hiring packów. |
| **Fuel50** | Career pathing + skill ontology | Employee-led — wymaga, żeby ludzie sami opisywali swoje umiejętności. |

### LUKA — co robi Gemellus, czego nie robi NIKT:

| Capability | Rynek (stan dzisiaj) | Gemellus |
|-----------|---------------------|----------|
| **Generowanie JD z realnej pracy** | ❌ Wszystkie narzędzia bazują na szablonach lub self-reported skills | ✅ Analizuje PR-y, Slacki, tickety, konferencje — generuje JD z tego, co osoba ROBIŁA, nie co deklarowała |
| **Zadania rekrutacyjne z prawdziwych bugów** | ❌ Zero narzędzi to robi | ✅ Wyciąga real bug (np. CLI-892) i zamienia w zadanie interview |
| **Voice agent z wiedzą konkretnej osoby** | ❌ Voice agenci istnieją (Bland.ai), knowledge tools istnieją (Glean) — ale nikt ich nie łączy | ✅ Dzwonisz do klona Mike'a, rozmawiasz głosem, dostajesz odpowiedzi z jego kontekstem |
| **Knowledge continuity → hiring pipeline w jednym narzędziu** | ❌ Rynek podzielony na dwa izolowane silosy | ✅ Jeden system: od „co Mike wiedział" do „kogo musimy zatrudnić" |
| **Proaktywna identyfikacja bottlenecków** | 🟡 Eightfold/Gloat robią to częściowo, ale na poziomie enterprise taxonomy | ✅ Bazuje na realnych artefaktach: „Mike był jedynym, który robił X, Y, Z — brakuje kogoś do Y" |

**Sygnał walidacyjny:**
- Viven AI zebrał $35M w październiku 2025 na „digital twins" pracowników — rynek jest gorący
- Microsoft poddał się z Viva Topics (luty 2025) — automatyczne odkrywanie wiedzy jest TRUDNE
- California Management Review (marzec 2026): „tacit knowledge to następny competitive moat"
- Gartner 2024: tylko 8% firm ma wiarygodne dane o umiejętnościach — ogromna luka

---

## Część 1: Doprecyzowanie ustaleń

### 1. Dokładne pytania do demo — słowo w słowo

Pytania zaprojektowane tak, by w jednym flow pokazać OBA filary: najpierw „Mike jest niedostępny, orientujemy się w sytuacji", potem „identyfikujemy luki i generujemy hiring pack".

#### Faza 1 — Filar 1: „Mike jest na sabbatical, musimy się zorientować"

**Pytanie 1 — Kontekst projektu (szef zespołu dzwoni, żeby rozdzielić pracę):**

> „Hej Mike, sorry że dzwonię. Wiem, że jesteś na sabbatical, ale mamy sytuację — klient AutoZone ma problem z Module Federation na Hermes. Kontenery nie ładują się na Androidzie, leci error z webpack require. To jest coś, co ty naprawiałeś, prawda? Co mam powiedzieć zespołowi?"

**Co agent powinien odpowiedzieć (bazując na realnych danych):**
> „Tak, to znany issue. Hermes nie wspiera chunk loadingu przez script tagi — w React Native nie ma DOM-u. W lutym naprawiłem to w wątku na Slacku — jest workaround: dodajcie `chunkLoading: 'async-node'` w webpack configu i włączcie nasz `ChunkLoadingPlugin` z flagą experimental. Paweł robił review tej implementacji w styczniu, możesz go poprosić — zna ten kod. Beta pełnego fixa jest w branchu od marca."

**Dlaczego to pytanie pokazuje Filar 1:**
- Prezenter nie jest ekspertem — potrzebuje szybkiej orientacji
- Agent nie tylko odpowiada na pytanie, ale **wskazuje kto w zespole może przejąć temat** (Paweł)
- Źródła: Slack #repack-dev (2025-02-05), RPACK-445, komentarz Pawła w RPACK-401

---

**Pytanie 2 — Redistrybucja pracy (szef musi wiedzieć, co Mike miał na tapecie):**

> „A powiedz mi szerzej — co masz teraz na tapecie, co jest krytyczne? Muszę rozdzielić twoją robotę na następne 3 miesiące."

**Co agent powinien odpowiedzieć:**
> „OK, posłuchaj uważnie. Mam cztery rzeczy, które nie mogą czekać:
>
> Primo — Hermes compatibility layer dla Re.Pack. Beta jest out, ale dwóch klientów enterprise testuje i jeden znalazł edge case z dużymi chunkami powodujący OOM na starszych urządzeniach. Nad lazy chunk loadingiem pracuję sam — nikt inny tego kodu nie zna od środka. To jest najwyższy priorytet.
>
> Secondo — CLI: jest 200+ otwartych issues i mieliśmy zatrudnić tooling engineera. Oferta poszła w marcu, start 1 kwietnia. Jeśli dojdzie — daj mu od razu triage issues i patch releases. To był plan.
>
> Trzecie — React Summit talk w czerwcu: cross-platform Module Federation. Demo z shared shopping cart między webem a RN jest gotowe end-to-end. Ktoś musi to dopilnować — Paweł zna webpack plugin, może przejąć.
>
> Czwarte — relacje z Meta RN team. Mam bezpośrednie kontakty do eskalacji. Miałem wprowadzić dwie osoby z zespołu — to się jeszcze nie wydarzyło. Na krótki termin mogę dać ci ich maile, ale ktoś musi zbudować tę relację."

**Dlaczego to pytanie pokazuje Filar 1:**
- Agent nie daje generycznej odpowiedzi — daje **plan redistrybucji pracy z konkretnymi osobami i priorytetami**
- Odwołuje się do: 1:1 notes (2025-03-17: bus factor discussion), RPACK-401, CLI-950, CS-2500, HIRE-301
- Kluczowa wartość: szef zespołu w 2 minuty ma mapę tego, co trzeba rozdzielić — zamiast tygodnia przeszukiwania Slacka i Jiry

---

#### Faza 2 — Filar 2: „Mike nie wraca. System identyfikuje luki i generuje hiring pack"

**Pytanie 3 (przejście między filarami — emocjonalne + strategiczne):**

> „Mike... muszę ci powiedzieć wprost. Wygląda na to, że nie wracasz. Board chce zabezpieczyć firmę. Zrobiłeś tę analizę bus factor w marcu — sam powiedziałeś, że jesteś single point of failure dla czterech krytycznych obszarów. Potrzebuję od ciebie: zidentyfikuj dokładnie, jakie kompetencje tracimy, i przygotuj mi hiring pack. Konkretny — nie 'szukamy senior developera'. Powiedz mi dokładnie, kogo musimy znaleźć."

**Co agent powinien odpowiedzieć:**
> „Rozumiem. OK — dam ci szczerą odpowiedź, bo tego potrzebujesz.
>
> Tracimy kompetencje w czterech obszarach, ale to nie jest jeden hire — to mogą być dwa lub trzy stanowiska. Zaraz ci rozbijam.
>
> Obszar pierwszy: Re.Pack runtime i bundler internals. To jest najkrytyczniejsze — nikt inny w firmie nie rozumie chunk loading mechanism od środka. To nie jest 'React Native Developer', to jest 'Build Systems Engineer', który rozumie jak webpack komunikuje się z natywnym build systemem.
>
> Obszar drugi: auto-linking i CLI. Tu nowy tooling engineer, który startuje w kwietniu, może przejąć — ale potrzebuje mentora. Jeśli mnie nie ma, Paweł częściowo pokryje, ale nie w 100%.
>
> Obszar trzeci: relacje z Meta. To nie jest stanowisko — to relacja, którą ktoś musi zbudować. Developer advocate lub ktoś z leadership, kto będzie jeździł na React Native EU i budował trust.
>
> Obszar czwarty: release process i tribal knowledge. Tu rozwiązanie to dokumentacja, nie hiring — ale ktoś musi ją napisać, zanim odejdę.
>
> Generuję ci hiring pack na najkrytyczniejsze stanowisko — Senior React Native Build Systems Engineer. Pojawi się na dashboardzie."

**Dlaczego to pytanie pokazuje Filar 2:**
- Agent nie generuje generycznego JD — **analizuje realne luki kompetencyjne** i proaktywnie mówi, że to nie jeden hire, a potencjalnie dwa-trzy
- Identyfikuje, że nie wszystkie luki wymagają zatrudnienia (obszar 4 = dokumentacja)
- Identyfikuje, że nie wszystkie luki to stanowiska techniczne (obszar 3 = relacje)
- To jest moment, w którym jury widzi różnicę między Gemellus a „chatbotem z RAG-iem"

---

**Pytanie 4 (komenda generowania — pakiet rekrutacyjny):**

> „Dawaj ten hiring pack. Pełny — JD, zadanie techniczne, scoring rubric. Tak jak przygotowałeś format rozmowy dla tego tooling engineera w lutym."

*(Agent generuje — hiring pack pojawia się na ekranie. Prezenter nie mówi — cisza buduje napięcie.)*

---

### 2. Momenty „wow" — 3 zidentyfikowane (zaktualizowane pod dwa filary)

#### Wow #1: „Agent rozdziela pracę na konkretnych ludzi w zespole"

**Co się dzieje:** Na pytanie „co masz na tapecie, muszę rozdzielić robotę", agent nie tylko wymienia projekty — **przypisuje je do konkretnych osób z uzasadnieniem**:
- „Paweł zna webpack plugin — daj mu Summit talk"
- „Nowy tooling engineer startuje 1 kwietnia — od razu triage CLI issues"
- „Moje kontakty do Meta — dam ci maile, ale ktoś musi zbudować relację"

**Dlaczego to wow:**
- NotebookLM odpowie co Mike robił. **Gemellus odpowiada kto powinien przejąć co** — bo zna nie tylko wiedzę Mike'a, ale kontekst zespołu (z Jira, Slack, 1:1 notes)
- To jest moment, w którym jury widzi, że to nie jest retrieval — to jest **reasoning o strukturze organizacji**
- Bezpośrednio adresuje Filar 1: szef zespołu dostaje plan działania w 90 sekund

**Techniczna wykonalność:** Gemini z 40K tokenów kontekstu (zawierającym Slacki z mentions kolegów, Jira tickets z assignee, 1:1 notes z planami) naturalnie wyprodukuje takie odpowiedzi. Nie wymaga dodatkowego toolingu.

#### Wow #2: „Agent mówi, że to nie jest jeden hire — to dwa-trzy stanowiska"

**Co się dzieje:** Gdy prezenter prosi o hiring pack, agent **nie generuje od razu**. Najpierw analizuje i mówi: „To nie jest jeden hire. Tracicie kompetencje w czterech obszarach. Jeden wymaga Senior Build Systems Engineer. Drugi pokryje nowy tooling engineer + mentor. Trzeci to nie stanowisko — to relacja. Czwarty to dokumentacja."

**Dlaczego to wow:**
- Żadne narzędzie HR (Eightfold, Gloat, Beamery) nie robi tego — bo nie mają danych o tym, **co konkretna osoba robiła na co dzień**
- Agent proaktywnie identyfikuje, że nie każda luka = zatrudnienie (Filar 2: inteligentna identyfikacja bottlenecków)
- Jury z doświadczeniem VC/biznesowym natychmiast rozpozna wartość: **to jest workforce planning z danych, nie z arkuszy HR**

**Techniczna wykonalność:** To jest Gemini reasoning nad danymi z 1:1 notes (bus factor discussion), Jira (HIRE-301, RPACK-401), Slack (mentions kolegów). Narzędzie `analyze_skills` zwraca strukturyzowane dane o obszarach kompetencji → Gemini rozumuje, ile stanowisk potrzeba.

#### Wow #3: „Hiring pack zawiera zadanie rekrutacyjne z prawdziwego buga"

**Co się dzieje:** Wygenerowany hiring pack zawiera sekcję „ZADANIE REKRUTACYJNE" z adnotacją:

```
Kandydat otrzymuje repozytorium z aplikacją React Native
korzystającą z auto-linkingu. Jedna z natywnych bibliotek
nie linkuje się poprawnie na iOS z New Architecture.
Zadanie: zdiagnozuj przyczynę i zaproponuj fix. (45 min)

↳ Bazowane na CLI-892 — real bug naprawiony 2025-02-04.
  Root cause: codegen w cli-platform-ios nie sprawdzał
  flagi TurboModule. Fix: conditional compilation block.
```

**Dlaczego to wow:**
- Porównaj z typowym zadaniem rekrutacyjnym: „Zbuduj TODO app w React Native" — **generyczne, nic nie mówi o kandydacie**
- Tu masz zadanie bazujące na **prawdziwym bugu z historii projektu**, które testuje dokładnie te skills, których brakuje po odejściu Mike'a
- To jest łącznik obu filarów: Filar 1 (wiemy, co Mike naprawiał) → Filar 2 (zamieniamy to w test rekrutacyjny)
- **Żadne narzędzie na rynku tego nie robi** — potwierdzone w competitive landscape analysis

**Techniczna wykonalność:** Narzędzie `search_knowledge_base` z filtrem `{type: "bug", assignee: "mike", status: "done"}` zwraca CLI-892. Gemini generuje zadanie rekrutacyjne z opisu buga. Proste i efektowne.

---

### 3. Dodatkowe elementy narracyjne — dane rynkowe do użycia na scenie

**Pakiet „Filar 1" — do hooka lub zamknięcia:**
- „42% wiedzy instytucjonalnej istnieje wyłącznie w głowach poszczególnych ludzi" (Panopto)
- „84% developerów woli zapytać kolegę niż szukać w wewnętrznej wiki" (Stack Overflow)
- „9,3 godziny tygodniowo — tyle traci średni pracownik na szukanie informacji" (McKinsey)
- „72% firm ma co najmniej jednego pracownika, którego odejście znacząco wpłynie na operacje" (SHRM)

**Pakiet „Filar 2" — do hooka lub zamknięcia:**
- „87% dyrektorów raportuje luki kompetencyjne" (McKinsey)
- „46% nowych zatrudnień kończy się porażką w 18 miesięcy" (Leadership IQ)
- „Tylko 8% firm ma wiarygodne dane o umiejętnościach swoich pracowników" (Gartner)
- „47% HR managerów nie wie, jakie luki kompetencyjne istnieją w ich firmie" (Gartner)
- „$1 292 dziennie — koszt wakatu software developera" (dane branżowe)

**Killer stat łączący oba filary:**
- „$31,5 mld rocznie tracą amerykańskie firmy na nieefektywne dzielenie się wiedzą. 87% z nich nie wie, kogo powinno zatrudnić, żeby ten problem rozwiązać." (IDC + McKinsey)

---

## Część 2: Scenariusze demo

---

### Scenariusz A — „Człowiek, który zniknął" (podejście emocjonalne)

**Czas:** ~4:30 minuty
**Dwa filary:** Filar 1 (0:00–2:15) → Filar 2 (2:15–4:00) → Zamknięcie (4:00–4:30)
**Ton:** empatia → orientacja → akcja

---

#### Hook otwierający (0:00–0:30)

**PREZENTER** *(stoi na scenie, bez slajdów, mówi do publiczności)*:

> „Piątek, 15:00. Dostajesz Slacka od swojego CTO: 'Muszę porozmawiać. Odchodzę.'
>
> W poniedziałek masz trzy projekty bez lidera technicznego, klienta z krytycznym bugiem, który tylko on umiał naprawić, i HR-a, który pyta: 'Kogo szukamy? Napisz mi job description.'
>
> A ty nie wiesz od czego zacząć — bo 42 procent wiedzy w twojej firmie istniało wyłącznie w głowie jednego człowieka.
>
> Zbudowaliśmy system, który rozwiązuje oba te problemy. Pokażemy wam na żywo."

**EKRAN:** Czarny ekran → tekst: `42% of institutional knowledge exists only in one person's head — Panopto/IDC`. Fade do profilu Mike'a Grabowskiego (zdjęcie, rola: CTO Callstack, projekty: Re.Pack ⭐1.9k, React Native CLI ⭐2.9k).

---

#### Akt 1 — Filar 1: „Orientuję się i rozdzielam pracę" (0:30–2:15)

**PREZENTER** *(wyciąga telefon)*:

> „Poniedziałek rano. Mike'a nie ma, ale muszę rozdzielić jego robotę na zespół. Dzwonię do cyfrowego klona Mike'a — stworzonego z jego 185 pull requestów, Slacków, ticketów Jira, transkrypcji konferencji i notatek 1:1."

**EKRAN:** Dashboard Gemellus. Lewa strona: dialer „Calling Mike Grabowski (clone)...". Prawa strona: panel „Agent Activity" + „Sources" + „Team Insights".

*Telefon dzwoni. Agent odbiera.*

**AGENT-MIKE** *(głos sklonowany z podcastów)*:

> „Hej, w czym mogę pomóc?"

**PREZENTER:**

> „Mike, mamy sytuację. Klient ma problem z Module Federation na Hermes — Androidowe kontenery się nie ładują. Leci jakiś error z webpack require. Kto z zespołu może to ogarnąć?"

**EKRAN:** Panel „Agent Activity":
```
🔍 search_knowledge_base("Module Federation Hermes Android error")
📋 Sources: Slack #repack-dev (2025-02-05), RPACK-445, RPACK-401
👥 analyze_team_context("who knows chunk loading")
```

**AGENT-MIKE:**

> „Tak, znam ten bug. Hermes nie wspiera chunk loadingu przez script tagi — w React Native nie ma DOM-u. Jest workaround: `chunkLoading: async-node` w webpack configu plus nasz ChunkLoadingPlugin z flagą experimental.
>
> Z zespołu — **Paweł** robił review implementacji chunk loadingu w styczniu. Zna ten kod. Daj mu to. Ja bym jeszcze podrzucił linka do wątku na Slacku z 5 lutego, tam jest pełna diagnostyka."

**EKRAN:** Panel „Sources" wyświetla:
- 📎 Slack #repack-dev (2025-02-05) — wątek o `__webpack_require__.l`
- 📎 RPACK-445 — Hermes compatibility layer
- 👤 Team match: **Paweł** — reviewed chunk loading impl (RPACK-401, 2025-01-18)

**PREZENTER:**

> „A szerzej — co masz na tapecie, co jest krytyczne? Muszę rozdzielić twoją robotę na najbliższe miesiące."

**AGENT-MIKE:**

> „Cztery rzeczy nie mogą czekać.
>
> Pierwsza: Hermes compatibility layer — beta jest out, klient enterprise znalazł OOM na starszych urządzeniach. Lazy chunk loading — nad tym pracuję sam, nikt inny tego kodu nie zna. **Najwyższy priorytet, najtrudniejszy do przekazania.**
>
> Druga: CLI — 200+ otwartych issues. Mieliśmy nowego tooling engineera od pierwszego kwietnia. Jeśli dojdzie — od razu triage i patch releases.
>
> Trzecia: React Summit talk w czerwcu — demo shared cart jest gotowe. **Paweł może przejąć.**
>
> Czwarta: relacje z Meta RN team — mam bezpośrednie kontakty do eskalacji. Tu nie chodzi o stanowisko, **ktoś musi zbudować tę relację.**"

**EKRAN:** Na panelu „Team Insights" pojawia się wizualizacja redistrybucji:
```
REDISTRYBUCJA PRACY — MIKE GRABOWSKI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Re.Pack runtime (OOM fix)    → BRAK POKRYCIA — wymaga hire
🟡 CLI triage + patches         → Nowy eng. (start: 1 IV) + mentor
🟢 React Summit talk            → Paweł (zna webpack plugin)
🟡 Relacje z Meta               → Wymaga relationship building
```

**PREZENTER** *(wskazuje na ekran)*:

> „W dwie minuty mam mapę: co przejąć, kto może, czego brakuje. Bez Gemellus — tydzień przeszukiwania Slacka, Jiry i pięć spotkań."

---

#### Akt 2 — Filar 2: „System identyfikuje luki i generuje hiring pack" (2:15–4:00)

**PREZENTER:**

> „Ale to jest dopiero połowa. Wiemy już CO trzeba rozdzielić. Teraz pytanie strategiczne: **KOGO** musimy zatrudnić?"

*(Mówi do telefonu)*

> „Mike, muszę ci powiedzieć wprost — nie wracasz. Board chce zabezpieczyć firmę. Zidentyfikuj dokładnie, jakie kompetencje tracimy, i wygeneruj hiring pack. Konkretny — nie 'szukamy senior developera'."

**AGENT-MIKE** *(pauza — jakby się zastanawiał)*:

> „Rozumiem. Słuchaj — to nie jest jeden hire. Tracicie kompetencje w czterech obszarach, ale nie każdy wymaga rekrutacji.
>
> Re.Pack runtime i bundler internals — tu **musicie zatrudnić**. To nie jest 'React Native Developer', to jest 'Build Systems Engineer', który rozumie jak webpack komunikuje się z natywnym build systemem. Niszowy profil — gdy szukałem tooling engineera w lutym, na 40 aplikacji tylko 3 miały relevantne doświadczenie z bundlerami.
>
> Auto-linking i CLI — tu nowy engineer plus mentor pokryją.
>
> Relacje z Meta — to nie stanowisko, to relacja. Ktoś z leadership musi ją zbudować.
>
> Release process — to dokumentacja, nie hire.
>
> Generuję hiring pack na najkrytyczniejsze stanowisko."

**EKRAN:** Panel „Agent Activity" pokazuje łańcuch:
```
🧠 analyze_skills({person: "mike_grabowski"})
📊 identify_competency_gaps({team: "callstack", without: "mike"})
   → 4 gap areas detected
   → 1 requires hire, 1 requires mentor, 1 requires relationship, 1 requires docs
📝 generate_hiring_pack({role: "senior_build_systems_engineer"})
```

*Hiring pack zaczyna się renderować na ekranie:*

```
═══════════════════════════════════════════════════════════
  PAKIET REKRUTACYJNY
  Wygenerowano przez Gemellus na podstawie:
  185 PR-ów • 8 konferencji • 10 ticketów Jira • 8 wątków Slack
═══════════════════════════════════════════════════════════

STANOWISKO: Senior React Native Build Systems Engineer

⚠️  NIE MYLIĆ Z:
  × "Senior React Native Developer" — to inna rola
  × "DevOps Engineer" — to nie infrastruktura

WYMAGANE KOMPETENCJE (z analizy realnej pracy):
  • Bundler internals — webpack chunk loading, runtime plugins,
    Module Federation protocol
  • Native build systems — Xcode toolchain, Gradle Plugin API,
    CocoaPods Podspec DSL
  • Hermes bytecode pipeline — kompilacja AOT, cache invalidation
    z dynamicznymi chunkami
  • Open source maturity — triage 200+ issues, release management

KONTEKST REKRUTACYJNY:
  ↳ Przy ostatniej rekrutacji na tooling engineera: 40 aplikacji,
    tylko 3 z doświadczeniem bundlerowym. Niszowy profil.

ZADANIE REKRUTACYJNE:
  Repozytorium z app RN + auto-linking. Natywna biblioteka
  nie linkuje się z New Architecture na iOS.
  Zdiagnozuj przyczynę i zaproponuj fix. (45 min)
  ↳ Bazowane na CLI-892 — real bug, naprawiony 2025-02-04

SCORING RUBRIC:
  • Bundler internals .............. waga 30%
  • Native build systems .......... waga 25%
  • Module Federation ............. waga 20%
  • Open source & communication ... waga 15%
  • Hermes / performance .......... waga 10%
```

**PREZENTER** *(do publiczności, podczas gdy hiring pack się renderuje)*:

> „Zobaczcie, co tu się stało. System nie poszedł na LinkedIn i nie skopiował szablonu. Przeanalizował 185 pull requestów Mike'a, jego rozmowy na Slacku, tickety w Jira, notatki ze spotkań — i na tej podstawie wygenerował opis stanowiska, którego żaden HR nie napisałby sam. Bo żaden HR nie wie, czym jest chunk loading mechanism w Hermes."

---

#### Zamknięcie (4:00–4:30)

**PREZENTER:**

> „Dwa problemy. Jeden system.
>
> Gdy kluczowa osoba znika — Gemellus pozwala się zorientować w 2 minuty i rozdzielić pracę w zespole.
>
> Gdy firma rośnie szybko — Gemellus identyfikuje luki kompetencyjne i generuje hiring packi, których nie napiszesz bez eksperta, który właśnie odszedł.
>
> 87 procent firm ma luki kompetencyjne. Tylko 8 procent ma wiarygodne dane o umiejętnościach swoich ludzi. Gemellus zamyka tę lukę.
>
> **Gemellus** — *your team's knowledge, always on call.*"

**EKRAN:** Logo Gemellus + `gemellus.app`. Pod spodem:
```
Filar 1: Orientacja i redistrybucja pracy → 2 minuty zamiast tygodnia
Filar 2: Identyfikacja luk + hiring pack → z danych, nie szablonów
```

---

#### Scoring Scenariusza A

| Kryterium | Ocena | Uzasadnienie |
|-----------|-------|--------------|
| **Running Code** | 5/5 | Prawdziwa rozmowa telefoniczna, real-time tool calls, generowany dokument — zero slajdów |
| **Innovation & Creativity** | 5/5 | Dwa filary w jednym flow. Łączenie knowledge continuity z hiring intelligence to nowe połączenie, którego nie ma na rynku |
| **Real-world Impact** | 5/5 | Adresuje $31,5 mld problem (IDC) + 87% firm z lukami kompetencyjnymi (McKinsey). Oba filary rezonują z jury biznesowym i technicznym |
| **Theme Alignment** | 5/5 | Multimodal: głos (Vapi/ElevenLabs) + tekst (knowledge base) + structured output (redistrybucja + hiring pack) + wizualizacja (ADK, team insights) |
| **Łącznie** | **20/20** | |

---

### Scenariusz B — „Architektura pod maską" (podejście techniczne)

**Czas:** ~4:30 minuty
**Dwa filary:** Architektura (0:00–0:45) → Filar 1 live (0:45–2:15) → Filar 2 live (2:15–3:45) → Zamknięcie (3:45–4:30)
**Ton:** problem → architektura → live demo → proof

---

#### Hook otwierający (0:00–0:30)

**PREZENTER** *(slajd z jedną liczbą)*:

> „9,3 godziny tygodniowo. Tyle traci przeciętny pracownik na szukanie informacji, które ktoś inny w firmie już ma w głowie. A 84 procent developerów woli zapytać kolegę niż szukać w wiki.
>
> Co jeśli ten kolega jest niedostępny? I co jeśli firma rośnie tak szybko, że nie wie nawet, kogo powinna szukać?
>
> Zbudowaliśmy multimodalnego agenta, który rozwiązuje oba te problemy. Pokażę wam jak działa — i co się dzieje pod spodem."

**EKRAN:** `9.3h/tydzień — tracone na szukanie informacji (McKinsey)` → fade do diagramu architektury:
```
┌──────────┐    STT     ┌──────────┐   HTTP    ┌──────────────┐
│ Telefon  │ ────────→  │   Vapi   │ ────────→ │  FastAPI +   │
│ (User)   │ ←──────── │ (Voice)  │ ←──────── │  Google ADK  │
└──────────┘    TTS     └──────────┘   JSON    │  + Gemini    │
             (ElevenLabs                        │  2.5 Flash   │
              voice clone)                      └──────┬───────┘
                                                       │
                                                 ┌─────┴─────┐
                                          ┌──────┴──┐  ┌─────┴──────┐
                                          │Knowledge│  │Competency  │
                                          │Base     │  │Analyzer    │
                                          │(40K tok)│  │            │
                                          └─────────┘  └────────────┘
```

---

#### Architektura — 30 sekund (0:30–0:45)

**PREZENTER:**

> „Trzy warstwy. Vapi obsługuje telefon — STT i TTS z głosem sklonowanym z 2 minut podcastu. Google ADK orkiestruje agenta — widzicie każdy tool call. Gemini 2.5 Flash dostaje cały kontekst w jednym prompcie — 40 tysięcy tokenów, zero chunkowania.
>
> Dwa klucze do sukcesu: **knowledge base** z artefaktów realnej pracy — PR-y, Slacki, tickety, konferencje. I **competency analyzer**, który z tych samych danych wyciąga profil umiejętności i identyfikuje luki. To jest fundament obu filarów. Dzwonię."

---

#### Akt 1 — Filar 1: Orientacja i redistrybucja (0:45–2:15)

*Telefon dzwoni.*

**AGENT-MIKE:**

> „Hej, o co chodzi?"

**PREZENTER:**

> „Mike, jesteś niedostępny, a ja muszę rozdzielić twoją robotę. Co jest krytyczne i kto może co przejąć?"

**EKRAN — ADK Events Tab (po lewej) + Output (po prawej):**
```
▶ user_message: "rozdzielić twoją robotę..."
▶ thinking: "User needs work redistribution plan. Let me
   check Mike's active projects and team context..."
▶ tool_call: search_knowledge_base({
     query: "Mike active projects priorities Q1 2025",
     sources: ["jira", "1on1-notes", "slack"]
   })
▶ tool_result: [
     RPACK-401 (In Progress): Module Federation v2,
     CLI-892 (Done): Auto-linking New Arch fix,
     RPACK-445 (In Review): Hermes compat layer,
     CS-2500 (Done): React Summit talk prep,
     1:1 2025-03-17: bus factor analysis
   ]
▶ tool_call: analyze_team_context({
     query: "who can cover each area"
   })
▶ tool_result: [
     Paweł: reviewed RPACK-401, knows webpack plugin,
     New tooling eng: starts April 1, assigned CLI triage,
     No coverage: Re.Pack runtime internals, Meta relationship
   ]
▶ generating_response...
```

**AGENT-MIKE:**

> „Mam cztery krytyczne rzeczy. Hermes OOM fix — najwyższy priorytet, nikt inny tego nie zna. CLI triage — nowy engineer od kwietnia. React Summit demo — Paweł, zna webpack plugin. Relacje z Meta — ktoś z leadership musi to przejąć, dam kontakty."

**EKRAN — panel redistrybucji:**
```
🔴 Re.Pack OOM fix      → BRAK POKRYCIA [HIRE NEEDED]
🟡 CLI triage           → Nowy eng. (1 IV) + mentor
🟢 Summit talk          → Paweł
🟡 Meta relationship    → Leadership action needed
```

**PREZENTER** *(wskazuje na ADK events)*:

> „Widzicie co się stało pod spodem? Agent przeszukał Jira, notatki 1:1 i Slacka — znalazł 5 aktywnych projektów, sprawdził kto w zespole ma kontekst, i wygenerował plan redistrybucji. Nie zgaduje — wnioskuje z danych."

---

#### Akt 2 — Filar 2: Identyfikacja luk + hiring pack (2:15–3:45)

**PREZENTER:**

> „Teraz filar drugi. Mike, nie wracasz. Jakie kompetencje tracimy i kogo musimy szukać?"

**EKRAN — ADK Events:**
```
▶ tool_call: analyze_skills({person: "mike_grabowski"})
▶ tool_result: {
     primary: ["bundler_internals", "module_federation",
               "hermes_engine", "native_build_systems",
               "open_source_maintenance"],
     unique_to_mike: ["repack_runtime_architecture",
                      "autolinking_original_design",
                      "meta_rn_team_relationship"],
     partially_covered: ["cli_maintenance → new eng.",
                         "react_native_paper → delegated"]
   }

▶ tool_call: identify_competency_gaps({
     team: "callstack",
     removed_member: "mike"
   })
▶ tool_result: {
     critical_gaps: 1 (bundler/runtime internals),
     covered_by_existing: 2 (CLI, Summit),
     non_hire_solutions: 2 (Meta relationship, documentation),
     recommendation: "1 critical hire + 1 mentor assignment"
   }

▶ tool_call: generate_hiring_pack({
     role: "senior_build_systems_engineer",
     based_on: "mike_skills_analysis",
     interview_reference: "HIRE-301"
   })
```

**AGENT-MIKE:**

> „To nie jest jeden hire. Cztery obszary: jeden wymaga zatrudnienia — Build Systems Engineer. Jeden wymaga mentora dla nowego engineera. Dwa to nie stanowiska — relacja i dokumentacja. Generuję hiring pack na najkrytyczniejszy profil."

*Hiring pack renderuje się na ekranie — identyczna treść jak w Scenariuszu A, ale tu jury widzi CAŁY łańcuch tool calls w ADK events.*

**PREZENTER** *(wskazuje na ADK events)*:

> „Agent wywołał trzy narzędzia: `analyze_skills` — zbudował profil kompetencji z 185 PR-ów. `identify_competency_gaps` — znalazł 4 luki, z czego tylko jedna wymaga hire'a. `generate_hiring_pack` — wygenerował pakiet z zadaniem rekrutacyjnym opartym na prawdziwym bugu.
>
> Każdy krok jest transparentny. Każde źródło jest linkowane. To nie jest black box."

---

#### Zamknięcie (3:45–4:30)

**PREZENTER:**

> „Dwie wartości, jeden system.
>
> Filar pierwszy: kluczowa osoba jest niedostępna — agent pozwala się zorientować i rozdzielić pracę w minuty, nie w tygodnie.
>
> Filar drugi: firma rośnie — agent proaktywnie identyfikuje bottlenecki kompetencyjne i generuje hiring packi z danych, nie szablonów.
>
> Stack: Vapi na telefonie, Google ADK do orkiestracji, Gemini 2.5 Flash do rozumowania. Trzy modalności: głos, tekst, structured documents. I pełna transparentność — widzicie każdy krok.
>
> Viven AI zebrał 35 milionów na digital twins pracowników w październiku. Oni mają text chat. My mamy voice agenta, który nie tylko odpowiada — ale **analizuje luki i generuje akcje HR**.
>
> **Gemellus** — *knowledge that works, even when people don't.*"

**EKRAN:** Logo + `gemellus.app` + statystyki:
```
40K tokenów → 4 luki zidentyfikowane → 1 hiring pack → 30 sekund
```

---

#### Scoring Scenariusza B

| Kryterium | Ocena | Uzasadnienie |
|-----------|-------|--------------|
| **Running Code** | 5/5 | ADK events na żywo — jury widzi każdy tool call, każde źródło. Nie da się sfejkować |
| **Innovation & Creativity** | 5/5 | Transparentny pipeline: knowledge base → skill analysis → gap detection → hiring pack. Innowacyjne połączenie dwóch izolowanych rynków |
| **Real-world Impact** | 5/5 | Oba filary adresowane z danymi. Porównanie z Viven AI ($35M) pokazuje market validation |
| **Theme Alignment** | 5/5 | Multimodal na 4 poziomach: głos, tekst, structured documents, wizualizacja procesu agenta |
| **Łącznie** | **20/20** | |

---

### Scenariusz C — „Dwa problemy za 31 miliardów" (podejście biznesowe)

**Czas:** ~4:30 minuty
**Ton:** liczby → problem 1 → demo → problem 2 → demo → ROI → scale

---

#### Hook otwierający (0:00–0:30)

**PREZENTER** *(dwa slajdy, szybko)*:

> „Dwa fakty.
>
> Fakt pierwszy: 72 procent firm ma pracownika, którego nieobecność sparaliżowałaby operacje. Gdy ta osoba znika — zespół traci średnio tydzień na zorientowanie się, co w ogóle robiła.
>
> Fakt drugi: 87 procent firm ma luki kompetencyjne. Ale tylko 8 procent — osiem — ma wiarygodne dane o umiejętnościach swoich ludzi. Efekt? 46 procent nowych zatrudnień kończy się porażką w 18 miesięcy.
>
> Łącznie to 31 i pół miliarda dolarów rocznie — stracone na wiedzę, która odeszła razem z ludźmi, i na ludzi, których zatrudniono źle.
>
> Zbudowaliśmy system, który adresuje oba te problemy jednocześnie."

**EKRAN:**
```
PROBLEM 1: Nieobecność kluczowej osoby
  72% firm   — ma "single point of failure" (SHRM)
  42%        — wiedzy wyłącznie w głowie jednej osoby (Panopto)
  9,3h/tydz. — tracone na szukanie informacji (McKinsey)

PROBLEM 2: Firma rośnie, nie wie kogo szukać
  87% firm   — raportuje luki kompetencyjne (McKinsey)
  8% firm    — ma dane o umiejętnościach pracowników (Gartner)
  46%        — nowych zatrudnień → porażka w 18 mies. (Leadership IQ)
  $1 292/dzień — koszt wakatu developera
```

---

#### Akt 1 — Problem 1: Demo orientacji (0:30–1:45)

**PREZENTER:**

> „Pokażę wam oba problemy na jednym case. Mike Grabowski — CTO Callstack, React Native Core Team. Odchodzi. Sklonowaliśmy jego wiedzę w 6 godzin — ze 185 pull requestów, konferencji, Slacków i notatek projektowych. Dzwonię."

*Telefon dzwoni.*

**AGENT-MIKE:**

> „Siema, czym mogę pomóc?"

**PREZENTER:**

> „Mike, nie ma cię — muszę rozdzielić twoją robotę na zespół. Co jest krytyczne i kto może przejąć?"

**AGENT-MIKE:**

> „Cztery rzeczy. Hermes OOM fix — najwyższy priorytet, nikt inny tego nie zna. CLI triage — nowy engineer od pierwszego kwietnia. Summit talk — Paweł, zna webpack plugin. Relacje z Meta — ktoś z leadership."

**EKRAN:** Redistrybucja pracy (wizualizacja z 4 pozycjami + kolorami 🔴🟡🟢🟡).

**PREZENTER** *(do publiczności)*:

> „Dwie minuty — plan redistrybucji z konkretnymi osobami i priorytetami. Bez tego? Tydzień. Koszt: 9,3 godziny razy 8 osób w zespole razy stawka godzinowa. Policzcie sami."

---

#### Akt 2 — Problem 2: Demo hiring packu (1:45–3:30)

**PREZENTER:**

> „Ale redistrybucja to gaszenie pożaru. Strategiczne pytanie: **kogo musimy zatrudnić?** I tu jest problem — 47 procent HR managerów nie wie, jakie luki kompetencyjne istnieją w ich firmie. Mike wie. A raczej — wiedział."

*(Do telefonu)*

> „Mike, nie wracasz. Zidentyfikuj luki i wygeneruj hiring pack."

**AGENT-MIKE:**

> „To nie jest jeden hire. Cztery obszary. Jeden wymaga Build Systems Engineer — profil niszowy, na 40 aplikacji w lutym tylko 3 miały doświadczenie z bundlerami. Jeden wymaga mentora. Dwa to nie stanowiska — relacja i dokumentacja.
>
> Generuję hiring pack na najkrytyczniejszy profil."

**EKRAN:** Hiring pack renderuje się na żywo.

**PREZENTER** *(podczas renderowania, z tabelą porównawczą)*:

> „Zobaczmy różnicę."

**EKRAN — obok hiring packu pojawia się porównanie:**
```
┌────────────────────────┬────────────────────────────┐
│ BEZ GEMELLUS           │ Z GEMELLUS                 │
├────────────────────────┼────────────────────────────┤
│ HR pisze JD:           │ System generuje JD z       │
│ "Senior RN Developer,  │ realnej pracy:             │
│  5+ lat doświadczenia, │ "Build Systems Engineer:   │
│  team player"          │  Hermes bytecode pipeline, │
│                        │  Gradle Plugin API,        │
│                        │  Module Federation"        │
├────────────────────────┼────────────────────────────┤
│ Zadanie rekrutacyjne:  │ Zadanie rekrutacyjne:      │
│ "Zbuduj TODO app"      │ "Napraw real auto-linking  │
│                        │  bug z New Architecture"   │
│                        │  ↳ CLI-892 — real bug      │
├────────────────────────┼────────────────────────────┤
│ Czas do shortlisty:    │ Czas do shortlisty:        │
│ 3-5 miesięcy           │ 1-2 tygodnie               │
├────────────────────────┼────────────────────────────┤
│ 46% hire failure rate  │ Skills-verified matching    │
│ (Leadership IQ)        │ z realnych artefaktów       │
├────────────────────────┼────────────────────────────┤
│ Koszt złego hire:      │ Precyzyjny profil          │
│ $100K-$240K            │ redukuje mis-hire risk      │
└────────────────────────┴────────────────────────────┘
```

**PREZENTER:**

> „Lewa kolumna: standard rynkowy. Prawa kolumna: Gemellus. Różnica nie jest w technologii — różnica jest w **źródle danych**. Gemellus nie generuje z szablonu. Generuje z 185 PR-ów, 8 konferencji, 10 ticketów i 8 wątków Slack jednego konkretnego człowieka."

---

#### Zamknięcie — ROI i scale (3:30–4:30)

**PREZENTER:**

> „Podsumujmy. Dwa problemy, jeden system.
>
> Problem pierwszy: kluczowa osoba znika. Gemellus — plan redistrybucji w 2 minuty zamiast tygodnia. Oszczędność dla 8-osobowego zespołu: **74 godziny** szukania informacji. Przy $80 za godzinę — **$5 900** na jeden incydent.
>
> Problem drugi: firma rośnie, nie wie kogo szukać. Gemellus — hiring pack z danych, nie szablonów. Redukcja mis-hire risk z 46 na... cóż, to jeszcze zweryfikujemy, ale kierunek jest jasny.
>
> Scale? Dzisiaj klonujemy jednego Mike'a. Docelowo — każdego kluczowego pracownika w organizacji. CTO, Head of Product, Lead Marketera. Firma, w której żadna wiedza nie jest single point of failure.
>
> Viven AI zebrał 35 milionów na digital twins. Oni mają text chat. My mamy voice agenta, który nie tylko odpowiada — ale generuje dokumenty, identyfikuje luki i mówi ci kogo musisz zatrudnić.
>
> **Gemellus** — *two problems, one system. Knowledge that works, even when people don't.*"

**EKRAN:**
```
$31,5 mld/rok problem (IDC)
     ↓
Gemellus: 2 filary, 1 system
     ↓
Filar 1: Orientacja w 2 min, nie w 7 dni
Filar 2: Hiring z danych, nie szablonów

gemellus.app
```

---

#### Scoring Scenariusza C

| Kryterium | Ocena | Uzasadnienie |
|-----------|-------|--------------|
| **Running Code** | 4/5 | Identyczne demo jak A/B, ale więcej czasu na slajdy i porównania — mniej „kodu na żywo" |
| **Innovation & Creativity** | 5/5 | Framing dwóch filarów jako jednego systemu + ROI calculation + porównanie z Viven AI |
| **Real-world Impact** | 5/5 | Najpełniejsze uzasadnienie — twarde dane na oba filary + tabela porównawcza + oszczędności |
| **Theme Alignment** | 4/5 | Multimodalność widoczna, ale mniej eksponowana — focus na ROI |
| **Łącznie** | **18/20** | |

---

## Rekomendacja końcowa

### Optymalny wariant: Scenariusz A z elementami B

**Dlaczego A jest najsilniejszy:**
- Emocjonalny hook natychmiast angażuje (każdy był w sytuacji „ktoś odszedł, co teraz")
- Naturalne przejście z Filaru 1 do Filaru 2 — nie wymaga zmiany tonu
- Wow momenty pojawiają się organicznie, nie trzeba ich tłumaczyć
- Hiring pack jako punchline buduje napięcie

**Co wziąć z B:**
- Panel ADK events (transparentność procesu) — na ekranie, ale prezenter nie zatrzymuje się, żeby tłumaczyć. Jury techniczne zobaczy i doceni; jury biznesowe skupi się na outputach.

**Co wziąć z C (jako backup):**
- Tabela porównawcza „BEZ GEMELLUS vs Z GEMELLUS" — na slajdzie Q&A, nie w demo
- ROI calculation — na pytanie jury „jaki jest business case?"
- Dane rynkowe (Viven AI $35M) — na pytanie „kto jeszcze to robi?"

### Kluczowa różnica vs wersja 1 tego dokumentu:

| Wersja 1 | Wersja 2 |
|----------|----------|
| „Klonujemy Mike'a" — focus na osobie | „Rozwiązujemy dwa problemy biznesowe" — focus na wartości |
| Jeden flow: Q&A → hiring pack | Dwa akty: orientacja + redistrybucja → identyfikacja luk + hiring pack |
| Moment wow: precyzyjny JD | Moment wow: agent rozdziela pracę na ludzi + mówi „to nie 1 hire, to 2-3 stanowiska" |
| Zamknięcie: „wiedza nie odchodzi" | Zamknięcie: „dwa problemy, jeden system" |

### Backup plan (jeśli demo się wywali):

1. **Video nagranie** rozmowy z agentem (nagrane wcześniej) — puścić jako fallback
2. **Screenshot hiring packu** — pokazać jako static output z komentarzem „wygenerowano w 30 sekund"
3. **Tabela porównawcza** z Scenariusza C — działa bez kodu, adresuje oba filary

---

## Appendix: Pełne dane do promptu agenta

### Źródła, na które agent powinien się powoływać

| Źródło | Filar | Konkret |
|--------|-------|---------|
| 1:1 2025-03-17 | F1+F2 | Bus factor: „4 krytyczne obszary: Re.Pack runtime, auto-linking, Meta, release process" |
| 1:1 2025-03-03 | F1 | „Potrzebujemy dokumentować 'dlaczego', nie tylko 'co'. Zaczynam pisać ADR-y." |
| 1:1 2025-02-10 | F2 | „40 aplikacji, 3 z bundler experience. Niszowy profil." + „OS work is our best marketing and hiring pipeline." |
| Slack #repack-dev 02-05 | F1 | Bug `__webpack_require__.l` — workaround z `chunkLoading: async-node` |
| Slack #hiring 02-20 | F2 | Format interview: debugging task (30 min) + design discussion (30 min) + OS scenarios (15 min) |
| Slack #general 02-15 | F1 | „Metro is CRA, Re.Pack is custom webpack config. 80/20 podział." |
| Slack #repack-dev 03-05 | F1 | Rspack — „experimental flag, nie first-class. Poczekajmy na dojrzałość MF w rspack." |
| Jira CLI-892 | F2 | Auto-linking bug z New Arch → root cause + fix → **zadanie rekrutacyjne** |
| Jira CORE-155 | F1 | ADR Metro vs Re.Pack: „kluczowy differentiator to ekosystem, nie wydajność" |
| Jira HIRE-301 | F2 | Kryteria hiring: bundler internals, native build systems, Hermes, OS maturity |
| Jira RPACK-401 | F1+F2 | Module Federation v2 — Paweł robił review (→ redistrybucja na Pawła) |
| Jira RPACK-445 | F1 | Hermes compat layer — tylko Mike zna runtime od środka |
| Talk Chain React 2017 | F1 | „The Dark Art of Bundlers" — geneza Haul → Re.Pack |
| GitHub profile | F1 | „Passionate about cross platform tech. When not working, find me on a race track." |
| Podcast React Universe | F1 | Styl komunikacji Mike'a — praktyczny, bezpośredni, evidence-based |

### Kompetencje Mike'a (do użycia przez `analyze_skills`)

```json
{
  "primary_skills": [
    "bundler_internals (webpack, rspack, metro)",
    "module_federation (web + mobile)",
    "react_native_core (new architecture, turbomodules)",
    "hermes_engine (bytecode, AOT compilation)",
    "native_build_systems (xcode, gradle, cocoapods)",
    "open_source_maintenance (cli, repack, haul, rnpm)",
    "cli_tooling (autolinking, config resolution)"
  ],
  "unique_to_mike": [
    "repack_runtime_architecture (chunk loading mechanism)",
    "autolinking_original_design (rnpm → rn core → community cli)",
    "meta_rn_team_relationship (direct escalation contacts)",
    "release_process_tribal_knowledge (0.64, 0.73, 0.74)"
  ],
  "partially_covered_by_team": [
    "webpack_plugin_development → Paweł",
    "cli_issue_triage → new tooling engineer (April 1)",
    "react_native_paper → Paper team",
    "ai_incubator → delegated"
  ],
  "leadership_skills": [
    "conference_organization (React Native EU / React Universe Conf)",
    "podcast_hosting (React Native Show / React Universe On Air)",
    "technical_hiring (interview design, candidate evaluation)",
    "enterprise_client_advisory (metro vs repack decisions)"
  ]
}
```

### Redistrybucja pracy (do użycia przez `analyze_team_context`)

```json
{
  "redistribution_plan": [
    {
      "area": "Re.Pack runtime (Hermes OOM fix)",
      "priority": "CRITICAL",
      "current_coverage": "NONE",
      "action": "HIRE — Senior Build Systems Engineer",
      "why": "Only Mike understands chunk loading mechanism internals"
    },
    {
      "area": "CLI maintenance + issue triage",
      "priority": "HIGH",
      "current_coverage": "PARTIAL",
      "action": "New tooling engineer (starts April 1) + mentor from team",
      "why": "200+ open issues, engineer already hired, needs onboarding"
    },
    {
      "area": "React Summit talk + demo",
      "priority": "MEDIUM",
      "current_coverage": "GOOD",
      "action": "Paweł — reviewed webpack plugin, knows demo codebase",
      "why": "Demo is working e2e, needs shepherd not builder"
    },
    {
      "area": "Meta RN team relationship",
      "priority": "HIGH",
      "current_coverage": "NONE",
      "action": "Leadership must build relationship — not a hire, it's a process",
      "why": "Direct escalation contacts, trust-based, can't be transferred via doc"
    },
    {
      "area": "Release process knowledge",
      "priority": "MEDIUM",
      "current_coverage": "LOW",
      "action": "Documentation sprint — video walkthroughs + ADRs",
      "why": "Tribal knowledge, but codifiable. Mike started ADRs but didn't finish"
    }
  ]
}
```
