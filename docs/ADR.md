# Architecture Decision Records (ADR) – Projekt StudyStudent


## ADR 001: Wybór frameworka backendowego (FastAPI)


* **Status:** Przyjęty (Accepted)
* **Kontekst:** 
  Aplikacja wymaga wydajnego, łatwego w utrzymaniu backendu REST API, który umożliwia szybkie definiowanie punktów końcowych (endpointów), automatyczną walidację wejściowych danych oraz natychmiastową generację interaktywnej dokumentacji dla zespołu.

* **Decyzja:** 
  Zdecydujemy się na użycie frameworka **FastAPI** w języku Python.

* **Konsekwencje:**
  * **Zalety:**
    * Automatyczna walidacja danych wyjściowych i wejściowych dzięki integracji z biblioteką **Pydantic**.
    * Automatycznie generowana dokumentacja Open API (Swagger UI pod adresem `/docs`).
    * Wysoka wydajność oparta na standardach ASGI (`uvicorn`).
    * Prosta i czysta struktura kodu zgodna z paradygmatem obiektowym (OOP).
 
---

## ADR 002: Wybór narzędzia do statycznej analizy i formatowania kodu (Ruff)


* **Status:** Przyjęty (Accepted)
* **Kontekst:** 
  Projekt musi spełniać rygorystyczne standardy czystości kodu (PEP 8) oraz posiadać scentralizowaną konfigurację sprawdzaną w sposób automatyczny przez narzędzia typu linter/formatter.

* **Decyzja:** 
  Wybieramy narzędzie **Ruff** skonfigurowane w centralnym pliku `pyproject.toml`.

* **Konsekwencje:**
  * **Zalety:**
    * Bardzo wysoka szybkość działania (napisany w Rust).
    * Zastępuje wiele osobnych narzędzi (Flake8, isort, Black) w jednym systemie.
    * Scentralizowana konfiguracja w pliku `pyproject.toml`.
  * **Wady:**
    * Konieczność instalacji dodatkowej biblioteki w środowisku wirtualnym.

---

---

## ADR 003: Architektura interfejsu użytkownika (Vanilla HTML/JS serwowany z serwera)


* **Status:** Przyjęty (Accepted)

* **Kontekst:** 
  Projekt wymaga zademonstrowania interakcji klienta z przygotowanym REST API za pomocą prostego interfejsu graficznego.

* **Decyzja:** 
  Tworzymy lekki frontend w czystym języku HTML/JS (`index.html`) serwowany bezpośrednio przez FastAPI przy użyciu modułu `FileResponse`.

* **Konsekwencje:**
  * **Zalety:**
    * Brak konieczności budowania i konfiguracji zewnętrznych frameworków (Node.js/React).
    * Łatwe uruchomienie całego projektu za pomocą pojedynczej komendy lub przycisku F5.
    * Bezpośrednia komunikacja asynchroniczna z API poprzez wbudowaną funkcję `fetch()`.
  * **Wady:**
    * Ograniczona skalowalność interfejsu przy rozbudowie aplikacji do wielu skomplikowanych widoków.
