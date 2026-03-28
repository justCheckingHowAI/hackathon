# TeamTwin - "Talk to Your Teammate"

## Multimodal Voice Agent That Clones Developer Knowledge

---

## Elevator Pitch

TeamTwin pozwala dosłownie zadzwonić do cyfrowego klona developera, który odszedł z firmy - i przeprowadzić z nim naturalną rozmowę o architekturze, decyzjach technicznych i know-how projektowym. Na tej samej bazie wiedzy system generuje ultra-precyzyjne materiały rekrutacyjne i prowadzi spersonalizowane rozmowy kwalifikacyjne z kandydatami.

**Stack:** Google Gemini 3.1 (multimodal reasoning, 2M context) + VAPI (voice agent orchestration)

---

## Problem

Kiedy senior developer odchodzi z firmy, zabiera ze sobą wiedzę, której nie ma w żadnej dokumentacji: dlaczego architektura wygląda tak a nie inaczej, jakie workaroundy zastosowano i dlaczego, jak naprawdę działa deployment pipeline, kontekst decyzji technicznych z ostatnich miesięcy. Koszt utraty takiej wiedzy to średnio 6-9 miesięcy produktywności nowego człowieka. A proces rekrutacyjny opiera się na generic job descriptions i standardowych pytaniach, które nie testują tego, co naprawdę jest potrzebne w danym projekcie.

---

## Rozwiązanie - Trzy Voice Agenty, Jedna Baza Wiedzy

### Agent 1: Knowledge Clone ("Porozmawiaj z Tomkiem")

**Co robi:** Voice agent VAPI, z którym rozmawiasz jak z prawdziwym członkiem zespołu. Pytasz o projekt, architekturę, decyzje - agent odpowiada w kontekście całej wiedzy, którą miał dany developer.

**Jak działa pod spodem:**
- Gemini 3.1 przetwarza multimodalnie wszystkie źródła wiedzy developera: transkrypcje spotkań, wiadomości Slack/Discord, tickety Jira, commity i PR-y, dokumentację techniczną, screenshoty architektury i diagramy
- 2M token context window pozwala załadować ogromny kontekst bez skomplikowanego RAG-a
- VAPI obsługuje naturalną rozmowę głosową z niskim latency
- Agent ma "osobowość" dopasowaną do stylu komunikacji danego developera (wyciągniętą z transkryptów)

**Przykładowa interakcja:**
```
Ty: "Hej, jak działa nasz pipeline do deploymentu na staging?"
Agent: "Używamy GitHub Actions z customowym workflow. Ważne - jest tam
       workaround na problem z cache'owaniem Docker layers, bo standardowy
       approach nie działał z naszym monorepo. Dodałem to po tym jak
       straciliśmy pół dnia na debugowanie w styczniu. Chcesz żebym
       opowiedział o tym workaroundzie?"
Ty: "Tak, i pokaż mi ten diagram, o którym mówiłeś na standupie."
Agent: [wysyła screenshot diagramu architektury pipeline'u]
```

### Agent 2: Recruitment Generator ("Znajdź zastępstwo")

**Co robi:** Na bazie profilu kompetencyjnego klona generuje komplet materiałów rekrutacyjnych - nie generic, a ultra-spersonalizowanych pod realia projektu.

**Co generuje:**
- **Job description** zbudowany z realnych kompetencji, nie buzzwordów. Zamiast "experience with microservices" pisze "must understand event-driven architecture with RabbitMQ, specifically handling message deduplication across three producer services"
- **Zadanie rekrutacyjne** wyciągnięte z prawdziwych problemów projektu (zanonimizowane). Kandydat rozwiązuje coś, co naprawdę trzeba będzie ogarnąć w tej roli
- **Scoring rubric** z kryteriami oceny opartymi na tym, co faktycznie było ważne w codziennej pracy
- **Profil idealnego kandydata** z wagami: co jest must-have (bo projekt tego wymaga), a co nice-to-have

**Interakcja głosowa:**
```
Ty: "Tomek odchodzi za dwa tygodnie. Przygotuj materiały rekrutacyjne."
Agent: "Na podstawie profilu Tomka widzę, że kluczowe kompetencje to:
       event-driven architecture, Kubernetes, i monitoring z Grafana stack.
       80% jego pracy to backend w Go, 20% to DevOps. Przygotowałem job
       description, zadanie techniczne i kryteria oceny. Chcesz je
       przejrzeć?"
Ty: "Dodaj jeszcze wymaganie o doświadczeniu z migracjami baz danych,
     bo planujemy przejście z Postgres na CockroachDB."
Agent: "Dodane. Zaktualizowałem też zadanie rekrutacyjne - teraz zawiera
       scenariusz migracji danych między bazami. Wysyłam dokumenty."
```

### Agent 3: AI Interviewer ("Przeprowadź rozmowę")

**Co robi:** Voice agent VAPI prowadzi techniczną rozmowę rekrutacyjną z kandydatem, zadając pytania oparte na realnych wyzwaniach projektu. Ocenia odpowiedzi w kontekście tego, jak te problemy były faktycznie rozwiązane.

**Jak działa:**
- Pytania są wyciągnięte z realnych problemów, bugów, decyzji architektonicznych
- Gemini analizuje odpowiedzi kandydata i porównuje z tym, jak developer faktycznie podchodził do takich problemów
- Agent adaptuje pytania na bieżąco - jeśli kandydat dobrze odpowiedział na pytanie o architekturę, idzie głębiej; jeśli słabo, sprawdza fundamenty
- Na koniec generuje scoring i rekomendację

**Przykładowa interakcja z kandydatem:**
```
Agent: "W naszym systemie mamy trzy mikroserwisy produkujące eventy do
       wspólnej kolejki. Jeden z nich regularnie generuje duplikaty
       przez race condition. Jak byś podszedł do tego problemu?"
Kandydat: [odpowiada]
Agent: "Ciekawe podejście. A jak byś obsłużył sytuację, w której
       deduplikacja musi działać across multiple consumers, z których
       każdy ma swój własny state?"
```

---

## Architektura Techniczna

```
┌─────────────────────────────────────────────────┐
│                   VAPI Platform                  │
│         (Voice orchestration + telephony)        │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Knowledge │  │Recruiter │  │  Interviewer  │  │
│  │  Clone    │  │Generator │  │    Agent      │  │
│  │  Agent    │  │  Agent   │  │               │  │
│  └─────┬────┘  └─────┬────┘  └──────┬────────┘  │
└────────┼─────────────┼──────────────┼────────────┘
         │             │              │
         └──────────┐  │  ┌───────────┘
                    ▼  ▼  ▼
         ┌─────────────────────────┐
         │   Google Gemini 3.1     │
         │   (Multimodal Brain)    │
         │                         │
         │ - 2M token context      │
         │ - Text + Image + Code   │
         │ - Reasoning + Analysis  │
         └────────────┬────────────┘
                      │
                      ▼
         ┌─────────────────────────┐
         │   Knowledge Base        │
         │                         │
         │ - Meeting transcripts   │
         │ - Slack/Discord msgs    │
         │ - Jira tickets          │
         │ - Git commits + PRs     │
         │ - Architecture diagrams │
         │ - Technical docs        │
         └─────────────────────────┘
```

### Komponenty do zbudowania:

1. **Data Ingestion Layer** - skrypty do parsowania i strukturyzowania danych z różnych źródeł (na hackaton: mockowane dane lub 2-3 prawdziwe źródła)
2. **Context Builder** - buduje profil kompetencyjny developera z surowych danych, tworzy "osobowość" agenta
3. **VAPI Agent configs** - konfiguracja trzech agentów z system promptami, tool definitions, voice settings
4. **Gemini integration** - multimodalne przetwarzanie zapytań z kontekstem knowledge base
5. **Output generator** - formatowanie materiałów rekrutacyjnych (job desc, zadania, scoring rubric)
6. **Frontend dashboard** (opcjonalnie) - wizualizacja profilu kompetencyjnego, scoring kandydatów

---

## Plan Demo - 5 Minut na Efekt Wow

### Setup na scenie

Dwa telefony na stole + ekran z dashboardem. Jeden telefon to "linia do Tomka" (klona), drugi to "linia rekrutacyjna".

### Akt 1: "Tomek odszedł, ale jego wiedza nie" (1.5 min)

Prowadzący: "Tomek, nasz senior backend developer, odszedł tydzień temu. Ale zostawił coś cenniejszego niż dokumentację."

*Dzwoni na pierwszy telefon.*

"Hej Tomek, nowy developer pyta jak działa nasz payment pipeline. Możesz opowiedzieć?"

Agent (głos Tomka) odpowiada naturalnie, z kontekstem - opisuje architekturę, wspomina decyzje projektowe, ostrzega przed pułapkami.

"A pokaż mi ten diagram, który rysowałeś na ostatnim sprincie."

Na ekranie pojawia się diagram - Gemini odnalazł go multimodalnie w bazie danych.

**Moment wow #1:** Agent cytuje konkretną rzecz ze spotkania ("pamiętasz jak na standup'ie 12 marca mówiłem, że ten endpoint ma race condition? Ciągle nie jest naprawiony").

### Akt 2: "Znajdź mi drugiego Tomka" (1.5 min)

"OK, potrzebujemy zastępstwa. Tomek, wygeneruj materiały rekrutacyjne na swojego następcę."

Agent analizuje profil i generuje: job description pojawia się na ekranie - ultra-specyficzny, ze zdaniami typu "musi rozumieć event sourcing w kontekście płatności z wieloma providerami". Potem zadanie rekrutacyjne - zanonimizowany realny problem z projektu. Potem scoring rubric z wagami.

Prowadzący: "Dodaj wymaganie o doświadczeniu z migracjami, bo planujemy przenosić się na nową bazę."

Agent: "Gotowe. Dodałem też pytanie o migracje do zadania rekrutacyjnego."

**Moment wow #2:** Materiały są absurdalnie precyzyjne w porównaniu z generic job descriptions.

### Akt 3: "Rozmowa rekrutacyjna na sterydach" (2 min)

"Mamy kandydata. Przeprowadźmy z nim rozmowę."

Ktoś z publiczności (lub członek zespołu) dzwoni na drugi telefon. AI Interviewer prowadzi rozmowę: zadaje pytanie oparte na realnym problemie z projektu. Kandydat odpowiada. Agent drąży, adaptuje pytania.

Na ekranie w real-time pojawia się scoring: "architectural thinking: 4/5", "problem decomposition: 3/5", "communication: 5/5".

Na koniec agent mówi: "Dziękuję. Na podstawie rozmowy, kandydat pokrywa 78% profilu kompetencyjnego Tomka. Mocne strony: system design i komunikacja. Luki: brak doświadczenia z event sourcing - rekomendowane 2-tygodniowe onboardingowe deep dive."

**Moment wow #3:** Agent nie tylko ocenia, ale daje konkretną rekomendację onboardingową, bo wie, czego kandydatowi brakuje vs. co Tomek umiał.

### Zamknięcie

"TeamTwin to nie replacement dla ludzi. To gwarancja, że kiedy odchodzą, ich wiedza zostaje - i że następna osoba dostanie najlepszy możliwy start."

---

## Scoring Kryteriów Hackatonu - Samoocena

| Kryterium | Target | Dlaczego |
|-----------|--------|----------|
| **Running Code** | 4-5 | Trzy działające voice agenty na VAPI + Gemini, live demo z prawdziwymi rozmowami |
| **Innovation** | 4-5 | Połączenie digital twin + voice interaction + AI-driven recruitment to novel combination |
| **Real-world Impact** | 5 | Knowledge drain + kosztowna rekrutacja to top 3 problemy CTO. Rozwiązanie jest natychmiast użyteczne |
| **Theme Alignment** | 5 | Trzy multimodalne voice agenty zbudowane na Gemini + VAPI. To jest dokładnie to, czego hackaton szuka |

---

## Podział Zadań na Hackaton

### Faza 1: Fundament (pierwsze 2-3h)
- Przygotowanie mockowanych danych (transkrypty spotkań, wiadomości Slack, tickety Jira, fragmenty kodu) - powinny być realistyczne i spójne, opowiadać historię jednego developera w projekcie
- Setup Gemini API + VAPI accounts
- Proof of concept: jeden VAPI agent odpowiadający na pytania z kontekstem z Gemini

### Faza 2: Knowledge Clone (2-3h)
- Context builder - strukturyzowanie danych w profil kompetencyjny
- System prompt dla agenta "Tomka" z osobowością i kontekstem
- Integracja multimodalna - agent potrafi wysłać diagram/screenshot gdy pytany
- Testowanie naturalności rozmowy

### Faza 3: Recruitment Generator (2h)
- Template'y dla job description, zadania, scoring rubric
- Prompt engineering - generowanie materiałów na bazie profilu
- Głosowa interakcja z agentem do iterowania na materiałach

### Faza 4: Interview Agent (2h)
- Bank pytań wygenerowanych z profilu kompetencyjnego
- Logika adaptacyjna (uproszczona - if/then na scoring)
- Real-time scoring na ekranie
- Podsumowanie i rekomendacja

### Faza 5: Polish + Demo prep (1-2h)
- Dashboard na ekran (może być prosty HTML/React)
- Przejście demo od A do Z
- Backup plan na wypadek problemów z siecią/API

---

## Potencjalne Rozszerzenia (Post-hackaton / Pitch na przyszłość)

- **Team-wide analysis** - mapa kompetencyjna całego zespołu, identyfikacja bus factor i single points of failure
- **Proaktywny knowledge capture** - agent regularnie "rozmawia" z developerami, wyciągając tacit knowledge zanim odejdą
- **Onboarding buddy** - nowy developer dostaje voice agenta, który zna cały kontekst projektu i odpowiada 24/7
- **Cross-team matchmaking** - "kto w firmie rozwiązywał podobny problem?" na bazie klonów wszystkich developerów
- **Competency gap detector** - porównanie profili zespołu z wymaganiami roadmapy, rekomendacje szkoleń lub rekrutacji
- **Exit interview automation** - ustrukturyzowana rozmowa głosowa wyciągająca wiedzę, której nie ma w docs

---

## Ryzyka i Mitygacja

| Ryzyko | Mitygacja |
|--------|-----------|
| Jakość mockowanych danych | Poświęć czas na realistyczne dane - to 50% sukcesu demo |
| Latency VAPI + Gemini | Testuj wcześnie, miej fallback na mniejszy model Gemini Flash |
| Agent nie brzmi naturalnie | Dopracuj system prompt z "osobowością", testuj różne voice settings |
| Demo się wysypie na żywo | Miej nagrany backup video, ale staraj się robić live |
| Za duży scope | Priorytet: Agent 1 musi działać idealnie. Agent 2 i 3 mogą być uproszczone |

---

## Killer Framing na Pitch

Nie mów "zbudowaliśmy knowledge management tool". Mów: **"Co by było, gdybyś mógł zadzwonić do kolegi, który odszedł z firmy pół roku temu, i zapytać go o cokolwiek?"**

To jest hook. Reszta to odpowiedź na pytanie "i co dalej z tą wiedzą?".

