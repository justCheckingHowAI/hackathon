# Maks Demo Plan

## Kontekst

Hackathon ma bardzo konkretne ograniczenia:

- ok. 8 godzin na build
- nacisk na `running code`, nie pitch deck
- theme alignment do `multimodal agents`
- warto użyć stacku sponsorów: `Google / Vertex AI / Gemini` oraz `Vapi`
- demo finałowe ma bardzo mały budżet czasowy, więc produkt musi mieć jedno czytelne "wow"

Pierwotny pomysł zespołu:

- mapować knowledge base organizacji programistycznej
- analizować transkrypcje rozmów, repozytoria git, Slack/Discord, webinary itp.
- identyfikować luki kompetencyjne
- rekomendować role do zatrudnienia
- generować opis stanowiska
- definiować sygnały, red flags i screening
- robić wstępny pre-screening kandydata
- ewentualnie generować materiały promocyjne / video

Problem tej wersji: to jest kilka produktów naraz. Na hackathon jury oceni przede wszystkim działający, spójny flow.

## Najlepszy framing

Najmocniejszy framing na demo:

> When a key employee leaves, our multimodal agent turns messy organizational knowledge into a backfill hiring plan in minutes.

Wersja po polsku:

> Gdy odchodzi kluczowa osoba, nasz multimodalny agent zamienia rozproszoną wiedzę firmy w gotowy plan backfillu: czego brakuje, kogo szukać i jak go ocenić.

To jest znacznie lepsze niż szerokie "mapujemy cały knowledge base organizacji", bo:

- ma jeden konkretny trigger
- daje mocny, zrozumiały problem biznesowy
- łatwo pokazać end-to-end flow
- pozwala pokazać wartość w 3 minuty

## Ocena Pomysłu Pod Kątem Kryteriów

### 1. Running Code

Ocena obecnego szerokiego pomysłu: `2/5`

Ryzyka:

- za szeroki scope
- dużo integracji i za dużo feature'ów
- łatwo skończyć z luźnymi generatorami zamiast jednego działającego produktu
- jury może uznać, że to mock workflow, a nie realna aplikacja

Ocena po dobrym zawężeniu: `4/5`

Warunek:

- jedno spójne flow
- realny ingest danych
- realny agent
- realny wynik końcowy, który da się obejrzeć i przetestować

### 2. Innovation & Creativity

Ocena: `4/5`

Dlaczego:

- połączenie organizational memory + hiring/backfill agent nie jest banalnym "HR chatbotem"
- ciekawy jest moment przejścia od nieustrukturyzowanej wiedzy do konkretnej decyzji operacyjnej
- jeśli agent uzasadnia rekomendacje evidence-based, robi się to wyraźnie bardziej interesujące niż klasyczny RAG

Co blokuje `5/5`:

- sam "AI do hiringu" nie jest już nowy
- trzeba pokazać unikalny workflow i sensowne reasoning, nie tylko generację tekstu

### 3. Real-world Impact

Ocena: `4/5`

Dlaczego:

- utrata wiedzy po odejściu kluczowych ludzi to realny, kosztowny problem
- złe backfille są drogie
- hiring teams często nie umieją szybko przełożyć faktycznych luk kompetencyjnych na dobry proces rekrutacyjny

Co blokuje `5/5`:

- bez działającego przykładu może to brzmieć zbyt strategicznie i zbyt szeroko
- potrzeba konkretnego use case'u, najlepiej z jedną osobą odchodzącą lub jednym nowym projektem

### 4. Theme Alignment

Ocena obecna: `2/5`

Dlaczego:

- sam pomysł jest mocny produktowo, ale nie jest jeszcze naturalnie pokazany jako `multimodal agent`
- bez voice/audio/PDF/code ingestion może wyglądać jak zwykły RAG dashboard

Ocena po odpowiednim złożeniu: `4/5`

Warunek:

- użycie `Gemini / Vertex AI` do ekstrakcji i reasoning
- użycie `Vapi` jako voice recruiter / screening agent
- multimodalne wejścia, np.:
  - CV PDF
  - audio rozmowy / voice screening
  - tekst z repo / Slack / transcriptów

## Główne Słabe Strony

### 1. Scope jest za szeroki

Obecnie pomysł obejmuje:

- organizational knowledge mapping
- skill gap detection
- backfill planning
- JD generation
- sourcing strategy
- screening design
- candidate Q&A
- candidate pre-screening
- CV matching
- potencjalnie video ad

To jest kilka osobnych produktów. Na hackathon trzeba brutalnie zawęzić scope.

### 2. Trudno obronić trafność rekomendacji

Jeśli system mówi:

> potrzebujecie Staff Engineera od distributed systems

jury może zapytać:

- z czego to wynika?
- jakie artefakty to potwierdzają?
- czy to nie jest hallucination?

Dlatego wynik musi mieć warstwę `evidence`, np.:

- skill detected from repo activity
- recurring domain ownership in transcripts
- missing responsibilities after employee exit

### 3. Wartość jest zbyt abstrakcyjna w szerokim framingu

"Mapujemy wiedzę organizacji" brzmi dobrze, ale nie daje szybkiego zrozumienia.

"Ania odchodzi i w 90 sekund dostajemy gotowy hiring pack" jest natychmiast czytelne.

### 4. Theme risk

Jeśli demo będzie tylko:

- upload dokumentów
- analiza
- wygenerowany raport

to projekt może nie wyglądać jak multimodalny agent, tylko jak kolejne RAG SaaS.

### 5. Data / integration risk

Nie zdążycie sensownie zintegrować wszystkiego:

- GitHub
- Slack
- Discord
- webinar transcripts
- call transcripts
- CV parser
- voice bot

Lepiej mieć 2-3 źródła wejściowe, ale dobrze spięte w jeden flow.

### 6. Trust / privacy risk

Automatyzacja hiringu jest wrażliwa. Nie możecie wyglądać jak system, który:

- automatycznie odrzuca kandydatów
- podejmuje decyzje HR bez człowieka

Lepiej mówić:

- agent przygotowuje evidence-backed recommendation
- final decision remains with the hiring team

## Co Uciąć Bez Litości

Nie brać do MVP:

- generowania video / spotu reklamowego
- pełnej strategii sourcingowej
- pełnego mapowania całej organizacji
- automatycznych decyzji hiringowych
- więcej niż 3 typów inputów

## Recommended MVP Scope

Najlepszy scope na hackathon:

### Core use case

> A key engineer is leaving. The system analyzes team knowledge artifacts, identifies the real competency gap, generates a hiring pack, and helps run the first candidate screen.

### Wejścia

Tylko `3` typy danych:

- repo / README / PR notes / docs
- transcript rozmowy lub export ze Slack/Discord
- CV kandydata w PDF

### Outputy

System powinien zwrócić:

- `skill evidence map`
- `gap summary`
- `role recommendation`
- `JD / scorecard`
- `must-have signals`
- `red flags`
- `interview loop + questions`
- `candidate match summary`

### Konieczne ograniczenie

Nie budować "platformy HR". Budować jeden przepływ:

1. firma sygnalizuje odejście osoby albo potrzebę nowej roli
2. agent analizuje knowledge artifacts
3. agent tworzy hiring pack
4. kandydat przechodzi mini screening
5. hiring team dostaje rekomendację

## Jak Użyć Stacku Sponsorów

### Google / Vertex / Gemini

Najbardziej sensowne użycie:

- ekstrakcja kompetencji z tekstu i dokumentów
- synteza luki kompetencyjnej
- structured output do scorecard / JD / interview plan
- reasoning nad wieloma źródłami

### Vapi

Najbardziej sensowne użycie:

- voice recruiter / screening assistant
- candidate asks questions about the role
- system zadaje 2-3 screening questions
- transcript z rozmowy trafia do końcowej oceny

### Multimodalność

Żeby theme alignment był mocny, pokażcie przynajmniej:

- PDF CV
- voice interaction
- textual knowledge artifacts

To wystarczy, żeby projekt uczciwie nazwać multimodalnym agentem.

## 3 Alternatywy Demo

## Alternatywa 1: Backfill Agent After Employee Exit

To jest najmocniejsza opcja.

### User journey

1. Hiring manager mówi: `Ania, nasza Senior Backend Engineer, odchodzi za 3 tygodnie.`
2. Agent analizuje repo, Slack / transcripts i dokumenty.
3. Agent pokazuje, jakie kompetencje i odpowiedzialności realnie znikają.
4. Agent generuje hiring pack.
5. Kandydat wrzuca CV.
6. Kandydat przechodzi krótki voice screening przez Vapi.
7. System pokazuje match score i uzasadnienie dla hiring teamu.

### Dlaczego to działa

- bardzo konkretny trigger
- łatwy do zrozumienia problem
- end-to-end flow jest naturalny
- można pokazać wartość operacyjną, nie tylko analysis

### Ocena

- `Running Code`: bardzo dobry fit
- `Innovation`: dobry
- `Impact`: bardzo dobry
- `Theme Alignment`: dobry, jeśli screening jest voice-based

### 3-minutowy układ demo

- `0:00-0:40` problem + ingest danych
- `0:40-1:30` skill gap + hiring pack
- `1:30-2:20` voice screening kandydata
- `2:20-3:00` match score + recommendation

## Alternatywa 2: Proactive Skill Gap Radar

Ta opcja jest bardziej strategiczna.

### User journey

1. CTO wrzuca roadmapę, repo i transcript webinaru o nowym obszarze.
2. Agent wykrywa, że organizacja wchodzi w domenę, której nikt dobrze nie pokrywa.
3. Agent proponuje nową rolę, zestaw kompetencji i proces oceny.

### Dlaczego to działa

- pokazuje predictive angle
- brzmi ambitnie biznesowo
- dobrze sprzedaje "organizational intelligence"

### Słabość

- mniej emocjonalne niż odejście kluczowej osoby
- trudniej obronić trafność rekomendacji
- mniej naturalne do szybkiego demo

### Ocena

- `Running Code`: średni fit
- `Innovation`: dobry
- `Impact`: dobry
- `Theme Alignment`: średni do dobrego

## Alternatywa 3: Candidate Copilot Based on Organizational Knowledge

Ta opcja jest najbardziej widowiskowa z perspektywy voice demo.

### User journey

1. Zespół ma zdefiniowaną lukę kompetencyjną.
2. Kandydat wrzuca CV.
3. Kandydat rozmawia z voice agentem przez Vapi.
4. Agent odpowiada na pytania o rolę i równolegle robi lekki screening.
5. Hiring team dostaje structured summary i ocenę dopasowania.

### Dlaczego to działa

- bardzo demo-friendly
- łatwo pokazać Vapi
- łatwo pokazać multimodalność

### Słabość

- mniej unikalne
- może zostać odebrane jako "kolejny recruiter bot"
- słabiej eksponuje organizational memory aspect

### Ocena

- `Running Code`: dobry fit
- `Innovation`: średni do dobrego
- `Impact`: dobry
- `Theme Alignment`: bardzo dobry

## Ranking Alternatyw

1. `Backfill Agent After Employee Exit`
2. `Proactive Skill Gap Radar`
3. `Candidate Copilot Based on Organizational Knowledge`

## Rekomendacja

Najlepszy wybór na hackathon:

`Alternatywa 1: Backfill Agent After Employee Exit`

Dlaczego:

- najlepszy balans między wykonalnością a wow effect
- łatwo obronić biznesową wartość
- łatwo zrobić demo end-to-end
- łatwo podpiąć multimodalność i sponsor stack

## Minimalny Scope Aplikacji

Jeśli trzeba zejść jeszcze niżej, to aplikacja może mieć tylko 3 ekrany:

### 1. Team Knowledge Intake

- upload / podgląd 2-3 artefaktów
- wskazanie osoby, która odchodzi
- uruchomienie analizy

### 2. Backfill Hiring Pack

- luka kompetencyjna
- evidence snippets
- recommended role
- scorecard
- interview questions

### 3. Candidate Screen

- upload CV
- krótka rozmowa głosowa przez Vapi
- final fit summary

To wystarczy na hackathon.

## Ważne Zasady Produktowe

### 1. Nie udawajcie pełnej prawdy o organizacji

Mówcie:

- agent analyzes selected artifacts
- produces evidence-backed recommendations

Nie mówcie:

- system understands the whole company

### 2. Nie obiecujcie automatycznego hiringu

Mówcie:

- assists hiring teams
- accelerates backfill planning
- summarizes candidate fit

Nie mówcie:

- decides who to hire

### 3. Dowody są ważniejsze niż długość outputu

Lepiej pokazać:

- 3 konkretne evidence snippets

niż:

- 2 strony wygenerowanego opisu roli

## Proponowany Pitch

### One-liner

> When critical employees leave, companies lose both capacity and hidden knowledge. Our multimodal agent turns internal artifacts and candidate signals into a ready-to-run backfill process in minutes.

### Krótsza wersja na scenę

> We turn messy company knowledge into hiring action.

## Następne Decyzje Do Iteracji

Przed kolejnym krokiem warto ustalić:

- czy demo idzie w `employee exit / backfill`, czy w `proactive skill gap`
- jakie dokładnie `3 źródła danych` bierzemy do MVP
- czy voice demo ma być po stronie `kandydata`, czy `hiring managera`
- czy w 3 minuty pokazujemy pełne end-to-end, czy kończymy przed screeningiem

