# Vapi Assistant Source of Truth Design

## Context

Projekt ma już działające endpointy Vapi w backendzie FastAPI:
- `GET /vapi/assistant/{assistant_id}`
- `GET /vapi/phone-numbers`
- `POST /vapi/calls`

Kod jest rozdzielony na moduły:
- `api/routes_vapi.py`
- `api/service_vapi.py`
- `api/schemas_vapi.py`

Aktualnie integracja z Vapi używa ręcznie zbudowanego wrappera HTTP opartego o `httpx`. To działa, ale nie daje spójnego modelu zarządzania assistantem. Konfiguracja assistanta nadal żyje głównie w dashboardzie Vapi, a repo zna tylko `assistantId` przekazywane do endpointów.

To jest problem, bo kolejne kroki projektu wymagają:
- wersjonowania promptu, modelu, voice config i tools
- łatwego bootstrapu środowiska po pullu repo
- dodawania i review zmian w assistant config przez Git, a nie tylko przez dashboard

## Goal

Repo ma stać się source of truth dla jednego istniejącego assistanta Vapi o ID:

`f1941929-8416-486f-ba81-154de28fb7d1`

Po wdrożeniu:
- pełna specyfikacja assistanta będzie trzymana w repo
- backend będzie używał oficjalnego Python Server SDK Vapi zamiast ręcznego `httpx`
- będzie istniał jawny mechanizm `pull` i `push` między repo a Vapi
- dashboard Vapi będzie traktowany jako miejsce obserwacji/debugu, a nie edycji źródłowej

## Recommended Approach

Rekomendowany wariant to:

1. Użyć `VapiAI/server-sdk-python` jako jedynego klienta do API Vapi.
2. Trzymać jedną pełną specyfikację assistanta w repo jako JSON.
3. Dodać skrypt synchronizacyjny z dwoma trybami:
   - `pull`: pobiera aktualny stan assistanta z Vapi do pliku repo
   - `push`: aktualizuje istniejącego assistanta w Vapi na podstawie pliku repo
4. Zachować istniejące endpointy backendowe dla call flow, ale przepiąć je na SDK.

To jest wystarczająco proste na obecny etap i przygotowuje grunt pod tools bez robienia przedwczesnej abstrakcji na wielu assistantów lub wiele środowisk.

## Alternatives Considered

### 1. Snapshot only

Pobrać assistanta do repo jako podgląd, ale dalej traktować dashboard jako źródło zmian.

Dlaczego odrzucone:
- nie daje source of truth
- utrudnia review zmian promptu i tools
- powoduje dryf między repo a dashboardem

### 2. Source of truth rozbite na wiele plików

Trzymać prompt, model, tools i voice osobno, a finalny payload składać programowo.

Dlaczego odłożone:
- to ma sens długofalowo
- ale na dziś zwiększa złożoność bez realnego zysku
- jeden JSON jest lepszy na szybki bootstrap i synchronizację istniejącego assistanta

## Design

### 1. Assistant identity

Assistant jest jeden i zarządzany po stałym ID:

`VAPI_ASSISTANT_ID=f1941929-8416-486f-ba81-154de28fb7d1`

To ID trafia do env i do logiki synchronizacji. Nie wspieramy teraz tworzenia nowych assistantów ani wyboru między wieloma konfiguracjami.

### 2. Assistant config in repo

Repo będzie zawierać plik:

`config/vapi/assistant.json`

Plik ma zawierać pełny payload istotny dla `update assistant`, w szczególności:
- `name`
- `firstMessage` / analogiczne pola rozmowy, jeśli istnieją w obiekcie
- `model`
- `voice`
- `transcriber`
- `server` / `serverUrl`, jeśli assistant używa webhooków lub tools przez backend
- `tools`
- wszystkie inne pola potrzebne do zachowania semantyki bieżącego assistanta

Reguła:
- jeśli pole jest częścią definicji assistanta i ma znaczenie dla zachowania rozmowy, powinno być w repo
- pola runtime, metadane systemowe i server-generated IDs niezwiązane z definicją nie powinny być ręcznie utrzymywane, jeśli SDK/API ich nie wymaga przy update

### 3. Bootstrap flow

Pierwszy krok implementacji to `pull` istniejącego assistanta z Vapi do repo.

To robi z obecnej konfiguracji w dashboardzie punkt startowy, po którym:
- repo staje się źródłem prawdy
- dalsze zmiany idą przez edycję pliku i `push`

### 4. SDK integration

Ręczny wrapper `httpx` w `api/service_vapi.py` zostanie zastąpiony klientem z oficjalnego SDK.

Warstwa serwisowa nadal zostanie utrzymana, ale tylko jako cienki adapter dla projektu:
- tworzenie klienta z env
- mapowanie błędów SDK na `HTTPException`
- rozwiązywanie numeru telefonu po numerze lub po ID

To daje dwie korzyści:
- kod biznesowy backendu nie zależy bezpośrednio od kształtu SDK w route’ach
- testy mogą nadal stubować lokalny adapter bez pełnego mockowania zewnętrznej biblioteki

### 5. Sync mechanism

Zostanie dodany skrypt CLI, np.:

`api/scripts/sync_vapi_assistant.py`

Obsługiwane komendy:
- `pull`
- `push`

`pull`:
- czyta `VAPI_PRIVATE_KEY` i `VAPI_ASSISTANT_ID`
- pobiera assistanta przez SDK
- zapisuje znormalizowany JSON do `config/vapi/assistant.json`

`push`:
- czyta `config/vapi/assistant.json`
- waliduje, że spec jest obiektem JSON
- aktualizuje assistanta o `VAPI_ASSISTANT_ID` przez SDK

Opcjonalnie można dodać trzeci tryb:
- `diff` albo `validate`

Ale nie jest to wymagane na pierwszy etap.

### 6. Existing HTTP endpoints

Istniejące endpointy zostają:
- `GET /vapi/assistant/{assistant_id}`
- `GET /vapi/phone-numbers`
- `POST /vapi/calls`

Na razie nie zmieniamy ich kontraktu zewnętrznego.

Dodatkowo można dodać endpoint administracyjny dopiero później, jeśli będzie potrzebny:
- `POST /vapi/assistant/sync`

Na pierwszy etap lepszy jest skrypt CLI niż admin endpoint, bo:
- nie zwiększa powierzchni API
- nie wymaga zabezpieczania dodatkowej mutacji HTTP
- lepiej pasuje do workflow “zmień plik -> push config”

### 7. Tools readiness

Projekt zakłada przyszłe dodanie tools.

Dlatego assistant spec w repo musi być gotowa na:
- listę `tools`
- konfigurację server/webhook targetów
- prompt instructions opisujące, kiedy tool ma być wywoływany

To oznacza, że JSON assistanta ma być trzymany w formie możliwie bliskiej payloadowi Vapi, a nie w lokalnym custom DSL. W przeciwnym razie późniejsze dodawanie tools będzie generowało niepotrzebną warstwę translacji.

## File-Level Plan

### New files

- `config/vapi/assistant.json`
- `api/scripts/sync_vapi_assistant.py`

### Modified files

- `.env.example`
- `README.md`
- `api/requirements.txt`
- `api/service_vapi.py`
- `api/routes_vapi.py`
- `api/schemas_vapi.py`
- `api/tests/test_main.py` lub nowe testy podzielone na bardziej odpowiednie moduły

## Environment Variables

Docelowo wymagane:
- `VAPI_PRIVATE_KEY`
- `VAPI_ASSISTANT_ID`
- `VAPI_DEFAULT_PHONE_NUMBER`
- `VAPI_DEFAULT_PHONE_NUMBER_ID` opcjonalnie

`VAPI_ASSISTANT_ID` powinno być ustawione jawnie i wskazywać dokładnie:

`f1941929-8416-486f-ba81-154de28fb7d1`

## Error Handling

System powinien jasno rozróżniać:
- brak konfiguracji env
- błąd autoryzacji Vapi
- brak assistanta o oczekiwanym ID
- brak numeru telefonu odpowiadającego `VAPI_DEFAULT_PHONE_NUMBER`
- błąd walidacji pliku `assistant.json`

Zasada:
- błędy sync skryptu mają kończyć się niezerowym exit code i czytelnym komunikatem
- błędy runtime endpointów mają być mapowane na sensowne `HTTPException`

## Testing Strategy

### Unit tests

Testy powinny pokryć:
- tworzenie klienta Vapi z env
- `pull` assistanta do pliku
- `push` pliku do API
- rozwiązywanie `phoneNumberId` po numerze domyślnym
- outbound call przy użyciu SDK adaptera
- obsługę brakujących envów i błędnych danych

### Contract preservation

Istniejące endpointy `/vapi/*` powinny zachować obecny shape odpowiedzi na tyle, na ile to możliwe, żeby nie rozwalić istniejących ręcznych flow testowych.

### Manual verification

Po wdrożeniu trzeba ręcznie sprawdzić:
- `pull` dla assistanta `f1941929-8416-486f-ba81-154de28fb7d1`
- diff pliku repo po ręcznej edycji promptu
- `push`
- outbound call na numer testowy

## Risks

### 1. API shape mismatch between current raw HTTP and SDK

SDK może zwracać obiekty w nieco innym kształcie niż obecne ręczne `dict`.

Mitigacja:
- trzymać cienki adapter w `service_vapi.py`
- do route’ów zwracać jawnie serializowane `dict`

### 2. Pull writes too much server-generated data

Surowy obiekt assistanta może zawierać pola niepożądane w repo.

Mitigacja:
- w `pull` zrobić świadomą normalizację
- zapisywać tylko pola potrzebne do późniejszego `push`

### 3. Dashboard drift

Ktoś może zmienić assistanta ręcznie w dashboardzie po wprowadzeniu repo source of truth.

Mitigacja:
- jasno opisać workflow w README
- używać `pull` tylko do bootstrapu lub świadomego importu zmian

## Non-Goals

Na ten etap nie wchodzą:
- wielu assistantów
- environment-specific assistant specs
- UI do edycji assistanta
- automatyczne migracje między różnymi assistant IDs
- pełna orkiestracja tools backendowych

## Success Criteria

Implementację uznajemy za gotową, jeśli:
- backend używa oficjalnego `server-sdk-python`
- `VAPI_ASSISTANT_ID` jest jawnie skonfigurowane
- `config/vapi/assistant.json` istnieje i zawiera bieżącą specyfikację assistanta
- `pull` i `push` działają dla assistanta `f1941929-8416-486f-ba81-154de28fb7d1`
- outbound call dalej działa
- README opisuje workflow repo source of truth
