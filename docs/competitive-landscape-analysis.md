# Analiza krajobrazu konkurencyjnego — Gemellus

**Data analizy:** 2026-03-28
**Zakres:** Narzedzia knowledge continuity + Skills intelligence / competency gap

---

## Podsumowanie wykonawcze

Rynek jest podzielony na dwa izolowane silosy: **narzedzia zarzadzania wiedza** (Kategoria A) i **platformy skills intelligence / talent marketplace** (Kategoria B). Zadne z istniejacych narzedzi nie laczy obu tych swiatow w jeden produkt. Jedyny czesciowy wyjmek to **Viven AI** (spinka od zalozycieli Eightfold, $35M seed od Khosla Ventures, pazdziernik 2025), ktory tworzy "cyfrowe blizniaki" pracownikow — ale skupia sie wylacznie na Q&A i nie generuje pakietow rekrutacyjnych.

**Kluczowa luka rynkowa:** Zaden produkt na rynku nie potrafi:
1. Sklonowac wiedzy konkretnej osoby z jej rzeczywistych artefaktow pracy (PR-y, Slack, spotkania, kod)
2. Przeksztalcic tej wiedzy jednoczesnie w zdolnosc Q&A ORAZ gotowe pakiety rekrutacyjne (opis stanowiska + zadania rekrutacyjne)
3. Udostepnic to jako voice agent, do ktorego mozna zadzwonic

---

## KATEGORIA A — Narzedzia Knowledge Continuity

### 1. Guru (getguru.com)

**Co robi:**
- Platforma knowledge management z AI Knowledge Agents
- Weryfikuje i utrzymuje wiedze firmowa automatycznie (auto-verification/unverification)
- 100+ integracji: Slack, Teams, Salesforce, Zendesk, Confluence, SharePoint
- Od 2026: wsparcie Slack MCP — dostep do wiadomosci Slack w czasie rzeczywistym
- Dostarcza odpowiedzi tam, gdzie zespol pracuje (Slack, przegladarka)

**Co robi z odchodzacymi pracownikami:**
- Wymaga od odchodzacych pracownikow recznego przeniesienia wlasnosci "Cards" na innych
- Zacheca do dzielenia sie wiedza, ale to **proces manualny** — odchodzacy musi sam opisac co wie
- NIE skanuje automatycznie artefaktow pracy (PR-ow, Slacka, spotkan) odchodzacego pracownika

**Czego NIE robi:**
- Nie wyciaga wiedzy automatycznie z pracy pracownika
- Nie tworzy opisow stanowisk ani zadan rekrutacyjnych
- Nie oferuje voice agenta / telefonu
- Wymaga ciaglego recznego utrzymania — "only as good as the work you put into it"
- Nie radzi sobie z dlugimi, zlozoymi dokumentami

**Opinie uzytkownikow:** 95% satysfakcji (2828 recenzji), ale uzytkownicy narzekaja na koniecznosc precyzyjnych slow kluczowych w wyszukiwaniu i ciagla potrzebe recznego utrzymania bazy.

**Cena:** Tiered SaaS, przystepne dla SMB

---

### 2. Tettra

**Co robi:**
- Wiki firmowe z AI botem odpowiadajacym na pytania w Slacku
- Integracje: Slack, Google Workspace, GitHub
- Markdown editing, version control
- Prosty, intuicyjny interfejs

**Czego NIE robi:**
- Slaba funkcja wyszukiwania w duzych bazach wiedzy
- Brak jednoczesnej edycji przez wielu uzytkownikow
- Minimalna personalizacja layoutow
- Ograniczone integracje z narzediami trzecimi vs konkurencja
- Brak zaawansowanego zarzadzania uprawnieniami
- **Nie analizuje artefaktow pracy, nie tworzy pakietow rekrutacyjnych, brak voice agenta**

**Opinie uzytkownikow:** Chwalony za latwosc uzycia i wsparcie techniczne, krytykowany za ograniczone wyszukiwanie.

**Cena:** Subskrypcja tiered, przystepna

---

### 3. Notion AI

**Co robi:**
- Baza wiedzy + AI search po calym workspace
- Enterprise Search indeksuje: Slack, Google Drive, GitHub, Jira, Teams, SharePoint, OneDrive
- Respektuje uprawnienia dostepu (SOC 2 Type 2, ISO 27001, GDPR)
- AI odpowiada na pytania z kontekstem calego workspace + podlaczonych narzedzi

**Czego NIE robi:**
- Problemy z wydajnoscia przy duzych zbiorach danych
- AI dostepne tylko w planach Business i Enterprise
- Nie analizuje PDF-ow bezposrednio (wymaga importu tekstu)
- **Nie klonuje wiedzy konkretnej osoby — przeszukuje cala baze bez personalizacji na eksperta**
- **Nie generuje opisow stanowisk, zadan rekrutacyjnych, brak voice agenta**

**Cena:** AI wlaczone od planu Business ($18/user/mo)

---

### 4. Glean (glean.com)

**Co robi:**
- Enterprise AI search po 100+ narzedziach (Google Drive, Slack, Teams, Jira, GitHub, Salesforce...)
- Asystent AI odpowiadajacy na pytania i streszczajacy dokumenty/watki
- Respektuje uprawnienia dostepu
- Agentic tasks: streszczanie backlogow, drafty Slack updates
- Twierdzenia o oszczednosci 110h/user/rok

**Czego NIE robi:**
- **Nie wykonuje akcji** — znajdzie odpowiedz, ale nie rozwiaze ticketa, nie wysledzi emaila
- Brak weryfikacji wiedzy — moze zwracac przestarzale wyniki sprzed 3 lat
- Wymaga connectorow — brak wsparcia = brak danych z danego zrodla
- Brak natywnej integracji w platformach komunikacyjnych
- **Nie klonuje wiedzy konkretnej osoby, nie generuje pakietow rekrutacyjnych, brak voice agenta**
- Zlozony setup, ograniczona personalizacja

**Opinie uzytkownikow:** Silny ranking i relevance, ale uzytkownicy narzekaja na cene, brak akcji, i wzrost kosztow 7-12%/rok przy odnowieniu.

**Cena:** ~$45-50+/user/mo, minimum ~$50-60K/rok, 100+ seats

---

### 5. Microsoft Viva Topics

**Status: WYCOFANY (luty 2025)**

- Microsoft zakonczyl Viva Topics 22 lutego 2025
- Zastapiony przez SharePoint + Microsoft Copilot
- Strony tematyczne wygenerowane przez AI przestaly byc dostepne
- Automatyczne rozpoznawanie tematow w Search, Office, Teams — wylaczone
- **Potwierdzenie ze nawet Microsoft nie znalazl sposobu na automatyczne odkrywanie wiedzy w skali — wraca do Copilota**

---

### 6. Shelf.io

**Co robi:**
- Knowledge automation dla contact center
- MerlinAI sluchajac pytan sugeruje odpowiedzi w search, self-service, chat, CRM
- Monitoruje jakosc tresci: sprzecznosci, przestarzale info, duplikaty
- GenAI Content Copilot — tworzenie/aktualizacja artykulow jednym klikiem
- Analytics: search behavior, feedback trends, content gaps

**Czego NIE robi:**
- Zaprojektowany specjalnie dla srodowisk contact center — **nie jest narzedziem ogolnym**
- Brak mozliwosci wiki
- Wyszukiwanie czasem zwraca mniej trafne wyniki
- Brak jednoczesnej edycji
- **Nie klonuje wiedzy pracownikow, nie tworzy pakietow rekrutacyjnych, brak voice agenta**

**Cena:** Enterprise, quote-based

---

### 7. Spekit

**Co robi:**
- Just-in-time learning dla zespolow sprzedazowych
- AI Sidekick: kontekstowy asystent surfujacy odpowiedzi w Salesforce, Gmail, Outlook, Chrome, Gong
- Deal Rooms, change alerts, quizzy
- 80% szybszy onboarding, 30-40% mniej ticketow support

**Czego NIE robi:**
- Wymaga duzej inwestycji czasu w tworzenie "Spekow"
- Skupiony na revenue enablement — **nie jest narzedziem ogolnego knowledge management**
- Problemy z precyzja umieszczania contentu
- **Nie analizuje artefaktow pracy, nie klonuje wiedzy, brak pakietow rekrutacyjnych**

**Status:** Aktywny, $19M revenue w 2024, acquisicja Cquence (AI startup)

---

### 8. Google NotebookLM

**Co robi:**
- AI research assistant: synteza informacji z uploadowanych dokumentow
- Studio: Audio/Video Overviews, Mind Maps, Slide Decks, Infographics, Quizzy
- "Deep Research" (od XI 2025) — agentic researcher
- Enterprise tier: NotebookLM Plus (SMB) i Enterprise (duze org.)
- VPC-SC compliant, dane nie sa uzywane do treningu modeli

**Czego NIE robi:**
- **Limit 50 zrodel/notebook** (300 Plus, 600 Ultra) — za malo dla klonowania calej wiedzy osoby
- Notebooki nie komunikuja sie miedzy soba — brak cross-notebook connections
- Brak eksportu z zachowaniem cytatow
- Nie wyswietla grafik z PDF-ow (tabele, wykresy, obrazy)
- Brak integracji z narzediami pracy (Slack, Jira, GitHub, CRM)
- **Wymaga recznego uploadu dokumentow — nie skanuje automatycznie artefaktow pracy**
- **Nie generuje opisow stanowisk, zadan rekrutacyjnych, brak voice agenta**
- Brak trybu offline
- Ograniczone wsparcie jezykowe

**Opinie uzytkownikow:** Uwielbiane Audio Overviews, ale uzytkownicy frustruja sie limitem zrodel i brakiem eksportu.

**Cena:** Free (50 sources), Plus ~$14/mo, Pro $19.99/mo, Enterprise custom

---

### 9. Viven AI (NAJBLIZSZY KONKURENT)

**Co robi:**
- **Cyfrowe blizniaki pracownikow** — LLM trenowany na decyzjach, komunikacji i wiedzy domenowej
- Integruje: email, Slack, Google Docs, kod, wiadomosci chat, spotkania
- Pairwise context & privacy — precyzyjnie kontroluje kto moze widziec jakie informacje
- Kazdy widzi historie zapytan do swojego bliznniaka (deterrent)
- Twins dzialaja tez jako personal assistant (status updates, meeting prep)
- Deployed w Genpact (140K pracownikow), Eightfold, Josh Bersin Company

**Czego NIE robi (KLUCZOWE):**
- **Nie generuje opisow stanowisk z pracy pracownika**
- **Nie tworzy zadan rekrutacyjnych / interview tasks**
- **Nie oferuje voice agenta — tylko text-based queries**
- **Nie laczy wiedzy z procesem hiring — to czyste Q&A**
- Bardzo wczesny produkt (seed stage, Q4 2025)
- Brak publicznych recenzji uzytkownikow — za wczesne na ocene
- Brak informacji o limitach skalowalnosci

**Cena:** Enterprise, nieopublikowana

**Relacja do Gemellus:** Viven to najblizszy konkurent w warstwie "klonowania wiedzy", ale adresuje TYLKO strone Q&A. Nie mysli o hiringu w ogole. To jest polowa tego, co Gemellus moze zrobic.

---

## KATEGORIA B — Skills Intelligence / Workforce Planning

### 1. Eightfold AI

**Co robi:**
- Talent Intelligence Platform: deep learning na 1.6B+ profili kariery i 1.6M+ umiejetnosci
- Inferuje umiejetnosci, potencjal i trajektorie kariery — wykracza poza keyword matching
- Scoring kandydatow 1-5 na bazie skills, potential, fit
- Agentic AI (2025-2026): screenuje kandydatow 24/7, prowadzi wstepne rozmowy
- Digital Twin (patrz Viven AI powyzej)
- Internal mobility, workforce planning

**Czy generuje job descriptions z rzeczywistej pracy?**
- Konwertuje JD na filtry skill-based, ale **nie generuje JD z artefaktow pracy odchodzacego pracownika**
- JD musi byc dostarczone — Eightfold optymalizuje, ale nie tworzy od zera

**Czy tworzy interview tasks z realnych projektow?**
- **NIE** — matchuje kandydatow do rol, ale nie generuje zadan rekrutacyjnych opartych na faktycznej pracy

**Ograniczenia:**
- Slabe analytics mimo nazwy "intelligence platform"
- Rekruterzy musza nawigowac pomiedzy Eightfold i ATS
- UI przytlaczajace dla nowych uzytkownikow
- Matchowanie czasem nietrafne
- Class action w Kalifornii (FCRA)
- Drogi: prohibitywny dla organizacji <2000 pracownikow

**Cena:** Enterprise, custom pricing

---

### 2. Gloat

**Co robi:**
- Internal Talent Marketplace: laczy pracownikow z projektami, gigs, mentorami, stanowiskami
- AI-powered Workforce Graph: deep learning o relacjach miedzy praca, skills i rolami
- Skills Foundation: harmonizuje dane z roznych zrodel
- Career Planning: AI przewiduje "nastepne 3-4 kroki" w karierze
- Person-centric approach (vs job-centric)

**Czy generuje JD z pracy pracownika?** **NIE**
**Czy tworzy interview tasks?** **NIE**

**Ograniczenia:**
- Wymaga, zeby pracownicy wypelnili profile — puste profile = brak rekomendacji
- Duzo pracy przygotowawczej na poczatku wdrozenia
- Ciagla praca utrzymaniowa po launchu (szkolenia, interakcje z uzytkownikami)
- Ograniczone dane o adopcji przez pracownikow

**Cena:** Enterprise, custom

---

### 3. Beamery

**Co robi:**
- Talent Lifecycle Management: od sourcingu po internal mobility i alumni
- Skills Intelligence: wspolny jezyk rol i umiejetnosci
- Ray — agentic AI consultant embedded w platformie
- Real-time workforce planning w Slack i Teams
- ISO 42001 (AI Management Systems)
- 4x redukcja cyklu hiring, 25% szybsze milestones

**Czy generuje JD z pracy pracownika?** **NIE** — uzywa skills data do matchowania, ale JD trzeba dostarczyc
**Czy tworzy interview tasks?** **NIE**

**Ograniczenia:**
- Trudnosci techniczne raportowane przez uzytkownikow
- Obawy o tempo rozwoju wzgledem celow wzrostu

**Cena:** Enterprise, nieopublikowana

---

### 4. Phenom

**Co robi:**
- Talent Experience Platform: AI personalizacja calego lifecycle (rekrutacja → retencja)
- Chatbot konwersacyjny dla kandydatow
- X+ Agents: sourcing, matchowanie, career pathing (multi-model GenAI)
- Digitalizacja skills, job architectures, profili pracownikow
- Identyfikacja skill/competency gaps na poziomie departamentu
- Akwizycja Be Applied (2026) — adaptive skills validation

**Czy generuje JD z pracy pracownika?** **NIE** — optymalizuje istniejace JD
**Czy tworzy interview tasks z realnych projektow?** **NIE** — ale Be Applied dodaje skills validation

**Ograniczenia:**
- AI matchowanie mogloby byc trafniejsze
- Brak publicznego API
- Skupiony na acquisition > knowledge retention

**Cena:** Enterprise, custom

---

### 5. Fuel50

**Co robi:**
- Talent Intelligence + Internal Mobility z I/O psychology
- 5000+ capabilities ontology budowana przez psychologow i data scientists
- AI-powered marketplace: gigs, projekty, coaching, mentoring, wakaty
- Career DNA: skills + aspiracje + wartosci + agility
- Executive analytics: skills distribution, hot skills trends, retention risks

**Czy generuje JD z pracy pracownika?** **NIE**
**Czy tworzy interview tasks?** **NIE**

**Ograniczenia:**
- Wymaga ustalonej job architecture
- Trudne dla agencji staffingowych i contingent workforce
- Zlozone wdrozenie, problemy z integracjami
- Wyzwania z widocznoscia dla managerow

**Cena:** Enterprise, 2000+ pracownikow

---

### 6. Lightcast (dawniej Emsi Burning Glass)

**Co robi:**
- Labor Market Intelligence: 2.5B+ job postings, 800M+ career profiles, 100+ government sources
- Open Skills taxonomy: 32,000+ umiejetnosci
- Compensation benchmarking, talent supply/demand analysis
- Career pathways, competitive intelligence
- 165+ krajow pokrycia (ekspansja 2025-2026)

**Czy generuje JD z pracy pracownika?** **NIE** — dostarcza dane rynkowe do tworzenia JD, ale nie analizuje artefaktow pracy
**Czy tworzy interview tasks?** **NIE**

**Charakter:** To zrodlo danych rynkowych, nie narzedzie operacyjne. Informuje o trendach, nie dziala na artefaktach pracy.

---

### 7. Heidrick Navigator

**Co robi:**
- Leadership Intelligence Platform: ocena i matchowanie liderow
- Powered by Eightfold.ai technology
- Unlimited assessments, real-time progress tracking
- Heidrick Immersive (marzec 2026): AI-driven symulacje inflection points
- Obserwuje jak liderzy mysla, decyduja i dzialaja pod presja

**Czy generuje JD z pracy pracownika?** **NIE** — ocenia liderow, nie generuje JD
**Czy tworzy interview tasks?** Symulacje sa formm assessmentu, ale **generyczne, nie oparte na realnych projektach firmy**

**Charakter:** Niszowy — skupiony wylacznie na C-level / leadership, nie na szerokiej rekrutacji.

---

### 8. LinkedIn Talent Insights

**Co robi:**
- Dane z 1B+ profili, 58M firm, 20M+ ofert pracy
- Talent pool analysis: dostepnosc skills w regionach/branzach
- Company reports: sklad workforce, talent flow, attrition, skills
- Competitive intelligence: trendy hiring konkurencji
- Employer branding metrics

**Czy generuje JD z pracy pracownika?** **NIE**
**Czy tworzy interview tasks?** **NIE**

**Ograniczenia:**
- "Dane czuja sie ograniczone, brakuje glebokosci do strategicznych decyzji"
- Ograniczona personalizacja raportow
- Brak API
- Ograniczenia licencyjne miedzy markami w tej samej firmie
- **Insights oparte na publicznych profilach LinkedIn — nie na faktycznej pracy**

---

## ANALIZA LUKI RYNKOWEJ

### Co potrafi KAZDE istniejace narzedzie:

| Mozliwosc | Guru | Glean | NotebookLM | Viven | Eightfold | Gloat | Phenom | Lightcast |
|---|---|---|---|---|---|---|---|---|
| Przeszukiwanie bazy wiedzy | TAK | TAK | TAK | TAK | - | - | - | - |
| AI Q&A z dokumentow | TAK | TAK | TAK | TAK | - | - | - | - |
| Integracja z narzedziami pracy | TAK | TAK | NIE | TAK | TAK | TAK | TAK | - |
| Skills mapping/ontology | - | - | - | - | TAK | TAK | TAK | TAK |
| Talent matching | - | - | - | - | TAK | TAK | TAK | - |
| Internal mobility | - | - | - | - | TAK | TAK | TAK | - |
| Labor market data | - | - | - | - | - | - | - | TAK |

### Czego NIE potrafi ZADNE istniejace narzedzie:

| Brakujaca mozliwosc | Status na rynku |
|---|---|
| **Automatyczne klonowanie wiedzy z artefaktow pracy (PRy, Slack, spotkania, kod)** | Viven AI czesciowo (text Q&A), ale brak glebokiej analizy kodu/PR-ow |
| **Generowanie opisu stanowiska z rzeczywistej pracy odchodzacego pracownika** | ZADEN produkt na rynku |
| **Tworzenie zadan rekrutacyjnych opartych na realnych projektach** | ZADEN produkt na rynku |
| **Polaczenie knowledge continuity Z procesem hiring w jednym produkcie** | ZADEN produkt na rynku |
| **Voice agent do "zadzwonienia" i uzyskania odpowiedzi od klonu** | ZADEN produkt na rynku laczy voice z knowledge cloning |
| **Identyfikacja "czego brakuje" po odejsciu pracownika → automatyczna konwersja na JD** | ZADEN produkt na rynku |

---

## PRZEWAGA GEMELLUS — CO MOZE ZROBIC INACZEJ

### Silo #1: Knowledge Continuity (Guru, Glean, NotebookLM, Viven)
- Te narzedzia **przeszukuja to, co juz zostalo zapisane** — ale 80% wiedzy eksperckiej jest tacit knowledge, ktore nigdy nie zostalo udokumentowane
- Guru wymaga recznego tworzenia "Cards" — odchodzacy pracownik musi SAM opisac co wie
- Glean przeszukuje istniejace dokumenty, ale nie rozumie KONTEKSTU decyzji
- NotebookLM wymaga recznego uploadu — nie laczy sie z narzedziami pracy
- **Viven jest najblizszy**, ale ograniczony do text Q&A i nie laczy wiedzy z hiringiem

### Silo #2: Skills Intelligence (Eightfold, Gloat, Beamery, Phenom)
- Te narzedzia **operuja na abstrakcyjnych skills taxonomy** — 32,000 umiejetnosci w Lightcast, 1.6M w Eightfold
- Ale **nie wiedza CO KONKRETNIE robil dany pracownik** — wiedza tylko jakie "labels" pasuja do jego profilu
- Job descriptions sa tworzone z szablonow lub optymalizowane z istniejacych — **nie generowane z realnej pracy**
- Interview tasks sa generyczne — **nie oparte na prawdziwych projektach, PR-ach, decyzjach architektonicznych**

### Gemellus wypelnia luke miedzy silowami:

```
ARTEFAKTY PRACY PRACOWNIKA
(PR-y, Slack, spotkania, kod, dokumenty)
          |
          v
   [GEMELLUS ENGINE]
          |
    +-----+-----+
    |             |
    v             v
KNOWLEDGE       HIRING
CONTINUITY      PACKAGE
    |             |
    v             v
- Voice Q&A   - Job Description
- Text Q&A      z faktycznej pracy
- "Zadzwon    - Interview tasks
  do eksperta"   z realnych projektow
                - Skills gap analysis
                  z artefaktow
```

### Konkretne przewagi Gemellus nad kazda kategorima:

**vs Viven AI (najblizszy konkurent):**
- Gemellus: voice agent (zadzwon i zapytaj) vs Viven: tylko text
- Gemellus: generuje pakiety rekrutacyjne vs Viven: tylko Q&A
- Gemellus: analizuje kod i PR-y gleboko vs Viven: ogolne dokumenty i emaile
- Viven ma $35M funding i Genpact jako klienta — Gemellus musi szybko dzialac

**vs Glean:**
- Gemellus: personalizowany na konkretna osobe vs Glean: przeszukuje cala firme
- Gemellus: voice interface vs Glean: brak
- Gemellus: tworzy JD i interview tasks vs Glean: brak
- Glean: $50K+/rok minimum vs Gemellus: potencjalnie bardziej przystepny

**vs Eightfold + skills platforms:**
- Gemellus: JD z realnej pracy (bottom-up) vs Eightfold: JD z taxonomy (top-down)
- Gemellus: interview tasks z prawdziwych projektow vs Eightfold: generyczne matching
- Gemellus: "co ta osoba NAPRAWDE robia" vs Eightfold: "jakie labels pasuja do profilu"

---

## PODSUMOWANIE KRYTYCZNE

### Rynek w marcu 2026:
1. **Knowledge management jest dojrzaly** — ale wszystkie narzedzia wymagaja recznego tworzenia i utrzymania wiedzy
2. **Viven AI to sygnalowy konkurent** — waliduje rynek digital twins pracownikow, ale skupia sie na Q&A
3. **Skills intelligence jest dojrzaly** — ale operuje na abstrakcjach, nie na faktycznej pracy
4. **NIKT nie laczy obu swiatow** — to jest otwarta luka
5. **Voice interface dla wiedzy eksperckiej** — voice agenci istnieja (Bland.ai, Synthflow, Retell), ale zaden nie jest polaczony z klonowaniem wiedzy pracownika
6. **Microsoft poddal sie z Viva Topics** — automatyczne odkrywanie wiedzy jest trudne; kto to zrobi dobrze, wygra

### Najwazniejsze ryzyka:
- **Viven AI** moze dodac hiring features — maja zespol i funding
- **Eightfold** moze polaczyc Digital Twin z Talent Intelligence — maja oba komponents
- **Glean** moze dodac personalizacje per-person — maja dane i integracje
- **Privacy/compliance** — klonowanie wiedzy z emaili i Slacka to pole minowe regulacyjne (Viven adresuje to "pairwise context")

### Rekomendacja pozycjonowania Gemellus:
**"Od artefaktow pracy do pelnego pakietu ciaglosci — wiedza + rekrutacja w jednym"**

Unikalna propozycja wartosci: jedyny produkt, ktory automatycznie transformuje rzeczywista prace pracownika w (1) callowanlnego voice agenta wiedzy i (2) gotowy pakiet rekrutacyjny na zastepstwo.

---

## Zrodla

### Kategoria A — Knowledge Continuity
- [Guru Features](https://www.getguru.com/features)
- [Guru Offboarding Blog](https://www.getguru.com/blog/how-guru-helps-guru-offboard-employees)
- [Guru Review - Siit.io](https://www.siit.io/tools/trending/guru-review)
- [Tettra Reviews - Capterra](https://www.capterra.com/p/167522/Tettra/reviews/)
- [Tettra Review - Research.com](https://research.com/software/reviews/tettra)
- [Notion AI Enterprise Search](https://www.notion.com/product/enterprise-search)
- [Notion AI Review 2026](https://max-productive.ai/ai-tools/notion-ai/)
- [Glean AI Review - Fritz.ai](https://fritz.ai/glean-review/)
- [Glean Reviews - eesel.ai](https://www.eesel.ai/blog/glean-reviews)
- [Glean Review - Workativ](https://workativ.com/ai-agent/blog/glean-review)
- [Microsoft Viva Topics Retirement](https://learn.microsoft.com/en-us/microsoft-365/topics/changes-coming-to-topics)
- [Viva Topics Retired FAQ - ClearPeople](https://www.clearpeople.com/blog/viva-topics-retired-faqs)
- [Shelf.io Reviews - G2](https://www.g2.com/products/shelf-shelf/reviews)
- [Spekit JIT Learning](https://www.spekit.com/just-in-time-learning)
- [NotebookLM Limitations - Atlas](https://www.atlasworkspace.ai/blog/notebooklm-limitations)
- [NotebookLM Review - Prezent.ai](https://www.prezent.ai/blog/notebooklm-review)
- [NotebookLM Evolution - Medium](https://medium.com/@jimmisound/the-cognitive-engine-a-comprehensive-analysis-of-notebooklms-evolution-2023-2026-90b7a7c2df36)

### Kategoria B — Skills Intelligence
- [Eightfold AI Review - MindHunt](https://mindhuntai.com/blog/eightfold-ai-review)
- [Eightfold Digital Twin - Engineering Blog](https://eightfold.ai/engineering-blog/agentic-operating-system-digital-twins/)
- [Viven AI - TechCrunch](https://techcrunch.com/2025/10/15/eightfold-co-founders-raise-35m-for-viven-an-ai-digital-twin-startup-for-querying-unavailable-coworkers/)
- [Viven AI - Official](https://viven.ai/)
- [Josh Bersin - Digital Twin](https://joshbersin.com/2025/10/arriving-now-the-digital-twin/)
- [Gloat Platform](https://gloat.com/)
- [Gloat Reviews - Gartner](https://www.gartner.com/reviews/market/internal-talent-marketplaces/vendor/gloat/product/gloat)
- [Beamery Platform](https://beamery.com/)
- [Beamery Reviews - Gartner](https://www.gartner.com/reviews/market/candidate-relationship-management-crm-software/vendor/beamery/product/beamery-talent-lifecycle-management-platform)
- [Phenom Platform](https://www.phenom.com/)
- [Phenom Be Applied Acquisition](https://www.reworked.co/talent-management/phenom-acquires-be-applied-for-skills-first-hiring/)
- [Fuel50 Skills Gaps](https://fuel50.com/2026/02/how-fuel50-makes-skills-gaps-visible/)
- [Fuel50 Reviews - OutSail](https://www.outsail.co/post/fuel50-reviews---pricing-pros-cons-and-user-feedback)
- [Lightcast Data](https://lightcast.io/products/data/overview)
- [Heidrick Navigator](https://www.heidrick.com/en/products/heidrick-navigator)
- [Heidrick Immersive Launch](https://heidrick.mediaroom.com/2026-03-23-Heidrick-Struggles-Launches-Heidrick-Immersive,-an-AI-Enhanced-Platform-for-Observing-Leadership-in-Motion)
- [LinkedIn Talent Insights](https://business.linkedin.com/talent-solutions/talent-insights)
- [LinkedIn Talent Insights Reviews - G2](https://www.g2.com/products/linkedin-talent-insights/reviews)

### Tacit Knowledge & Market Gap
- [Tacit Knowledge Competitive Moat - California Management Review](https://cmr.berkeley.edu/2026/03/tacit-knowledge-is-your-next-competitive-moat/)
- [AI in Tacit Knowledge Capture - ResearchGate](https://www.researchgate.net/publication/391962459)
- [AI Knowledge Management Challenges - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0040162525002148)
- [Knowledge Transfer in Software Teams - CISIN](https://www.cisin.com/coffee-break/knowledge-transfer-in-software-teams.html)
