# Superset Env Setup Design

## Goal

Zautomatyzowac przygotowanie worktree w Superset tak, aby nowy workspace zawsze dostawal aktualne `.env` z glownego worktree bez recznego kopiowania.

## Scope

- Dodac projektowy config Superset w `.superset/config.json`.
- Dodac setup script, ktory podczas tworzenia workspace nadpisuje lokalne `.env` zawartoscia z `SUPERSET_ROOT_PATH/.env`.
- Zwracac czytelny blad, jezeli w root repo nie ma `.env`.
- Dodac prosty test integracyjny skryptu.

## Approach

Wybrany wariant to cienki `config.json`, ktory deleguje logike do `.superset/setup.sh`. Dokumentacja Superset zaleca taki podzial dla logiki wykraczajacej poza pojedyncze polecenie, a w tym przypadku chcemy miec jawne nadpisanie pliku, walidacje warunkow wejsciowych i latwy punkt rozbudowy.

Skrypt bedzie opieral sie na zmiennych `SUPERSET_ROOT_PATH` i `SUPERSET_WORKSPACE_PATH`, wiec zachowanie pozostanie zgodne z runtime Superset i nie bedzie zalezne od lokalnych sciezek developera.

## Testing

Dodany test uruchomi setup script w tymczasowym katalogu root/workspace i potwierdzi, ze:

- istniejące `.env` w workspace zostaje nadpisane,
- brak `.env` w root konczy sie bledem i czytelnym komunikatem.
