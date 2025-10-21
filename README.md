<h1>🐾 BorderHearts API</h1>

<h3>BorderHearts API to aplikacja webowa Django REST Framework służąca do zarządzania hodowlą psów rasy Border Collie.
Projekt pozwala właścicielowi hodowli zarządzać bazą psów, miotów i szczeniąt, a klientom przeglądać aktualne mioty oraz rezerwować szczenięta.</h3>
<h2></h2>

<b>Technologie:</b>

1. Python 3.14

2. Django 5.2.7

3. Django REST Framework

4. SQLite (lub PostgreSQL)
<h2></h2>
<b>Modele:</b>

1. User — użytkownik (admin / klient)

2. Dog — pies hodowlany

3. Litter — miot (rodzice, data, liczba szczeniąt)

4. Puppy — szczeniak (status: wolny / zarezerwowany / sprzedany)

5. Reservation — rezerwacja dokonana przez użytkownika
<h2></h2>
<b>Autoryzacja:</b>

role:

1. admin — pełny dostęp, zarządzanie hodowlą

2. user — przeglądanie szczeniąt, tworzenie rezerwacji
<h2></h2>
<b>Autor:</b>

Klaudia Lubiejewska

Semestr 2025/2026 – Aplikacje WWW
