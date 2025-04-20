# Zasady migracji bazy danych SQLite

## 1. Tworzenie migracji
- Każda zmiana w strukturze bazy danych (np. nowe tabele, kolumny, zmiana typów danych) powinna być wprowadzana poprzez dedykowane pliki migracyjne, a nie bezpośrednią edycję bazy.
- Migracje powinny być wersjonowane i posiadać czytelne nazwy opisujące zmianę (np. `add_user_table`, `alter_meal_column`).

## 2. Zachowanie spójności danych
- Przed wykonaniem migracji należy wykonać kopię zapasową bazy danych.
- Migracje nie powinny powodować utraty istniejących danych bez wyraźnej potrzeby i odpowiedniej dokumentacji.

## 3. Narzędzia do migracji
- Zalecane jest używanie narzędzi migracyjnych kompatybilnych z SQLite, np. Alembic (dla SQLAlchemy), Flask-Migrate, lub dedykowanych skryptów migracyjnych.
- Skrypty migracyjne powinny być testowane na kopii bazy przed wdrożeniem na produkcji.

## 4. Edycja schematu
- Unikać ręcznych zmian w pliku `.db` SQLite.
- Wszelkie zmiany powinny być odzwierciedlone w modelach ORM oraz plikach migracyjnych.

## 5. Zarządzanie wersjami migracji
- Każda migracja powinna posiadać unikalny numer wersji lub znacznik czasu.
- Należy prowadzić rejestr wykonanych migracji (np. tabela `alembic_version` lub własna tabela migracji).

## 6. Rollback i naprawa migracji
- Każda migracja powinna mieć możliwość cofnięcia (rollback).
- W przypadku błędu migracji należy przywrócić kopię zapasową oraz przeanalizować przyczynę problemu.

## 7. Testowanie migracji
- Migracje powinny być testowane automatycznie (np. w ramach CI/CD) na testowej bazie danych.
- Po migracji należy uruchomić testy integracyjne, aby upewnić się, że aplikacja działa poprawnie z nowym schematem.

## 8. Dokumentacja
- Każda migracja powinna być opisana w dokumentacji projektu: co zmienia, dlaczego została wprowadzona, czy wymaga dodatkowych kroków.

## 9. Zgodność z SQLite
- Należy pamiętać o ograniczeniach SQLite (np. brak niektórych typów ALTER TABLE).
- W razie potrzeby migracje powinny wykorzystywać tymczasowe tabele i kopiowanie danych, zgodnie z dokumentacją SQLite.

## 10. Bezpieczeństwo
- Pliki migracyjne nie powinny zawierać danych wrażliwych ani haseł.
- Dostęp do narzędzi migracyjnych powinien być ograniczony do zaufanych użytkowników.