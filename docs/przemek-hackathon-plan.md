# OrgBrain: Blueprint hackathonowy na wygraną

Ten pomysł projektowy trafia w autentyczną lukę rynkową wartą eksploracji. **Żadne istniejące narzędzie nie agreguje kompleksowo kanałów komunikacji, repozytoriów kodu i transkrypcji rozmów w celu wnioskowania o kompetencjach i planowania odejść.** Najbliższy konkurent, TechWolf (53 mln USD pozyskane, wspierany przez Workday i SAP), pobiera dane z Jiry i GitHuba, ale ledwo dotyka e-maili, transkrypcji rozmów czy Discorda. Opisana przez Ciebie funkcjonalność planowania odejść / bus-factor jest całkowicie nieobsługiwana. Przy właściwej 6–8-godzinnej egzekucji skupionej na angażującym demo voice-first zbudowanym na Vapi + Gemini, koncept ten uzyskuje **9/10 za dopasowanie do tematu** i ma silny potencjał wygranej.

Adresowalny rynek jest duży i szybko rośnie: sam workforce analytics to **rynek o wartości 2,4–3,5 mld USD rosnący w tempie 12–16% CAGR**, osadzony w szerszym ekosystemie talent intelligence o wartości 20–30 mld USD. Sygnał pilności jest ogłuszający — **87% firm raportuje luki kompetencyjne** (McKinsey), WEF nazywa luki kompetencyjne „największą barierą transformacji biznesowej", a organizacje tracą **31,5 mld USD rocznie** z powodu słabego dzielenia się wiedzą (IDC). Timing jest idealny: 85% pracodawców stosuje skills-based hiring (wzrost z 40% w 2020), ale zaledwie 16% faktycznie wykorzystuje dane o kompetencjach w decyzjach kadrowych (Deloitte 2025).

---

## Krajobraz konkurencyjny ma lukę w kształcie TechWolfa, którą możesz wykorzystać

Rynek skills intelligence to trzypoziomowy krajobraz: wyspecjalizowani vendorzy AI-first (Eightfold AI przy wycenie **2,1 mld USD**, Gloat zbliżający się do **1 mld USD**, TechWolf z **53 mln USD pozyskanymi**), inkumbenci HCM (Workday Skills Cloud, SAP SuccessFactors) oraz wschodzący gracze niszowi (Reejig, Fuel50, 365Talents). Fragmentacja rynku jest skrajna — żaden vendor nie posiada więcej niż ~13% udziału, a PEAK Matrix Everest Group z 2025 ocenia **29 dostawców** w samym skills intelligence.

TechWolf zasługuje na największą uwagę, bo jako jedyny duży gracz faktycznie wnioskuje o kompetencjach z artefaktów pracy, zamiast polegać na samodzielnie deklarowanych profilach. Pobiera dane z Jiry, Asany, GitHuba, Salesforce'a, Confluence'a i wymienia Slacka jako integrację, deklarując **~95% trafności** wnioskowania o kompetencjach. Workday i SAP zainwestowały w TechWolfa, de facto outsourcując najtrudniejszy problem techniczny. Josh Bersin porównał TechWolfa do „MuleSofta dla kompetencji" — middleware łączącego heterogeniczne systemy.

Ale kluczowa luka: **żadna platforma nie analizuje głęboko treści e-maili, transkrypcji spotkań/rozmów ani Discorda pod kątem mapowania kompetencji.** Eightfold (396 mln USD pozyskane) opiera się na CV i danych profilowych w stylu LinkedIn. Gloat (192 mln USD pozyskane) korzysta z systemów HR i samodzielnie deklarowanych umiejętności. Nawet TechWolf skupia się na ustrukturyzowanych narzędziach pracy, nie na nieustrukturyzowanej komunikacji. Warstwa transkrypcji rozmów — gdzie sygnały ekspertyzy są najbogatsze (wiedza domenowa demonstrowana w dyskusji real-time, podejście do rozwiązywania problemów, styl przywództwa) — to zasadniczo dziewiczy teren.

Nowsza kohorta startupów waliduje wykonalność techniczną, nie konkurując bezpośrednio. **Interloom** (Monachium, 16,5 mln USD pozyskane w marcu 2026) pobiera e-maile supportowe i tickety serwisowe, budując „grafy kontekstu" dla wiedzy operacyjnej. **Aware** (Columbus, używany przez Walmart, Deltę, Chevron) monitoruje wiadomości Slack/Teams pod kątem sentymentu i ryzyka — dowodząc, że mining komunikacji enterprise'owej działa na skalę, choć dla compliance, nie kompetencji. **Glean** (wycena 4,6 mld USD) buduje enterprise'owe grafy wiedzy z danych wewnętrznych, ale skupia się na wyszukiwaniu/retrieval, nie mapowaniu kompetencji. Żaden nie łączy pełnego stacka, który proponujesz: kanały komunikacji + repozytoria kodu + transkrypcje rozmów → wnioskowanie o kompetencjach → analiza luk → planowanie odejść.

Ryzyko prywatności jest realne i musi być zaadresowane nawet w pitchu hackathonowym. Funkcje monitorowania workplace'owego Aware wygenerowały znaczny backlash medialny na początku 2024. Każde rozwiązanie minujące dane komunikacyjne potrzebuje jasnego frameworku zgód, warstw anonimizacji i przejrzystego governance'u. Na hackathon wystarczy jeden slajd adresujący zasady „privacy by design" — wyróżni Was jako przemyślanych builderów.

---

## Liczby rynkowe, od których sędziowie nachylą się do przodu

Pitch-ready narracja pisze się sama z tymi statystykami. Rotacja pracowników kosztuje USA **2,9 bln USD rocznie**, a indywidualny koszt zastąpienia to **33–200% rocznego wynagrodzenia** w zależności od seniority stanowiska. Luki kompetencyjne zagrażają **8,5 bln USD potencjalnego globalnego przychodu** do 2030. A jednak mniej niż połowa organizacji ma jasny wgląd we własne kompetencje kadrowe (McKinsey), a **47% nadal śledzi kompetencje za pomocą arkuszy kalkulacyjnych** lub przestarzałych narzędzi HR.

Przyspieszenie popytu jest strukturalne, nie cykliczne. Future of Jobs Report 2025 WEF prognozuje **170 mln nowych ról utworzonych i 92 mln zlikwidowanych** do 2030, wymagając reskillingu na bezprecedensową skalę. IBM szacuje, że **40% siły roboczej** będzie wymagało reskillingu w ciągu trzech lat, a **82% pracowników** uważa, że będą musieli się przeszkalać co najmniej raz w roku. Firmy, które z sukcesem wdrożyły podejście skills-based, odnotowały poprawę retencji o **98%** (Deloitte), a wewnętrzna mobilność podniosła retencję do **7,4 roku vs 4,1 roku** bez niej.

Na hackathonowy pitch zakotwicz na trzech liczbach: **31,5 mld USD** (roczny koszt słabego dzielenia się wiedzą w USA, IDC), **42%** (wiedza instytucjonalna posiadana wyłącznie przez indywidualnego pracownika — wychodzi za drzwi, gdy odchodzi, Panopto), i **5–8 miesięcy** (czas, aż nowy pracownik osiągnie pełną produktywność). To ramuje problem jako pilny, uniwersalny i kosztowny.

---

## Budowanie z Vapi + Gemini: architektura, która faktycznie działa w 7 godzin

Architektura techniczna powinna opierać się na trzech warstwach: Vapi do orkiestracji głosu, Google ADK z Gemini do inteligencji agentowej i Neo4j do grafu wiedzy. To nie jest aspiracja — każdy komponent ma produkcyjnie gotowe SDK i darmowe plany odpowiednie na hackathon.

**Vapi** orkiestruje trzyczęściowy pipeline głosowy (speech-to-text → LLM → text-to-speech) z latencją poniżej 700ms. Natywnie wspiera Gemini jako backbone LLM i wystawia custom tool functions, które Twój backend może implementować. Kluczowa możliwość dla tego projektu to prymityw **Squads** w Vapi — orkiestracja wielu asystentów z zachowaniem kontekstu. Możesz routować między „Agentem zapytań o kompetencje", „Agentem oceny ryzyka" i „Agentem analizy luk", każdy wyspecjalizowany dla innej domeny wiedzy. Vapi Build Challenge 2025 przyciągnął **300+ zgłoszeń** z pulą nagród ponad 20 tys. USD; zwycięzca Talvin AI zbudował głosową ocenę kandydatów — bezpośrednio sąsiadujący use case.

**Google ADK** (Agent Development Kit) to idealny framework agentowy. Instalujesz przez `pip install google-adk[voice]`, definiujesz agentów jako klasy Pythona z tool functions i deployujesz na Cloud Run. ADK wspiera hierarchie multi-agent (sekwencyjne, równoległe, pętlowe) i streamuje przez Gemini Live API do dwukierunkowego głosu real-time. Użyj **Gemini 2.5 Flash** do niskolatencyjnych interakcji głosowych i **Gemini 3 Pro** (1M+ tokenów kontekstu, natywnie multimodalny) do zadań głębokiej analizy. **Gemini Embedding 2** — pierwszy natywnie multimodalny model embeddingowy — może mapować tekst, kod, audio i dokumenty w jedną zunifikowaną przestrzeń wektorową, idealną do wyszukiwania wiedzy cross-channel.

**Neo4j** dopełnia stack grafową bazą danych zoptymalizowaną pod zapytania relacyjne. Neo4j opublikował kompletny model grafowy zarządzania kompetencjami (`Person -[:HAS_SKILL]-> Skill`, `Person -[:CONTRIBUTES_TO]-> Project`, `Project -[:REQUIRES_SKILL]-> Skill`) i zbudował produkcyjny przykład wyciągający kompetencje z wewnętrznych kanałów Slacka za pomocą NLP. **AuraDB free tier** wspiera 200 tys. węzłów i 400 tys. relacji — więcej niż wystarczająco. Modele Text2Cypher Neo4j na Vertex AI Model Garden (oparte o Gemma 3) umożliwiają natural language graph queries, więc agent głosowy może tłumaczyć „kto zna Kubernetesa?" bezpośrednio na traversal Cypher.

Aby głos był centralny, a nie doklejony, każda interakcja powinna być voice-first: „Hej agencie, kto w zespole zna nasz system płatności?" wyzwala `search_skills` tool call → traversal grafowy Neo4j → rankingi z confidence scores wypowiedziane z powrotem. „Co się stanie, jeśli Sarah odejdzie?" wyzwala analizę `departure_impact` → traversal grafowy mapujący unikalne kompetencje Sarah, zależności projektowe i luki wiedzowe → ocena ryzyka narrowana, podczas gdy wizualizacja jednocześnie pojawia się na dashboardzie. Ten zsynchronizowany output głos-plus-wizualizacja to multimodalny moment, który wygrywa hackathony.

Rekomendowany pattern integracyjny na szybkość hackathonową: użyj Vapi z Gemini jako bezpośrednim providerem LLM, zdefiniuj 3–4 custom tools w Vapi, które wywołują Twój backend FastAPI, backend odpytuje Neo4j i zwraca strukturyzowane wyniki. Pomiń złożoność ADK Streaming, chyba że team jest pewny, że zdąży to podpiąć. Wypełnij Neo4j bogatym zestawem sample'owych danych (25–30 osób, 60+ kompetencji, 6–8 zespołów, 5 projektów) zamiast budować realny pipeline ingestion. Demo **jednej** live extrakcji — przepuść batch wiadomości Slacka przez Gemini do entity extraction i pokaż aktualizujący się graf — żeby udowodnić, że koncept działa.

---

## 7-godzinny plan egzekucji i jak wygrać demo

Najważniejszy strategiczny insight: **buduj pod demo, nie pod produkt.** Twój 3-minutowy skrypt demo to Twoja specyfikacja. Jeśli feature nie jest w demo, nie buduj go. Zwycięskie projekty hackathonowe jak Konveyor (Microsoft AI Agents Hackathon 2025, zwycięzca Python za 5 tys. USD — agentowy AI do transferu wiedzy) i Bits2Brain (wizualna „Mapa Gwiazd Wiedzy" z grafami wiedzy) wygrały robiąc jedną rzecz wyjątkowo dobrze, nie wiele rzeczy przeciętnie.

Alokacja godzina po godzinie:

- **Godziny 0–1** (Setup): Developerzy inicjują repo, konto Vapi, klucze Google AI API i boilerplate React/Next.js. Produkt/design definiuje skrypt demo, tworzy mock dane (50+ fake'owych wiadomości Slacka z sygnałami ekspertyzy) i szkicuje 3–4 ekrany dashboardu.
- **Godziny 1–3** (Core Build): Dev 1 konfiguruje agenta głosowego Vapi z system promptem i 3 function tools. Dev 2 buduje backend FastAPI — ingestuje mock dane, podpina zapytania Neo4j, wystawia endpointy API. Dev 3 (lub design lead) buduje shell dashboardu React z komponentami wizualizacji D3.js. Produkt finalizuje UI i zaczyna slide deck.
- **Godziny 3–5** (Integracja): Podłączenie agenta głosowego do backendu (zapytanie głosowe → API call → traversal grafowy → odpowiedź głosowa). Podpięcie frontendu do API, rendering heatmapy kompetencji i widoku ryzyka odejścia. Test pełnego flow demo end-to-end.
- **Godziny 5–6.5** (Polish): Wszyscy developerzy naprawiają bugi i utwardzają dokładną ścieżkę demo. Test flow demo **minimum 3 razy**. Produkt/design ćwiczy prezentację z timingiem.
- **Godzina 6.5** (Ubezpieczenie): **Nagraj backup video działającego demo.** To nie podlega negocjacji. Najlepsze zespoły zawsze mają Plan B.
- **Godziny 7–8** (Prezentacja): Zamroź kod, wyczyść stan przeglądarki, prezentuj.

### Skrypt demo — dokładny 3-minutowy łuk

Otwórz emocjonalnym hookiem: *„W zeszłym kwartale nasz lead engineer Sarah złożyła dwutygodniowe wypowiedzenie. Z dnia na dzień zdaliśmy sobie sprawę, że była jedyną osobą, która rozumiała nasz pipeline płatności, infrastrukturę AWS i trzy krytyczne integracje klientów. Odzyskanie tej wiedzy zajęło nam 4 miesiące i 120 000 dolarów w opłatach konsultingowych."* To trafia, bo każdy sędzia doświadczył utraty kluczowej osoby.

Potem live interakcja głosowa — to Twój moment „aha". Zadzwoń do agenta i zapytaj: *„Kto w naszym zespole ma głęboką wiedzę o naszym systemie przetwarzania płatności?"* Agent odpowiada naturalnie podając 2–3 nazwiska, poziomy pewności i, co kluczowe, **źródło tej wiedzy** („Na podstawie 47 wiadomości Slacka i 3 dokumentów designowych, Sarah Chen ma głęboką ekspertyzę; Mark ma powierzchowną znajomość"). Ta pojedyncza wymiana demonstruje, że AI potrafi zrozumieć nieustrukturyzowaną komunikację i zmapować ludzką wiedzę — sędziowie tego wcześniej nie widzieli.

Przełącz na dashboard pokazujący heatmapę kompetencji z czerwonymi wskaźnikami single-point-of-failure. Kliknij „Symuluj odejście" dla Sarah → natychmiastowa analiza wpływu: systemy zagrożone, członkowie zespołu z częściową wiedzą, szacowany czas odzyskania, sugerowany plan transferu wiedzy. Zamknij business case'em: *„Organizacje tracą ponad 30 000 USD na odchodzącego pracownika w kosztach transferu wiedzy. Zbudowaliśmy to z Vapi, Google Gemini i Neo4j w 7 godzin."*

---

## Poza hackathon: use case'y sygnalizujące realną firmę

Planowanie odejść jest przekonujące, ale szersze portfolio use case'ów sygnalizuje potencjał venture-scale.

**M&A due diligence** — prawdopodobnie najbardziej wartościowa sąsiednia aplikacja. 70% przejęć nie osiąga założonych celów (HBR), a **60% niepowodzeń transakcji wynika z problemów ludzkich** (Mercer), ale zaledwie 15% czasu due diligence poświęca się ocenie kapitału ludzkiego. Wyobraź sobie prześwietlanie DNA wiedzy celu akwizycyjnego przed podpisaniem: „80% wiedzy o kodzie żyje w 3 inżynierach, którzy już aktualizują LinkedIn."

**Incident response** — operacyjny killer use case. Podczas incydentu P1 o 3:00 w nocy, najkrytyczniejsze pytanie to zawsze „kto zna ten system?" Interfejs głosowy staje się naturalny i pilny: zadzwoń do agenta, zapytaj kto rozumie mikroserwis billingowy, dostań rankingi oparte na faktycznych commitach kodu i dyskusjach na Slacku. Historia Boeinga unaocznia to — Boeing stracił 28 000 doświadczonych pracowników podczas COVID, a wynikająca z tego utrata „wiedzy plemiennej o bezpieczeństwie" przyczyniła się bezpośrednio do incydentu z panelem drzwi 737 MAX. Utrata wiedzy w NASA jest jeszcze dramatyczniejsza: po zakończeniu programu Space Shuttle, NASA dosłownie utraciła zdolność odtworzenia inżynierii z ery lądowań na Księżycu.

**Akceleracja onboardingu** — adresuje **2,4 mln USD rocznych strat produktywności na 1000 pracowników** (Panopto) poprzez auto-generowanie przewodników „kogo pytać o co" z faktycznych wzorców komunikacji.

**Ocena gotowości AI** — aktualny i strategiczny use case: 75% organizacji stworzyło role wymagające AI, ale tylko 31% wdrożyło strategie (Aon 2024). Narzędzie może scorować zespoły pod kątem gotowości AI analizując faktyczne użycie narzędzi i dyskusje techniczne względem krzywych capability AI, znacznie trafniej niż ankiety self-reportowe.

Na hackathonowy pitch wspomnij 2–3 z tych use case'ów krótko na slajdzie „wizja", żeby zasygnalizować szerokość. Ale demo skupij całkowicie na core mapowaniu kompetencji i planowaniu odejść — **głębokość ponad szerokość wygrywa hackathony.**

---

## Podsumowanie: co czyni to zwycięzcą

Trzy czynniki zbiegają się, czyniąc ten koncept hackathonowy wyjątkowo silnym:

1. **Autentyczna luka rynkowa**: gap między miningiem danych z kanałów komunikacji a wnioskowaniem o kompetencjach jest realny, zwalidowany przez fundraise TechWolfa na 53 mln USD za częściowe rozwiązanie i przez konsensus analityków, że wnioskowanie o kompetencjach z faktycznych artefaktów pracy to kolejna granica branży.

2. **Naturalne dopasowanie multimodalne**: głos to intuicyjny interfejs do odpytywania wiedzy organizacyjnej („kto zna X?"), tekst dostarcza głębi (raporty, plany transferu), a wizualizacja unaocznia wzorce (heatmapy, grafy zależności) — to nie jest wymuszona multimodalność, ale organiczny design produktowy.

3. **Rezonans emocjonalny**: każdy sędzia, każdy manager, każdy inżynier doświadczył momentu, gdy kluczowy kolega odszedł i krytyczna wiedza wyparowała. „Historia Sarah" to nie hipoteza — to uniwersalne doświadczenie.

### Krytyczne priorytety egzekucji

- Wypełnij graf wiedzy przed hackathnem (nie marnuj godzin na ingestion danych)
- Uczyń interakcję głosową otwierającym momentem demo (pre-warm połączenie Vapi, skryptuj dokładne pytania, testuj 5+ razy)
- Zsynchronizuj odpowiedzi głosowe z aktualizacjami wizualizacji dashboardu przez WebSocket dla multimodalnego „wow"
- Nagraj backup demo video w godzinie 6 bez względu na wszystko

### Sugestie nazwy

**OrgBrain**, **KnowledgeGraph.ai** lub **Hivemind** — coś, co sygnalizuje inteligencję i skalę organizacyjną.

---

Jeśli uda Ci się nail'ować live zapytanie głosowe, które zwraca „Sarah ma głęboką ekspertyzę Kubernetes na podstawie 47 wiadomości Slacka i 12 code reviews", podczas gdy heatmapa jednocześnie podświetla ją jako single point of failure, stworzyłeś moment demo, który jest jednocześnie technicznie imponujący i emocjonalnie przekonujący. Tak się wygrywa hackathony.

