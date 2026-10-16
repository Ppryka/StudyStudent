# Feature Specification: Study Student – platforma kojarzenia studentów do wspólnej nauki

**Feature Branch**: `001-study-student-mvp`
**Status**: Draft
**Input**: Opis interesariusza: „Aplikacja webowa ułatwiająca studentom znalezienie osób do wspólnej nauki z konkretnych przedmiotów oraz nawiązywanie nowych znajomości na uczelni (tablica ogłoszeń, filtrowanie, profil studenta, mapa miejsc spotkań, sekcja społecznościowa „okienka”)”.

> Niniejsza specyfikacja opisuje **CO** system ma robić i **DLACZEGO**. Decyzje technologiczne (Python, framework webowy, baza danych, dostawca map) należą do `plan.md` i nie są tu przesądzane.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 – Profil studenta (Priority: P1)

Jako **student** chcę **uzupełnić profil o uczelnię, kierunek, rok studiów i preferencje nauki**, aby **inni studenci mogli ocenić, czy pasujemy do siebie jako partnerzy do nauki**.

**Why this priority**: Profil jest warunkiem wstępnym dla ogłoszeń i sekcji społecznościowej (autor ogłoszenia musi być identyfikowalny), a pola uczelni i kierunku zasilają domyślne filtry.

**Independent Test**: Zarejestrowany student uzupełnia i zapisuje profil, a następnie widzi go w trybie podglądu publicznego, bez użycia innych funkcji.

**Acceptance Scenarios**:

1. **Given** zalogowany student bez uzupełnionego profilu, **When** wybierze uczelnię i kierunek ze słownika, poda rok studiów od 1 do 5 i zapisze formularz, **Then** system zapisuje profil i wyświetla komunikat „Profil zapisany”.
2. **Given** zalogowany student w formularzu profilu, **When** spróbuje zapisać formularz bez wybranej uczelni, **Then** system nie zapisuje zmian i oznacza pole „Uczelnia” jako wymagane.
3. **Given** student z zapisanym profilem, **When** zaznaczy preferencje nauki (forma: stacjonarna / online, pora dnia, styl: cicha nauka / dyskusja) i zapisze, **Then** preferencje są widoczne w publicznym podglądzie profilu.
4. **Given** inny zalogowany student, **When** otworzy publiczny profil studenta, **Then** widzi imię, uczelnię, kierunek, rok i preferencje oraz nie widzi adresu e-mail.

---

### User Story 2 – Dodanie ogłoszenia nauki (Priority: P1)

Jako **student** chcę **dodać ogłoszenie z przedmiotem, kierunkiem, opisem problemu i formą spotkania**, aby **znaleźć osoby, które pomogą mi lub będą się ze mną uczyć danego przedmiotu**.

**Why this priority**: Rdzeń wartości produktu; bez ogłoszeń tablica i filtrowanie nie mają treści.

**Independent Test**: Student z uzupełnionym profilem publikuje ogłoszenie i widzi je jako pierwsze na liście „Moje ogłoszenia” oraz na tablicy.

**Acceptance Scenarios**:

1. **Given** zalogowany student z uzupełnionym profilem, **When** wypełni przedmiot, kierunek, opis problemu (20–1000 znaków), formę spotkania „online” i opublikuje ogłoszenie, **Then** ogłoszenie pojawia się na tablicy ze statusem „Aktywne” i datą publikacji.
2. **Given** zalogowany student w formularzu ogłoszenia, **When** wpisze opis krótszy niż 20 znaków, **Then** system blokuje publikację i wyświetla komunikat o minimalnej długości opisu.
3. **Given** zalogowany student bez uzupełnionego profilu, **When** wybierze „Dodaj ogłoszenie”, **Then** system przekierowuje go do formularza profilu z informacją, że profil jest wymagany.
4. **Given** aktywne ogłoszenie starsze niż 30 dni, **When** nastąpi dzienne przetwarzanie wygasania, **Then** ogłoszenie otrzymuje status „Wygasłe” i znika z tablicy.

---

### User Story 3 – Przeglądanie i filtrowanie ogłoszeń (Priority: P1)

Jako **student** chcę **filtrować ogłoszenia po uczelni, przedmiocie, lokalizacji i formie spotkania**, aby **szybko znaleźć tylko te propozycje nauki, które są dla mnie realne**.

**Why this priority**: Bez filtrowania tablica przestaje być użyteczna przy większej liczbie ogłoszeń; to druga połowa podstawowej pętli wartości (dodaj → znajdź).

**Independent Test**: Na zbiorze testowych ogłoszeń zastosowanie kombinacji filtrów zwraca wyłącznie pasujące rekordy.

**Acceptance Scenarios**:

1. **Given** tablica z ogłoszeniami z różnych uczelni, **When** student ustawi filtr „Uczelnia = Politechnika Warszawska”, **Then** lista zawiera wyłącznie ogłoszenia z tej uczelni.
2. **Given** ustawiony filtr uczelni, **When** student doda filtry „Przedmiot = Analiza matematyczna” i „Forma = stacjonarna”, **Then** lista zawiera wyłącznie ogłoszenia spełniające wszystkie trzy warunki jednocześnie.
3. **Given** student z udostępnioną lokalizacją, **When** ustawi filtr „Lokalizacja: do 2 km”, **Then** lista zawiera wyłącznie ogłoszenia stacjonarne z miejscem spotkania w promieniu 2 km.
4. **Given** kombinacja filtrów bez wyników, **When** student zastosuje filtry, **Then** system wyświetla komunikat „Brak ogłoszeń” i przycisk „Wyczyść filtry”.
5. **Given** ustawione filtry, **When** student odświeży stronę lub skopiuje jej adres, **Then** te same filtry są nadal zastosowane.

---

### User Story 4 – Miejsce spotkania na mapie (Priority: P2)

Jako **autor ogłoszenia stacjonarnego** chcę **wskazać na mapie dokładne miejsce zbiórki**, aby **uczestnicy bez dodatkowych pytań trafili w to samo miejsce**.

**Why this priority**: Zwiększa skuteczność spotkań stacjonarnych, ale ogłoszenia działają bez niej (forma online, opis tekstowy).

**Independent Test**: Autor ustawia pinezkę w ogłoszeniu stacjonarnym, a inny student widzi to samo miejsce na mapie w szczegółach ogłoszenia.

**Acceptance Scenarios**:

1. **Given** student tworzący ogłoszenie z formą „stacjonarna”, **When** kliknie punkt na mapie i doda opis „wejście główne biblioteki, 2 piętro”, **Then** ogłoszenie zapisuje współrzędne punktu i opis miejsca.
2. **Given** student tworzący ogłoszenie z formą „stacjonarna”, **When** spróbuje opublikować ogłoszenie bez wskazania punktu, **Then** system blokuje publikację i prosi o wskazanie miejsca na mapie.
3. **Given** student tworzący ogłoszenie z formą „online”, **When** otworzy formularz, **Then** sekcja mapy jest ukryta, a ogłoszenie można opublikować bez lokalizacji.
4. **Given** opublikowane ogłoszenie stacjonarne, **When** inny student otworzy jego szczegóły, **Then** widzi mapę z pinezką w zapisanym punkcie i opisem miejsca.

---

### User Story 5 – Znajomi na okienko (Priority: P2)

Jako **student** chcę **oznaczyć swoje okienko między zajęciami i zobaczyć innych studentów z mojej uczelni wolnych w tym samym czasie**, aby **poznać nowe osoby i dobrze wykorzystać przerwę**.

**Why this priority**: Funkcja społecznościowa budująca zaangażowanie; niezależna od tablicy ogłoszeń, ale niekrytyczna dla MVP nauki.

**Independent Test**: Dwóch studentów tej samej uczelni z nakładającymi się okienkami widzi się nawzajem na liście i może wysłać zaproszenie.

**Acceptance Scenarios**:

1. **Given** zalogowany student z profilem, **When** doda okienko „dziś 12:00–13:30, kampus główny”, **Then** okienko jest widoczne dla innych studentów tej samej uczelni do godziny jego zakończenia.
2. **Given** student A z okienkiem 12:00–13:30 i student B z okienkiem 13:00–14:00 na tej samej uczelni, **When** student A otworzy listę „Wolni teraz w okienku”, **Then** widzi studenta B z informacją o wspólnym czasie 13:00–13:30.
3. **Given** student widzący innego studenta na liście okienek, **When** wyśle zaproszenie „Kawa w bufecie?”, **Then** adresat otrzymuje powiadomienie w aplikacji z możliwością akceptacji lub odrzucenia.
4. **Given** student, który zablokował innego użytkownika, **When** zablokowany użytkownik przegląda listę okienek, **Then** blokujący student nie jest na niej widoczny.
5. **Given** okienko, którego godzina zakończenia minęła, **When** dowolny student otworzy listę okienek, **Then** to okienko nie jest wyświetlane.

---

### Edge Cases

- Uczelni lub przedmiotu nie ma w słowniku → student zgłasza propozycję wpisu; do czasu akceptacji ogłoszenie trafia do kategorii „Inne”. [NEEDS CLARIFICATION: kto moderuje słowniki uczelni i przedmiotów?]
- Student nie udostępnił lokalizacji przeglądarki → filtr „Lokalizacja” działa na podstawie ręcznie wybranego kampusu lub miasta.
- Dostawca map jest niedostępny → formularz ogłoszenia stacjonarnego pozwala zapisać tekstowy opis miejsca, a pinezkę można dodać później; szczegóły pokazują opis zamiast mapy.
- Nakładające się okienka tego samego studenta → system scala je w jeden przedział.
- Ogłoszenie zawiera treści obraźliwe lub dane osobowe osób trzecich → każdy student może je zgłosić; po 3 zgłoszeniach ogłoszenie jest ukrywane do weryfikacji.
- Usunięcie konta → ogłoszenia, okienka i zaproszenia użytkownika są usuwane lub anonimizowane (RODO, art. 17).

---

## Requirements *(mandatory)*

### Functional Requirements

**Profil (US-1)**
- **FR-001**: System MUST umożliwiać zalogowanemu studentowi utworzenie i edycję profilu z polami: uczelnia, kierunek, rok studiów, preferencje nauki.
- **FR-002**: System MUST wymagać pól uczelnia, kierunek i rok studiów przed zapisem profilu.
- **FR-003**: System MUST udostępniać publiczny podgląd profilu innym zalogowanym studentom, bez ujawniania adresu e-mail.

**Ogłoszenia (US-2)**
- **FR-004**: System MUST umożliwiać studentowi z uzupełnionym profilem dodanie ogłoszenia z polami: przedmiot, kierunek, opis problemu (20–1000 znaków), forma spotkania (stacjonarna / online / hybrydowa).
- **FR-005**: System MUST umożliwiać autorowi edycję, zamknięcie i usunięcie własnego ogłoszenia.
- **FR-006**: System MUST automatycznie oznaczać ogłoszenia jako „Wygasłe” po 30 dniach od publikacji.

**Tablica i filtrowanie (US-3)**
- **FR-007**: System MUST prezentować aktywne ogłoszenia w kolejności od najnowszych, z paginacją po 20 pozycji.
- **FR-008**: System MUST umożliwiać filtrowanie ogłoszeń po uczelni, przedmiocie, lokalizacji (promień od punktu) i formie spotkania, łącząc filtry koniunkcją (AND).
- **FR-009**: System MUST odzwierciedlać aktywne filtry w adresie URL.

**Mapa (US-4)**
- **FR-010**: System MUST wymagać wskazania punktu na mapie dla ogłoszeń o formie „stacjonarna” lub „hybrydowa” i zapisywać współrzędne (WGS84) oraz opcjonalny opis miejsca (do 200 znaków).
- **FR-011**: System MUST wyświetlać mapę z pinezką miejsca spotkania w szczegółach ogłoszenia stacjonarnego.

**Okienka (US-5)**
- **FR-012**: System MUST umożliwiać studentowi dodanie okienka (data, godzina od–do, kampus) i automatycznie ukrywać je po jego zakończeniu.
- **FR-013**: System MUST wyświetlać listę studentów tej samej uczelni z okienkiem nakładającym się na okienko użytkownika, wraz ze wspólnym przedziałem czasu.
- **FR-014**: System MUST umożliwiać wysłanie zaproszenia z krótką wiadomością (do 200 znaków) oraz jego akceptację lub odrzucenie przez adresata.
- **FR-015**: System MUST umożliwiać blokowanie użytkowników; zablokowani użytkownicy nie widzą okienek ani profilu blokującego.

**Wspólne**
- **FR-016**: System MUST wymagać uwierzytelnienia dla wszystkich funkcji tworzenia i edycji treści. [NEEDS CLARIFICATION: czy rejestracja ma być ograniczona do adresów e-mail w domenach uczelnianych?]
- **FR-017**: System MUST umożliwiać zgłoszenie ogłoszenia lub profilu jako nieodpowiedniego.

### Non-Functional Requirements

Klasyfikacja wg ramy ISO/IEC 25002:2024 i modelu jakości produktu ISO/IEC 25010:2023.

| ID | Charakterystyka (podcharakterystyka) | Wymaganie | Metryka i próg |
|---|---|---|---|
| **NFR-001** | Performance efficiency (Time behaviour) | Lista ogłoszeń z filtrami odpowiada szybko. | Czas odpowiedzi API p95 ≤ 500 ms, p99 ≤ 1 s przy 10 000 aktywnych ogłoszeń |
| **NFR-002** | Performance efficiency (Capacity) | System obsługuje szczyt sesji. | ≥ 500 równoczesnych użytkowników i ≥ 100 req/s przy błędach < 1% |
| **NFR-003** | Performance efficiency (Time behaviour) | Widok mapy ładuje się płynnie. | LCP ≤ 2,5 s (p75, sieć 4G) |
| **NFR-004** | Reliability (Availability) | Usługa jest dostępna w okresie akademickim. | Availability ≥ 99,5% miesięcznie (≤ 3 h 39 min niedostępności) |
| **NFR-005** | Reliability (Faultlessness) | Awarie zdarzają się rzadko. | MTBF ≥ 720 h |
| **NFR-006** | Reliability (Recoverability) | Awarie są szybko usuwane, dane nie giną. | MTTR ≤ 1 h; RPO ≤ 24 h; RTO ≤ 4 h |
| **NFR-007** | Reliability (Fault tolerance) | Awaria dostawcy map nie blokuje ogłoszeń. | 100% operacji CRUD ogłoszeń działa przy niedostępnym API map |
| **NFR-008** | Security (Confidentiality) | Dane osobowe są chronione zgodnie z RODO. | 100% ruchu po TLS ≥ 1.2; e-mail niewidoczny publicznie; 0 wycieków w testach |
| **NFR-009** | Security (Authenticity, Integrity) | Uwierzytelnianie i dane są odporne na typowe ataki. | Zgodność z OWASP ASVS 4.0 L1; hasła Argon2id/bcrypt; 0 podatności High/Critical w skanie SAST/SCA przed wydaniem |
| **NFR-010** | Interaction capability (Operability, Learnability) | Kluczowe zadania są proste. | SUS ≥ 75; ≥ 90% nowych użytkowników dodaje ogłoszenie w ≤ 2 min |
| **NFR-011** | Interaction capability (Inclusivity) | Interfejs jest dostępny. | WCAG 2.1 AA: 0 błędów krytycznych w audycie automatycznym |
| **NFR-012** | Flexibility (Adaptability) | Aplikacja działa na urządzeniach studentów. | Poprawne działanie na szerokościach 360–1920 px i w 2 ostatnich wersjach Chrome, Firefox, Safari, Edge |
| **NFR-013** | Compatibility (Interoperability) | Integracje są oparte na standardach. | API opisane w OpenAPI 3.x; współrzędne w WGS84 (EPSG:4326) |
| **NFR-014** | Maintainability (Testability, Modifiability) | Kod jest łatwy w utrzymaniu. | Pokrycie testami ≥ 80% linii; złożoność cyklomatyczna ≤ 10 na funkcję; 0 błędów lintera i kontroli typów w CI |

### Key Entities

- **Student**: konto użytkownika; e-mail, hasło (hash), data rejestracji, lista zablokowanych użytkowników.
- **Profil**: 1:1 ze Studentem; uczelnia, kierunek, rok studiów, preferencje nauki.
- **Uczelnia / Kierunek / Przedmiot**: słowniki; Przedmiot należy do Kierunku, Kierunek do Uczelni.
- **Ogłoszenie**: autor (Student), przedmiot, kierunek, opis problemu, forma spotkania, status (Aktywne / Zamknięte / Wygasłe / Ukryte), data publikacji, opcjonalne Miejsce spotkania.
- **Miejsce spotkania**: współrzędne (WGS84), opis tekstowy.
- **Okienko**: Student, data, godzina od–do, kampus.
- **Zaproszenie**: nadawca, adresat, okienko, wiadomość, status (Wysłane / Zaakceptowane / Odrzucone).
- **Zgłoszenie**: zgłaszający, obiekt (Ogłoszenie lub Profil), powód, data.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: ≥ 90% nowych użytkowników uzupełnia profil i publikuje pierwsze ogłoszenie w czasie ≤ 2 minut (test użyteczności, n ≥ 10).
- **SC-002**: ≥ 40% aktywnych ogłoszeń otrzymuje co najmniej jedną odpowiedź w ciągu 72 godzin od publikacji.
- **SC-003**: 95% zapytań z filtrami zwraca wynik w ≤ 500 ms przy 10 000 aktywnych ogłoszeń.
- **SC-004**: ≥ 80% uczestników spotkań stacjonarnych ocenia wskazanie miejsca jako „wystarczające do trafienia bez dopytywania” (ankieta po spotkaniu).
- **SC-005**: ≥ 25% użytkowników aktywnych w miesiącu dodaje co najmniej jedno okienko.
- **SC-006**: Dostępność usługi ≥ 99,5% w każdym miesiącu semestru.

---

## Review & Acceptance Checklist

- [x] Brak szczegółów implementacyjnych (języki, frameworki, API) w treści wymagań
- [x] Wymagania są testowalne i jednoznaczne
- [x] Kryteria sukcesu są mierzalne i niezależne od technologii
- [x] Każda historia użytkownika ma niezależny test i scenariusze akceptacji
- [ ] Wszystkie znaczniki `[NEEDS CLARIFICATION]` rozstrzygnięte
