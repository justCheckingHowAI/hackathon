# Podsumowanie spotkania 1 — 2026-03-28

**Źródło:** `narada1_transkrypcja.txt` (nagranie 20260328-131721-Rec39.hda)
**Czas trwania:** ~17 minut
**Uczestnicy:** Max, Janusz, Adam, Przemek, Mieszko

---

## Skład zespołu i role

| Osoba | Rola | Odpowiedzialność na hackathonie |
|-------|------|--------------------------------|
| **Max** | Developer (core) | Konfiguracja API (Google, Vapi), rozwój backendu, środowisko deweloperskie |
| **Janusz** | Developer (core) | Konfiguracja API (Google, Vapi), rozwój backendu, środowisko deweloperskie |
| **Adam** | Produkt / doświadczenie VC / vibecoding | Zbieranie i organizacja danych (większość zebrana wcześniej) |
| **Przemek** | Produkt / doświadczenie VC / vibecoding | Historia demo i narracja, nazwa produktu, prezentacja, strona WWW, UI |
| **Mieszko** | Kreatywny / artystyczny | Historia demo i narracja (z Przemkiem), projekt UI, wizualizacje prezentacji |

---

## Kluczowe decyzje

### 1. Cel klonowania: tylko Mike Grabowski

Zespół uzgodnił skupienie wyłącznie na **Mike'u Grabowskim** w ramach MVP hackathonowego. Klonowanie wielu osób jest wyraźnie oznaczone jako **funkcja na przyszłość**, nie na dzisiaj.

> „Ograniczamy się na razie, nie skupiamy się na całym zespole, wspieramy tylko Mike'a."

Omówiona wizja długoterminowa: każdy członek zespołu miałby własną personę/klona i można by pytać dowolnego z nich. Ale na demo — tylko Mike.

### 2. Przebieg demo — struktura dwufazowa

Zespół uzgodnił podejście dwóch pytań:

**Pytanie 1 — Pozyskanie wiedzy:**
> „Mike, jesteś na urlopie, ale powiedz mi — co się stało w projekcie X i dlaczego podjęto tę decyzję?"

Demonstruje to zdolność klona wiedzy — agent odpowiada kontekstem projektowym, decyzjami architektonicznymi i wiedzą instytucjonalną.

**Pytanie 2 — Luka kompetencyjna / rekrutacja:**
> „Mike nie będzie już uczestniczył w tym projekcie. Kogo musimy znaleźć? Przygotuj pakiet rekrutacyjny."

Demonstruje to wartość wykraczającą poza proste Q&A — agent generuje opisy stanowisk, zadania rekrutacyjne, kryteria oceny i scoring kandydatów.

### 3. Architektura: dwa główne komponenty

| Komponent | Technologia | Cel |
|-----------|-------------|-----|
| **Warstwa głosowa** | Vapi | Interfejs rozmowy telefonicznej, speech-to-text, text-to-speech |
| **Mózg agenta** | Google Agent SDK (ADK) | Wnioskowanie, zapytania do bazy wiedzy, generowanie strukturalnych wyników |

Proces backendowy w ADK może być **wizualizowany podczas demo**, aby pokazać co dzieje się „pod maską" (wywoływane narzędzia, pobierane dane).

### 4. Strategia danych

- Adam ma już **większość danych zebranych** z pracy przed hackathnem (GitHub PR-y, podcasty, szablony danych syntetycznych)
- Dane muszą być zorganizowane w formacie do konsumpcji (Markdown lub JSON)
- Ingestion danych powinien mieć **funkcję odświeżania** (nie jednorazowy import)
- Na demo: dane są wstępnie załadowane, ale system powinien pokazywać możliwość aktualizacji

### 5. Multimodalność — minimum viable

Zespół uzgodnił, że **dwie modalności wystarczą** na hackathon:
- **Głos** (rozmowa telefoniczna przez Vapi)
- **Tekst** (załadowane dokumenty, wiadomości Slack, dane z GitHub)

Omówione opcjonalne dodatki (bez zobowiązania):
- Wideo/audio ingestion (np. pliki MP4 z podcastów)
- Przetwarzanie grafik/diagramów
- Mogą być dodane jako funkcje, jeśli starczy czasu

### 6. Podział zadań

| Ścieżka | Osoby | Fokus |
|----------|-------|-------|
| **Core development** | Max + Janusz | Konfiguracja Google API, integracja Vapi, Agent SDK, backend, środowisko dev |
| **Dane** | Adam | Organizacja zebranych danych, formatowanie do ingestion, konfiguracja bazy wiedzy |
| **Produkt i narracja** | Przemek + Mieszko | Narracja demo, nazwa produktu, prezentacja, strona WWW, projekt UI |
| **Wsparcie UI** | Max + Janusz (później) | Pomoc z frontendem/UI dla potrzeb backendu |

---

## Krytyczna dyskusja: zarzut NotebookLM

Znaczna część spotkania dotyczyła obawy, że produkt może zostać odrzucony jako **„po prostu NotebookLM z głosem"**. To najważniejsze zidentyfikowane ryzyko strategiczne.

### Zarzut
> „Wiesz co to NotebookLM? Możesz tam wrzucić wszystko — GitHub, spotkania, transkrypcje — i będzie z tobą rozmawiać jak Mike."

### Opracowane kontrargumenty

| Wyróżnik | NotebookLM | Nasz system |
|-----------|------------|-------------|
| **Auto-aktualizacja** | Statyczny — ręcznie wgrywasz źródła | Ciągłe pozyskiwanie i reindeksowanie nowych danych |
| **Wiele osób** | Jedna masa wiedzy, bez podziału na osoby | Odrębne persony na członka zespołu, routing pytań do właściwej osoby |
| **Wartość akcyjna** | Tylko konwersacyjne Q&A | Generuje pakiety rekrutacyjne, opisy stanowisk, zadania, kryteria oceny |
| **Mapowanie kompetencji** | Brak ekstrakcji umiejętności | Mapuje umiejętności na osoby, identyfikuje luki, rekomenduje kto powinien się czym zająć |
| **Okno kontekstu** | Ograniczone (testowano z podcastem — napotkano limity) | Zaprojektowane na dane w skali organizacji, wiele osób |

### Konkluzja
Zespół uzgodnił, że **pakiet rekrutacyjny / funkcja luki kompetencyjnej jest kluczowym wyróżnikiem**. Bez tego produkt jest podatny na porównanie z NotebookLM. Z tym — jest wyraźna dodatkowa wartość.

---

## Doprecyzowana wizja produktu

### Pozycjonowanie (wyłoniło się z dyskusji)

> Platforma dla C-level, która wspiera wzrost organizacyjny poprzez identyfikację najlepszych inwestycji kompetencyjnych — kogo zatrudnić, jakich umiejętności brakuje i jak znaleźć właściwych ludzi.

### Docelowi użytkownicy
- **Szybko rosnące startupy**, które muszą skalować zespoły szybko i precyzyjnie
- **Organizacje tracące kluczowe osoby**, które muszą zrozumieć jaka wiedza odchodzi razem z pracownikiem
- **Zespoły bez dedykowanego HR/Chief of Staff**, którym brakuje ekspertyzy do definiowania specjalistycznych ról

### Omówione przypadki użycia

| Przypadek użycia | Opis |
|-------------------|------|
| **Kluczowa osoba odchodzi** | Identyfikacja luk kompetencyjnych, generowanie pakietu rekrutacyjnego, szukanie zastępstwa |
| **Kluczowa osoba na urlopie** | Zapytanie do jej klona o wiedzę projektową, redystrybucja zadań |
| **Skalowanie zespołu** | Analiza roadmapy + obecnych możliwości, rekomendacja następnego zatrudnienia |
| **Luka kompetencyjna w projekcie** | „Potrzebujemy evals dla React Native — kto w zespole to potrafi?" → routing do klona właściwej osoby |
| **Nie wiesz czego potrzebujesz** | System analizuje wzorce pracy i artykułuje rolę, której sam nie potrafisz opisać |

### Insight „Nie wiesz czego potrzebujesz"

Jeden z najbardziej przekonujących momentów dyskusji:

> „Czasem nie potrafisz nazwać czego ci brakuje. Mówisz tylko »potrzebuję dobrego developera, który jest agile«. Ale sklonować Witka i wymyślić jak szukać kogoś takiego jak on — to jest niesamowite wyzwanie."

To pozycjonuje produkt jako rozwiązanie meta-problemu: **organizacje, które nie mają słownictwa do opisania kompetencji, których potrzebują**.

---

## Scenariusz demo (uzgodniony kierunek)

### Akt 1: Zapytanie o wiedzę
- Zadzwoń do klona Mike'a przez telefon
- Zapytaj o konkretną decyzję projektową lub problem techniczny
- Mike odpowiada z głębokim kontekstem, odwołując się do prawdziwych artefaktów

### Akt 2: Generowanie pakietu rekrutacyjnego
- Powiedz Mike'owi: „Nie będziesz już uczestniczył w projekcie. Potrzebujemy kogoś do obsługi X. Przygotuj pakiet rekrutacyjny."
- Mike generuje:
  - Opis stanowiska (specyficzny dla rzeczywistych potrzeb projektu, nie generyczny)
  - Zadania rekrutacyjne (oparte na prawdziwych wyzwaniach projektowych)
  - Kryteria oceny / rubryk scoringowy
  - Profil kandydata z must-have vs nice-to-have

### Wizualizacje wspierające
- Pokazanie procesu ADK (jakie narzędzia agent wywołał, jakie dane pobrał)
- Na slajdach prezentacji: pełna architektura i źródła danych
- Wygenerowany pakiet rekrutacyjny wyświetlony jako dopracowany output

---

## Nierozwiązane / odłożone kwestie

| Element | Status | Uwagi |
|---------|--------|-------|
| Nazwa produktu | **ROZWIĄZANE** | **[Gemellus](https://gemellus.app/)** |
| Dokładny skrypt demo z timingiem | **Nie sfinalizowano** | Będzie iterowany za ~1 godzinę po podziale zadań |
| Wsparcie klonowania wielu osób | **Odłożone (przyszłość)** | Tylko Mike na hackathon |
| Pipeline auto-ingestion | **Odłożony (przyszłość)** | Wstępnie załadowane dane na demo, funkcja odświeżania jako stretch goal |
| Strona WWW | **Do stworzenia** | Odpowiedzialność Przemka + Mieszka |
| Prezentacja | **Do stworzenia** | Odpowiedzialność Przemka + Mieszka |
| UI dla wyświetlania backendu | **Do zaprojektowania** | Max + Janusz pomogą, gdy zespół produktowy zdefiniuje potrzeby |

---

## Następne kroki (natychmiastowe)

1. **Max + Janusz** — Konfiguracja środowiska dev, klucze Google API, konto Vapi, start integracji Agent SDK
2. **Adam** — Organizacja zebranych danych Mike'a Grabowskiego w strukturalny format do ingestion
3. **Przemek + Mieszko** — Zdefiniowanie narracji demo, ~~start prac nad nazwą produktu~~ (ROZWIĄZANE: **Gemellus**), początek prezentacji
4. **Wszyscy** — Spotkanie za ~1 godzinę, przegląd postępów i iteracja nad przebiegiem demo
