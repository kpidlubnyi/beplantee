# Dokumentacja do strony internetowej BePlantee

## Moduły systemu projektu
### 1. Moduł autentyfikacji

- Obsługuje logowanie i rejestrację użytkownika.

- Zapewnia bezpieczeństwo danych.

- Obsługuje sesje/logowanie tokenowe.

### 2. Moduł bazy danych

- Obsługuje komunikację z bazą danych (MariaDB).

- Przechowuje dane o użytkownikach, roślinach, czynnościach pielęgnacyjnych, zdjęciach.

### 3. Moduł zarządzania roślinami

- Dodawanie, edycja i usuwanie roślin użytkownika.

-  Przypisywanie zdjęć do roślin.

-   Pobieranie informacji pielęgnacyjnych o roślinach (z bazy danych).

### 4. Moduł harmonogramu działań

-   Rejestracja i wykonanie czynności pielęgnacyjnych: podlewanie, nasłonecznianie itd.

-   Zapisywanie daty ostatniej pielęgnacji.

### 5. Moduł interfejsu użytkownika

-   Wyświetlanie listy roślin i ich szczegółów.

-   Formularze logowania, dodawania roślin, wykonywania czynności.

-   Możliwość przesyłania zdjęć.

## Potencjalne problemy 

#### - Ryzyko SQL Injections.
#### - Konieczność hashowania danych do logowania, szczególnie hasła.
#### - Ogranieczenia dotyczące rozmiaru przesyłanych plików.
#### - Potrzeba optymalizacji bazy danych.
#### - Trudności w znalezieniu odpowienich informacji lub obsłudze API.

## Czasochłonośc projektu

### Moduł autentyfikacji
- Implementacja logowania i rejestracji - 12 rg.
- Zabezpieczenie haseł - 6 rg.
- Obsługa sesji oraz tokenów - 6 rg.
- Testy / debugging - 8 rg.
**Łącznie - 32 rg.**

### Moduł bazy danych

- Projektowanie schematu - 6 rg.
- Implentacja połączenia, optymalizacja zapytań - 3 rg.
- Testy i debugging - 6 rg.
**Łącznie - 15 rg.**

### Moduł zarządzania roślinami

- Implementacja CRUD - 25 rg.
- Integracja API - 12 rg.
- Testy i debbuging - 10 rg.
**Łącznie - 46 rg.**

### Moduł harmonogramu działań

- Projektowanie UI/UX - 16 rg.
- Implementacja widoków, formularzy, responsywności - 16 rg.
- Testy i debbuging - 10 rg.
**Łącznie - 42 rg.**

### Dodatkowo

- Konfiguracje serwera i wdrożenie - 10 rg.
- Dokumentacja końcowa - 16 rg.
- Testowanie i naprawa błędów - 24 rg.

**Łącznie - 50 rg.**

***Łącznie - 185 rg.***

## Wymagania srzętowe oraz ludzkie

### Frontend (Hleb Shyn)

1. HTML5, CSS3.
2. Framework frontendowy (React).
3. Doświadczenie w tworzeniu responsywnych interfejsów.

### Backend (Kostiantyn Pidlubnyi)

1. Znajomość wybranych języków programowania (Python, JavaScript).
2. Doświadczenie pracy z MariaDB/MySQL.
3. Znajomość wzorców projektowych.
4. Doświadczenie w API REST.

### Dodatkowo (Kostiantyn Pidlubnyi)

- Umiejętność konfiguracji serwerów.

### Zasoby sprzętowe

1. Stacje robocze (laptopy).
2. IDE, systemy kontroli wersji.
3. Aplikacja do komunikacji zespołowej (Microsoft Teams).
4. Narzędzia do testowania.

### Zasoby dodatkowe

- Dostęp do API.

## Czas realizacji projektu

### Faza 1. Przygotowanie (1 tydzień)

- Wybranie technologii.
- Projektowanie architektury.
- Tworzenie schematu bazy danych.
- Przygotowanie repozytorium.

### Faza 2. Implementacja modułów podstawowych (2-3 tygodnie)

- Implementacja modułu bazy danych.
- Testy podstawowych zapytań.
- Implementacja modułu autentyfikacji.
- Implementowanie mechanizmów hashowania haseł.

### Faza 3. Implementacja modułów głównych funkcjonalności (4-5 tygodni)

- Implementacja modułu zarządzania roślinami.
- Implementacja modułu harmonogramu działań.
- Testy

### Faza 4. Implementacja interfejsu użytkownika (2-3 tygodnie)

- Implementacja UI.

### Faza 5. Integracja, testy i wdrożenie (3-4 tygodnie)

- Testy całościowe.
- Napisanie dokumentacji.
- "Wdrożenie" aplikacji.

## Potencjalne ryzyka 

| Ryzyko | Prawdopodobieństwo | Priorytet |
|--------|-------------------|-------|
| Problemy z integracją API | Wysokie | Wysoki |
| Niedotrzymanie harmonogramu z powodu braku siły roboczej | Niskie | Wysoki |
| Luki w bezpieczeństwie | Średnie | Wysoki |
| Konflikty pomiędzy bibliotekami | Niskie | Średni |
| Absencja członków zespołu | Niskie | Średni |
| Trudności z obsługą zdjęć i ich realizacją | Wysokie | Średni


## Kosztorys projektu

### Koszty osobowe

### 1. Koszty osobowe

| Moduł | Roboczogodziny | Stawka (zł/h) | Koszt (zł) |
|-------|----------------|--------------|-----------|
| Moduł autentyfikacji (Kostiantyn) | 32 | 50 | 1 600 |
| Moduł bazy danych (Kostiantyn) | 15 | 50 | 750 |
| Moduł zarządzania roślinami (Kostiantyn) | 38 | 50 | 1 900 |
| Moduł harmonogramu działań (Hleb) | 50 | 50 | 2 500 |
| Konfiguracja serwera i wdrożenie (Kostiantyn) | 10 | 50 | 500 |
| Dokumentacja końcowa | 16 | 50 | 800 |
| Testowanie całościowe | 24 | 50 | 1 200 |
| **Suma kosztów osobowych** | **185** | - | **9 250 zł** |

### 2. Infrastruktura deweloperska:

| Pozycja | Koszt jednostkowy | Liczba sztuk | Koszt całkowity |
|---------|-------------------|--------------|-----------------|
| Stacje robocze (laptopy) | Już posiadane | 2 | 0 zł |
| IDE (licencje) | Darmowe wersje (VS Code) | 2 | 0 zł |
| System kontroli wersji (Git/GitHub) | Darmowa wersja | 1 | 0 zł |
| Narzędzia do testowania | Darmowe oprogramowanie | - | 0 zł |

### 3. Koszty dodatkowe i rezerwa

| Pozycja | Koszt (zł) | Uwagi |
|---------|-----------|-------|
| Dostęp do API informacji o roślinach | 500 zł | Szacunkowy koszt roczny |
| Rezerwa projektowa (10%) | 1 150 zł | Na nieprzewidziane wydatki |
| **Suma kosztów dodatkowych** | **1 650 zł** | |

### 4. Podsumowanie kosztów

| Kategoria | Kwota (zł) |
|-----------|-----------|
| Koszty osobowe | 9 250 |
| Koszty dodatkowe i rezerwa | 1 650 |
| **Suma całkowita** | **10 900 zł** |

## Strategia Bezpieczeństwa dla projektu BePlantee

### 1. "Co chronić?"

#### Sprzęt i infrastruktura fizyczna
- Serwer aplikacji BePlantee
- Urządzenia używane do rozwoju aplikacji (laptopy deweloperów)

#### Dane
- **Dane osobowe użytkowników** (email, nazwa użytkownika, zaszyfrowane hasła)
- **Dane roślin użytkowników** (zdjęcia, nazwy, daty pielęgnacji)
- **Kopie zapasowe** bazy danych i plików użytkowników

#### Oprogramowanie
- Kod źródłowy aplikacji
- Biblioteki i zależności wykorzystywane w projekcie

#### Procesy i usługi
- Interfejs API
- Usługi uwierzytelniania i autoryzacji
- Usługi przechowywania i przetwarzania plików (zdjęcia roślin)

#### Niematerialne aktywa
- Reputacja serwisu
- Zaufanie użytkowników
- Prywatność użytkowników

### 2. "Przed czym chronić?"

#### Ataki ukierunkowane na aplikację
- **Ataki SQL Injection** - szczególnie istotne ze względu na wykorzystanie MariaDB
- **Cross-Site Scripting (XSS)** - zagrożenie podczas obsługi danych wejściowych od użytkownika

#### Zagrożenia związane z uwierzytelnianiem
- **Słabe hasła użytkowników** - mimo implementacji walidacji haseł
- **Kradzież sesji** - przechwycenie tokenów uwierzytelniających

#### Zagrożenia związane z infrastrukturą
- **Ataki typu Denial of Service (DoS)** - przeciążenie serwera prowadzące do niedostępności usługi
- **Utrata danych** - awaria serwera bez odpowiedniej kopii zapasowej

#### Zagrożenia zewnętrzne
- **Złośliwe oprogramowanie** - infekcja środowiska deweloperskiego
- **Awarie infrastruktury** - przerwy w dostawie prądu, problemy z łącznością

### 3. "Ile czasu, wysiłku i pieniędzy poświęcić na należną ochronę?"

| Lp | Ryzyko | Kategoria | Prawdopodobieństwo | Potencjalny wpływ | Szacowany koszt ochrony | Priorytet |
|----|--------|-----------|-------------------|-------------------|-------------------------|-----------|
| 1 | **Ataki SQL Injection** | Krytyczne | Wysokie | Krytyczny | Niski/Średni (8 rg) | Bardzo wysoki |
| 2 | **Słabe zabezpieczenie danych osobowych** | Krytyczne | Wysokie | Wysoki | Średni (12 rg) | Bardzo wysoki |
| 3 | **Nieautoryzowany dostęp do API** | Krytyczne | Wysokie | Wysoki | Średni (10 rg) | Wysoki |
| 4 | **XSS** | Średnie | Średnie | Średni do wysokiego | Niski (6 rg) | Wysoki |
| 5 | **Ataki na przesyłanie plików** | Średnie | Średnie | Wysoki | Niski (4 rg) | Wysoki |
| 6 | **Utrata danych** | Średnie | Niskie do średniego | Krytyczny | Średni (8 rg) | Wysoki |
| 7 | **DoS/DDoS** | Niskie | Niskie | Średni | Wysoki (500-1000 zł/rok) | Niski |

### 4. Strategia bezpieczeństwa

#### Zabezpieczenia dla danych:

1. **Dane użytkowników**:
   - Implementacja solidnego systemu hashowania haseł (aktualnie używamy bcrypt, co jest dobrą praktyką)
   - Zaszyfrowanie wrażliwych danych przechowywanych w bazie
   - Regularne backupy bazy danych z szyfrowaniem kopii zapasowych

2. **Dane roślin i zdjęcia**:
   - Walidacja typów plików przy uploadzię (już zaimplementowane)
   - Ograniczenie rozmiarów plików (już zaimplementowane)
   - Generowanie losowych nazw dla zapisywanych plików (już zaimplementowane)

#### Zabezpieczenia dla aplikacji:

1. **Ochrona API**:
   - Konsekwentne stosowanie tokenów JWT (już zaimplementowane)
   - Implementacja ograniczania liczby prób logowania
   - Timeout sesji po okresie bezczynności (zaimplementowany na 30 minut)

2. **Ochrona przed atakami**:
   - Parametryzowane zapytania SQL (konieczne do implementacji)
   - Sanityzacja wszystkich danych wejściowych użytkownika
   - Walidacja danych po stronie serwera, niezależnie od walidacji po stronie klienta

3. **Monitorowanie i audyt**:
   - Implementacja logowania dostępu i działań użytkowników

#### Procedury bezpieczeństwa:

1. **Zarządzanie kodem**:
   - Przechowywanie konfiguracji (klucze API, hasła) poza repozytorium kodu
   - Stosowanie zmiennych środowiskowych (.env) do przechowywania kluczy
   - Regularne aktualizacje bibliotek i zależności
   - Code reviews z naciskiem na aspekty bezpieczeństwa

2. **Zarządzanie hostingiem**:
   - Regularne aktualizacje oprogramowania serwerowego
   - Minimalizacja usług uruchomionych na serwerze
   - Korzystanie z HTTPS dla całej komunikacji

3. **Procedury na wypadek incydentów**:
   - Przygotowanie procedury powiadamiania użytkowników w przypadku wycieku danych
   - Regularne testowanie procedur przywracania systemu z kopii zapasowych

#### Alokacja zasobów:

Biorąc pod uwagę analizę ryzyka, proponujemy następującą alokację zasobów na zabezpieczenia:

1. **Czas deweloperski**:
   - 35 roboczogodzin na implementację najważniejszych zabezpieczeń (wysokie ryzyka)
   - 15 roboczogodzin na implementację średnio-priorytetowych zabezpieczeń
   - 10 roboczogodzin na regularne przeglądy i aktualizacje bezpieczeństwa
   - Łącznie: 60 roboczogodzin (7.5 dnia roboczego)

2. **Zasoby finansowe**:
   - 0-1000 zł rocznie na potencjalne usługi bezpieczeństwa (opcjonalnie)
   - Koszt hostingu z opcją automatycznych backupów (już uwzględniony w budżecie projektu)

## Analiza zasad bezpieczeństwa

### Zasada naturalnego styku z użytkownikiem

#### Bezproblemowe uwierzytelnianie:

- System używa tokenów JWT, które są transparentne dla użytkownika - po zalogowaniu użytkownik nie musi wielokrotnie podawać danych uwierzytelniających
- Sesje są automatycznie zarządzane przez middleware `(frontend/middleware/auth.js)`
- Automatyczne przekierowanie do strony logowania tylko gdy jest to niezbędne.

#### Walidacja haseł z pomocą dla użytkownika:

```javascript
// frontend/public/js/auth.js - walidacja w czasie rzeczywistym
function validatePassword(password) {
    const errors = [];
    if (password.length < 8) {
        errors.push('Password must be at least 8 characters long');
    }
    // Inne kryteria...
    return errors;
```

#### Przyjazne komunikaty błędów

- System wyświetla konkretne, pomocne komunikaty zamiast ogólnych błędów

- Walidacja po stronie klienta zapobiega frustrującym odrzuceniom formularzy

### Zasada spójności poziomej i pionowej

#### Spójność pozioma (w ramach warstwy):

Warstwa API (Backend):

```python
# Wszystkie endpointy chronione tokenem JWT
@router.get("/", response_model=List[UserPlantListItem])
def get_all_user_plants(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Konsekwentna autoryzacja
):
```

Warstwa Frontend:

```javascript
// frontend/routes/plants.js - wszystkie operacje wymagają autoryzacji
function requireAuth(req, res, next) {
  if (!req.session.user || !req.session.token) {
    return res.redirect('/auth/login');
  }
  next();
}
```

#### Spójność pionowa (między warstwami):

**Walidacja na wszystkich poziomach:**

1. Frontend - walidacja JavaScript dla UX
2. Backend - walidacja Pydantic dla bezpieczeństwa
3. Baza danych - ograniczenia na poziomie schematu

```python
# app/schemas/user_plant.py
class UserPlantBase(BaseModel):
    name: str = Field(..., max_length=20)  # Walidacja Pydantic
```

```sql
name = Column(String(20), nullable=False)  # Ograniczenie DB
```

### Zasada minimalnego przywileju

#### Autoryzacja na poziomie zasobów:

```python
# app/services/user_plant_service.py
def get_user_plant(db: Session, id: int, user_id: int) -> Optional[UserPlant]:
    return db.query(UserPlant).filter(
        UserPlant.id == id, 
        UserPlant.owner_id == user_id
    ).first()
```
#### Ograniczone uprawnienia użytkowników:

- Użytkownicy mogą modyfikować tylko własne rośliny
- Brak ról administratorskich w obecnej implementacji
- Każda operacja CRUD weryfikuje prawa dostępu

#### Sesje z ograniczonym czasem życia:

```python
# app/config.py
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Krótki czas życia tokenów
```

### Zasada domyślnej odmowy dostępu

#### Middleware autoryzacyjny:

```python
// frontend/routes/plants.js
function requireAuth(req, res, next) {
  if (!req.session.user || !req.session.token) {
    return res.redirect('/auth/login'); // Domyślna odmowa
  }
  next();
}
```

#### Weryfikacja tokenów:

```python
# app/utils/security.py
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Walidacja...
    except JWTError:
        raise credentials_exception  # Odmowa przy błędzie
```

#### Domyślne przekierowania:

- Nieuwierzytelnieni użytkownicy są automatycznie przekierowywani na stronę logowania
- Błędne tokeny skutkują odmową dostępu
- Brak dostępu do zasobów innych użytkowników