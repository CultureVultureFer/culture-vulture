# Programsko inženjerstvo

# Opis projekta

Ovaj projekt je rezultat timskog rada u sklopu projektong zadatka kolegija [Programsko inženjerstvo](https://www.fer.unizg.hr/predmet/proinz) na Fakultetu elektrotehnike i računarstva
Sveučilišta u Zagrebu

Kao projektni zadatak radit ćemo aplikaciju **CultureVulture**.
Koristeći vanjski API aplikacija će dohvaćati podatke o događajima, spremati ih u našu bazu i prikazivati ih na jednom mjestu.
Prvotno smo planirali koristiti Entrio, ali on nema javno dostupan API, tako da još biramo koji izvor ćemo koristiti.
Autentifikacija korisnika provodit će se preko vanjskog servisa koristeći OAuth 2.0.

## Uloge

U aplikaciji postoje tri vrste korisnika: korisnik, organizator i administrator. Uloge se razlikuju po dopuštenjima koja imaju

### Korisnik

Korisnik može koristiti aplikaciju za pretraživanje događaja po imenu događaja ili organizatora. Može filtrirati događaje po kategorijama i sortirati po datumu događaja ili abecedno. Korisnik može odabrati radijus oko svoje trenutne lokacije i vidjeti događaje u svojoj blizini.
Korisnik događaj može dodati u svoj Google kalendar kako na njega ne bi zaboravio, a nakon događaja može ostaviti komentar i recenziju kao povratnu informaciju.

### Organizator

Organizatori mogu objavljivati svoje vlastite događaje direktno u aplikaciji. Pri objavi unose datum i vrijeme početka i završetka događaja, cijenu ulaznice, kratki opis i kategoriju, npr. glazba, kazalište, sport, sajmovi.

### Administrator

Administrator ima pregled nad cijelom aplikacijom. Može upravljati događajima, profilima korisnika i organizatora.

# Cilj i motivacija

Ideja koja je dovela do ovog projekta zapravo je proizašla iz toga da je više ljudi u timu primijetilo kako dosta često vide plakate i objave događaja koji su već prošli, a na njega su zapravo htjeli otići. Naše rješenje je napraviti aplikaciju koja će sve to objediniti na jednom mjestu dohvaćanjem podataka s vanjskog API-ja.

# Funkcijski zahtjevi

| ID zahtjeva | Opis | Prioritet | Izvor | Kriteriji prihvaćanja |
|---|---|---|---|---|
| F-001 | Sustav korisnicima omogućuje registraciju putem OAuth 2.0 autentifikacije | Visok | Specifikacija projekta | Korisnik može kreirati račun i uspješno se prijaviti. |
| F-002 | Sustav omogućuje komentiranje i recenziju događaja | Srednji | Specifikacija projekta | Korisnik uspješno komentira i ocjenjuje događaj. |
| F-003 | Sustav podatke dohvaća s vanjskog API-a | Visok | Specifikacija projekta | Dohvaćeni podatci vidljivi su u aplikaciji. |
| F-004 | Organizator može uređivati i brisati vlastiti događaj | Visok | Zahtjev dionika | Promjene za događaj su vidljive i obrisani događaji se više ne prikazuju korisnicima. |
| F-005 | Lokacija događaja prikazana je na karti | Srednji | Specifikacija projekta | Događaj je vidljiv na karti i lokacija je jednaka navedenoj lokaciji. |
| F-006 | Korisnik može vidjeti događaj u odabranom radijusu svoje trenutne lokacije | Srednji | Specifikacija projekta | Nakon odabira radijusa prikazuju se događaji u odabranom radijusu. |
| F-007 | Korisnik može uređivati i obrisati svoj profil | Visok | Zahtjev dionika | Promjene profila su vidljive, a nakon brisanja profila korisnik se više ne može prijaviti s tim računom. |
| F-008 | Korisnik može pretraživati događaje po nazivu događaja ili organizatora | Visok | Specifikacija projekta | Prikazani su samo rezultati koji odgovaraju upisanom nazivu ili organizatoru. |
| F-009 | Korisnik događaj može dodati u Google kalendar | Srednji | Specifikacija projekta | Događaj uspješno dodan u Google kalendar s ispravnim datumom i vremenom događaja. |
| F-010 | Organizator može dodavati vlastite događaje | Visok | Specifikacija projekta | Dodani događaj vidljiv je korisnicima i vidljivi su svi uneseni podaci. |
| F-011 | Organizator može pregledati popis svojih objavljenih događaja | Srednji | Zahtjev dionika | Organizator na jednom mjestu može vidjeti i upravljati svojim događajima. |
| F-012 | Administrator ima mogućnost upravljanja događajima | Visok | Specifikacija projekta | Administrator može obrisati bilo koji događaj ili komentar, a obrisani sadržaj više nije vidljiv. |
| F-013 | Administrator može upravljati profilima korisnika i organizatora | Visok | Specifikacija projekta | Administrator može pogledati i obrisati bilo koji profil. |
| F-014 | Korisnik može pogledati detalje događaja | Visok | Zahtjev dionika | Nakon što korisnik klikne na događaj prikazuju se detalji o događaju. |
| F-015 | Korisnik može događaje poredati po datumu ili abecedno | Srednji | Zahtjev dionika | Događaji uspješno poredani ovisno o odabranom načinu sortiranja. |
| F-016 | Korisnik može filtrirati događaje po kategoriji | Visok | Specifikacija projekta | Odabirom jedne ili više kategorija prikazani događaji sužavaju se na odabrane kategorije. |
| F-017 | Korisnik može brisati vlastite komentare | Srednji | Zahtjev dionika | Nakon brisanja komentar više nije vidljiv. |

# Tehnologije

Frontend: React
Backend: Django
Database: PostgreSQL
Project management: GitHub, tbd
Vanjski servisi: OAuth 2.0, izvor događaja (tbd), Google Maps API, Google Calendar API

# Članovi tima

Karlo Čehulić: Team Lead
Ivan Bunić: Frontend engineer
Matija Krivec: Backend engineer
Roko Gulić: Backend engineer
Tomislav Facković: Frontend engineer
Vanda Meić: Frontend engineer
Tibor Brestovac: Backend engineer