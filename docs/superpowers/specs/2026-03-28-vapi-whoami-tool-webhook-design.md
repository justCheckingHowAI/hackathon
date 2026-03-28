# Vapi WhoAmI Tool Webhook Design

## Context

Repo ma już:
- `config/vapi/assistant.json` jako source of truth dla zarządzanego assistanta Vapi
- backend FastAPI z endpointami `GET /vapi/assistant/{assistant_id}`, `GET /vapi/phone-numbers`, `POST /vapi/calls`
- workflow `pull` / `push` do synchronizacji konfiguracji assistanta z Vapi

Aktualny assistant ma prompt i konfigurację głosową, ale nie ma jeszcze działającego custom tool calling.

W kontekście demo Gemellus assistant ma odpowiadać jako klon Mike’a Grabowskiego. Sam prompt może to zasugerować, ale na potrzeby demo chcemy jawnie pokazać działający backendowy tool wywoływany z Vapi. Użytkownik wskazał pierwszy testowy use case:
- tool `whoami`
- odpowiedź: że assistant jest klonem Mike’a Grabowskiego, CTO & Founder w Callstack
- źródło publiczne: `https://www.callstack.com/team/mike-grabowski`

Dodatkowe wymagania:
- webhook musi dać się testować lokalnie
- lokalny testing ma działać przez `localtunnel`
- późniejszy deploy endpointu ma iść pod `api.gemellus.app`

## Goal

Dodać pierwszy działający custom tool Vapi oparty o `model.tools`, tak aby:
- `config/vapi/assistant.json` definiował tool `whoami`
- Vapi mogło wywołać backendowy webhook dla tego toola
- backend zwracał wynik w formacie oczekiwanym przez Vapi
- lokalny testing był prosty i powtarzalny
- rozwiązanie było gotowe do rozszerzenia o kolejne tools bez przebudowy podstaw

## Recommended Approach

Rekomendowany wariant:

1. Dodać `whoami` do `model.tools` bezpośrednio w `config/vapi/assistant.json`.
2. Użyć dedykowanego endpointu webhookowego:
   - `POST /vapi/tools/whoami`
3. Skonfigurować tool-specific `server.url` w definicji toola zamiast jednego wspólnego `assistant.server.url`.
4. Dopisać do promptu jednoznaczną instrukcję, kiedy assistant ma używać `whoami`.
5. Na start zwracać statyczny wynik tekstowy, bez zewnętrznych fetchy ani lookupów runtime.

To jest najlepszy wariant na obecny etap, bo:
- pokazuje prawdziwy tool calling end-to-end
- minimalizuje złożoność webhooków
- upraszcza lokalne debugowanie
- nie blokuje późniejszego przejścia na wspólny router toolsów

## Alternatives Considered

### 1. Wspólny webhook dla wszystkich eventów Vapi

Czyli jedno `assistant.server.url` i ręczne rozgałęzienie po `message.type`.

Dlaczego nie teraz:
- miesza `tool-calls` z innymi webhook eventami
- utrudnia debugowanie pierwszego demo
- nie daje żadnej przewagi przy pojedynczym `whoami`

### 2. Trzymać tools poza repo i podpinać je przez `toolIds`

Dlaczego odrzucone:
- użytkownik jawnie wybrał `model.tools`
- pogarsza review w Git
- rozbija source of truth między repo a dashboard Vapi

### 3. Budować od razu uniwersalny framework na wiele tooli

Np. osobna warstwa dispatchera, rejestr handlerów i wspólny kontrakt dla wszystkich tooli.

Dlaczego odłożone:
- to jest rozsądny kolejny krok, ale nie pierwszy
- dla jednego toola zwiększa koszt implementacji bez zysku dla demo

## Design

### 1. Assistant config

W `config/vapi/assistant.json` do sekcji `model` zostanie dodane:
- `tools`

Pierwszy tool:
- `type: "function"`
- `name: "whoami"`
- opis wskazujący, że tool służy do ustalenia, czyim klonem jest assistant
- brak wymaganych parametrów wejściowych
- `server.url` wskazujące na webhook backendu

Lokalnie `server.url` będzie ustawiane na URL tunelu, np.:
- `https://<twoj-subdomain>.loca.lt/vapi/tools/whoami`

Docelowo w deployu:
- `https://api.gemellus.app/vapi/tools/whoami`

Assistant prompt dostanie krótką, jednoznaczną instrukcję:
- gdy użytkownik pyta kim jesteś, czyim jesteś klonem, kogo reprezentujesz albo prosi o identyfikację persony, użyj toola `whoami`

To jest krytyczne, bo w Vapi samo dodanie toola nie gwarantuje jego wywołania.

### 2. Webhook contract

Backendowy endpoint:

`POST /vapi/tools/whoami`

Zakładany kontrakt requestu od Vapi:
- webhook przychodzi jako `message.type = "tool-calls"`
- payload zawiera listę tool calli
- każdy tool call ma własne `id` oraz `name`

Backend nie powinien próbować obsługiwać innych eventów na tym endpointcie.

Odpowiedź do Vapi ma mieć format:

```json
{
  "results": [
    {
      "toolCallId": "call-id-from-vapi",
      "result": "You are Mike Grabowski, CTO & Founder at Callstack. Public profile: https://www.callstack.com/team/mike-grabowski"
    }
  ]
}
```

Jeśli payload będzie niepoprawny albo nie będzie zawierał oczekiwanego `whoami`, endpoint zwróci nadal `200`, ale z wpisem `error` dla danego `toolCallId`, zamiast podnosić wewnętrzny wyjątek bez struktury odpowiedzi.

To upraszcza diagnostykę w Vapi i jest bezpieczniejsze dla tool-calling flow.

### 3. Returned content

Tool `whoami` będzie zwracał statyczny wynik tekstowy:
- assistant jest klonem Mike’a Grabowskiego
- Mike Grabowski jest `CTO & Founder` w `Callstack`
- odpowiedź będzie zawierać publiczny link do strony profilu

Na tym etapie nie robimy:
- dynamicznego pobierania danych z `callstack.com`
- walidacji sieciowej przy każdym wywołaniu
- rozbudowanego JSON-a z metadanymi

Powód:
- demo potrzebuje niezawodności i niskiej latencji
- twardo zakodowana odpowiedź jest wystarczająca dla pierwszego toola

### 4. Backend structure

Implementacja backendowa ma pozostać prosta:
- schemy request/response w `api/schemas_vapi.py`
- route w `api/routes_vapi.py`
- mała funkcja pomocnicza lub handler w module Vapi, bez tworzenia osobnego subsystemu narzędzi

Granice odpowiedzialności:
- route: odbiór requestu i zwrot odpowiedzi HTTP
- schemy: walidacja payloadu
- handler: mapowanie tool calla na wynik

Jeśli w następnym kroku dojdą kolejne tools, wtedy można wydzielić osobny moduł dispatchera.

### 5. Local testing flow

Lokalny testing ma działać bez deployu produkcyjnego.

Rekomendowany flow:

1. Uruchomić lokalne API na porcie backendu, np. `8001`.
2. Wystawić je publicznie przez `localtunnel`, np.:
   - `lt --port 8001`
3. Ustawić otrzymany URL tunelu w `config/vapi/assistant.json` jako `model.tools[...].server.url`.
4. Wykonać `push` assistanta do Vapi.
5. Wywołać rozmowę i zapytać assistanta, czyim jest klonem.

Opcjonalnie można równolegle używać `vapi listen` do podglądu webhook eventów, ale nie jest to wymagane dla działania dedykowanego tool webhooka.

### 6. Production flow

Po deployu backendu:
- `server.url` w toolu zostanie podmienione na `https://api.gemellus.app/vapi/tools/whoami`
- assistant config zostanie ponownie wypchnięty do Vapi

Nie planujemy osobnej gałęzi konfiguracji DEV/UAT/PROD w tym zadaniu. Na teraz wystarczy jawna zmiana URL-a w source-of-truth i ponowny `push`.

### 7. Error handling

System powinien rozróżniać:
- błędny shape requestu od Vapi
- brak `toolCallId`
- wywołanie nieobsługiwanego toola na tym endpointcie

Zasady:
- endpoint ma odpowiadać szybko
- brak zewnętrznych zależności runtime
- błędy mają być zwracane w strukturze zgodnej z Vapi tool results, jeśli tylko da się ustalić `toolCallId`
- testy mają pokryć happy path i podstawowy invalid payload path

## File-Level Plan

### Modified files

- `config/vapi/assistant.json`
- `api/routes_vapi.py`
- `api/schemas_vapi.py`
- `README.md`
- `api/tests/test_main.py`

### Optional new file

Może pojawić się mały moduł pomocniczy, jeśli uprości kod, ale nie jest wymagany.

## Testing Strategy

Testy powinny pokryć:
- poprawną odpowiedź `POST /vapi/tools/whoami` dla poprawnego `toolCallId`
- zwrot ustrukturyzowanego błędu dla nieobsługiwanego lub niepoprawnego payloadu
- brak regresji w istniejących endpointach `/vapi/*`

Manualny test end-to-end:
- lokalny backend
- `localtunnel`
- `push` assistanta
- rozmowa z assistantem z pytaniem o to, czyim jest klonem

## Out of Scope

Poza zakresem tego zadania:
- wspólny router dla wszystkich tooli
- weryfikacja podpisów webhooków Vapi
- dynamiczne źródła danych dla `whoami`
- wiele środowisk konfiguracyjnych
- pełna orkiestracja innych webhook eventów Vapi

## Success Criteria

Po zakończeniu:
- assistant config w repo zawiera działający `model.tools[whoami]`
- backend obsługuje webhook `POST /vapi/tools/whoami`
- lokalny test przez `localtunnel` działa
- po zadaniu pytania o to, czyim klonem jest assistant, Vapi wywołuje tool i assistant odpowiada jako Mike Grabowski
