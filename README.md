# 🐶 BorderHearts Kennel API  
**Projekt API dla hodowli psów rasy Border Collie jako system rezerwacji szczeniąt**

BorderHearts Kennel API to RESTowe API pozwalające na:
- przeglądanie psów hodowlanych (suki, reproduktory),
- przeglądanie miotów oraz szczeniąt,
- rejestrację i logowanie użytkowników,
- składanie rezerwacji na wybranego szczeniaka,
- zabezpieczenie tokenowe (autentykacja),
- zapobieganie wielokrotnej rezerwacji tego samego szczeniaka.

Projekt wykonany w ramach przedmiotu **Aplikacje WWW (2025/2026Z)**.

---

##  Funkcjonalności API

### Publiczne (bez logowania)
- Lista umaszczeń (`/api/breeds/`)
- Lista psów (`/api/dogs/`)
- Lista miotów (`/api/litters/`)
- Lista szczeniąt (`/api/puppies/`)
- Wyszukiwarka psów / ras / szczeniąt (parametr `?q=`)

### Wymagające logowania Tokenem
- Tworzenie rezerwacji szczeniaka
- Usuwanie własnej rezerwacji
- Przegląd własnych rezerwacji

### Obsługa użytkowników
- Rejestracja (`/api/register/`)
- Logowanie i pobranie tokena (`/api/token/`)

---

## Technologie
- **Python 3.12**
- **Django 5.2**
- **Django REST Framework**
- Token Authentication (DRF)

---

## Instalacja i uruchomienie projektu

```bash
git clone https://github.com/klalub/Aplikacje-WWW.git
cd borderhearts

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Rejestracja i logowanie (token)

### Rejestracja użytkownika

POST (`/api/register/`)
#### Body:
```json
{
  "username": "client1",
  "password": "test1234"
}
```
#### Odpowiedź:
```json
{
  "id": 3,
  "username": "client1",
  "token": "89f0c1c83dd5ffa24f11b8af78d91c0ffd2cbd22"
}
```
### Logowanie – pobranie tokena
POST (`/api/token/`)
#### Body:
```json
{
  "username": "client1",
  "password": "test1234"
}
```
#### Odpowiedź:
```json
{
  "token": "89f0c1c83dd5ffa24f11b8af78d91c0ffd2cbd22"
}
```

Token dodajemy w Postmanie jako:
(`Authorization: Token <TWÓJ_TOKEN>`)

## Modele danych
### 1 Breed – rasa
```bash
id, name, color_pattern, description
```

### 2 Dog – dorosły pies
```bash
id, name, breed, gender, date_of_birth, color, description, health_tests, owner
```

#### Walidacje:

- imię tylko litery i spacje,
- data urodzenia nie może być z przyszłości.

### 3 Litter – miot
```bash
id, mother, father, birth_date, number_of_puppies, is_planned
```
#### Walidacje:
- matka ≠ ojciec
- różne płcie rodziców

### 4 Puppy – szczeniak
```bash
id, litter, name, gender, color, description, status ("available" / "reserved")
```
#### Walidacje:
- imię tylko litery i spacje

### 5 Reservation – rezerwacja
```bash
id, puppy, user, date_reserved, notes
```
#### Walidacje:
- szczeniak może mieć tylko jedną rezerwację

## Najważniejsze Endpointy
### Lista psów
GET (`/api/dogs/`)
### Dodanie psa
POST (`/api/dogs/`)
- (wymagane pola: imię, gender, date_of_birth, owner)
### Lista szczeniąt
GET (`/api/puppies/`)
### Rezerwacja
POST (`/api/reservations/`)
- Nagłówek: (`Authorization: Token <token>`)
#### Body:
```json
{
  "puppy": 1,
  "notes": "Poproszę o kontakt w sprawie odbioru."
}
```
#### Odpowiedź:
```json
{
  "id": 5,
  "puppy": 1,
  "user": 3,
  "date_reserved": "2025-01-15",
  "notes": "Poproszę o kontakt w sprawie odbioru."
}
```
#### Jeśli szczeniak już zarezerwowany:
```json
{
  "puppy": ["Ten szczeniak jest już zarezerwowany."]
}
```

## Przykładowe zapytania CURL
### Pobranie listy psów
```bash
curl http://127.0.0.1:8000/api/dogs/
```
### Rezerwacja szczeniaka
```bash
curl -X POST http://127.0.0.1:8000/api/reservations/ \
  -H "Authorization: Token TWOJ_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"puppy": 1}'
```

## Struktura projektu
```cpp
borderhearts/
│
├── kennel/
│   ├── models.py
│   ├── serializers.py
│   ├── api_views.py
│   ├── urls.py
│   └── static/
│       └── kennel/
│           └── border.jpg
│
├── borderhearts/
│   ├── settings.py
│   └── urls.py
```

```cpp
borderhearts/
│
├── manage.py
├── requirements.txt   ← TU!
│
├── kennel/
│   ├── models.py
│   ├── serializers.py
│   ├── api_views.py
│   └── urls.py
│   └── static/
│       └── kennel/
│           └── border.jpg
│
└── borderhearts/
    ├── settings.py
    └── urls.py
```

