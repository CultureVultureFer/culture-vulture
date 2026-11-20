# 2. Analiza zahtjeva

## 2.1 Funkcijski zahtjevi

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

## 2.2 Nefunkcijski zahtjevi
| ID | Opis | Prioritet | Izvor |
|---|---|---|---|
| NF-01 | Frontend stranice izrađen je u Reactu, backend u Djangu, a podatci se pohranjuju u PostgreSQL bazi | Visok | odluka tima | 
| NF-02 | Prijava se provodi putem OAuth 2.0 servisa i lozinka se nigdje ne sprema | Visok | Sigurnosna pravila |
| NF-03 | Sustav treba imati odgovarajuću dokumentacijui | Visok | Pravila dokumentiranja |
| NF-04 | Korisničko sučelje je na engleskom jeziku | Srednji | odluka tima |
| NF-05 | Podatci dohvaćeni s Ticketmastera osvježavaju se barem jednom dnevno | Srednji | Odluka tima |
| NF-06 | Lokacija korisnika koristi se samo za prikaz događaja u blizini korisnika i ne sprema se u bazu | Visok | Sigurnosna pravila |
## 2.3 Dionici i akteri
| ID aktera | uloga | Obuhvaćeni funkcijski zahtjevi |
|---|---|---|
| A-01 | Korisnik | F-001 registracija i prijava; F-002 ostavljanje komentara i recenzija; F-005 Prikaz lokacije događaja na karti; F-007 Uređivanje i brisanje vlastitog profila; F-006 Prikaz događaja u radijusu trenutne lokacije; F-008 Pretraživanje događaja; F-009 Dodavanje događaja u kalendar; F-014 Pregled detalja događaja; F-015 Sortiranje događaja; F-016 Sortiranje događaja; F-017 Brisanje vlastitih komentara. |
| A-02 | Organizator | F-004 Uređivanje i brisanje vlastitih događaja; F-010 Dodavanje vlastitih događaja; F-011 Pregled svojih objavljenih događaja. |
| A-03 | Administrator | F-012 Mogućnost upravljanja događajima; F-013 Upravljanje profilima korisnika i organizatora. |
| A-04 | Ticketmaster API | F-003 Dohvaćanje događaja s vansjkog API-a |
| A-05 | OAuth 2.0 | F-001 Prijava i registracija |
| A-06 | Google Maps API | F-006 Pregledavanje događaja oko trenutnog radijusa; F-005 Prikaz lokacije na karti |
| A-07 | Google Calendar API | F-009 Dodavanje događaja u kalendar |
## 2.4 Ograničenja i pretpostavke
| ID | Tip | Opis ograničenja ili pretpostavke | Izvor | Injženjerska posljedica/ provjera |
|---|---|---|---|---|
| C-01 | Ograničenje | Prijava se odvija isključivo preko OAuth 2.0 servisa | Odobreni zadatak | Provjera autoriziranih i neautoriziranih zahtjeva. |
| C-02 | Ograničenje | Ticketmaster odobrava samo ograničen broj događaja po upitu | Dokumentacija Ticketmastera | Dohvat ograničen na jedan grad |
| AS-01 | Pretpostavka | Dohvaćeni događaji imaju postavljenu adresu | Pretpostavka o podatcima | Planirati prikaz prijava bez valjane adrese |
| AS-02 | Pretpostavka | Korisnik dopušta pristup lokaciji | Procjena tima | Korisnici koji odbiju pristup ne mogu pregledati događaje u svom radijusu |
| AS-03 | Pretpostavka | Korisnik ima Google Račun | Procjena tima | Korisnik bez google računa nema pristup aplikaciji |
## 2.5 Sljedivost zahtjeva
| ID zahtjeva | Obrazac uporabe | Arhitekturna realizacija | Ispitivanje ili provjera |
|---|---|---|---|
| F-001 | UC1 | Web-klijent; API za prijavu; Google OAuth 2.0 | CT-01 Prva prijava stvara korisnika; CT-02 Registracija organizatora; ST-01 Prijava Google računom|
| F-002 | UC2 | Web-klijent; API za događaje, usluga za događaje | CT-03 Komentari i recenzije; ST-02 Ostavljanje komentara i recenzije |
| F-003 | UC10 | Ticketmaster API; PostgreSQL; usluga za događaje | CT-04 Obrada dohvaćenih događaja |
| F-004 | UC4 | Web-klijent, Api za događaje; usluga za događaje | CT-05 Uređivanje vlastitog događaja; ST-03 Uređivanje i brisanje događaja. |
| F-005 | UC5 | Web-klijent; Google Maps API; | ST-04 Prikaz lokacije događaja na karti |
| F-006 | UC6 | Web-klijent; Google Maps API; API za događaje; Usluga za događaje | CT-06 Dohvat događaja u radijusu; ST-05 Prikaz događaja u radijusu |
| F-007 | UC7 | Web-klijent; API za profil | CT-07 uređivanje i brisanje profila; ST-06 Uređivanje i brisanje profila. |
| F-008 | UC8 | Web-klijent; Api za događaje; Usluga za događaje | CT-08 Pretraga događaja po nazivu događaj ili organizacije; ST-07 Pretraga događaja po nazivu događaj ili organizacije. |
| F-009 | UC9 | Web-klijent; Google Calendar API; API za događaje; Usluga za događaje | ST-09 Dodavanje događaja u kalendar. |
| F-010 | UC4 | Web-klijent; API za događaje; usluga za događaje | CT-09 Dodavanje događaja; CT-10 Dodavanje događaja s krivim podatcima; ST-10 Dodavanje događaja. |
| F-011 | UC16 | Web-klijent; API za događaje; usluga za događaje | CT-11 Popis vlastitih događaja organizatora; ST-11 pregled vlastitih događaja. |
| F-012 | UC11 | Web-klijent; API za događaje; usluga za događaje| CT-12 Administrator uređuje podatke događaja ili ga briše; ST-12 Administrator upravlja događajem. |
| F-013 | UC12 | Web-klijent; Api za profile; usluga za profile| CT-13 Uređivanje podataka i brisanje profila; ST-13 Upravljanje profilima korisnika i organizatora. |
| F-014 | UC13 | Web-klijent; API za događaje; usluga za događaje | CT-14 Dohvat detalja događaja; ST-14 Prikaz detalja događaja. |
| F-015 | UC3 | Web-klijent; API za događaje; usluga za događaje | CT-15 Sortiranje po datumu ili abecedi; ST-15 Sortiranje događaja. |
| F-016 | UC14 | Web-klijent; API za događaje; usluga za događaje | CT-16 Filtriranje događaja po kategoriji; ST-16 filtriranje događaja. |
| F-017 | UC15 | Web-klijent; API za događaje; usluga za događaje | CT-17 Uređivanje i brisanje vlastitih komentara; ST-17 uređivanje i brisanje komentara. |
## 2.6 Pregled zahtjeva
| Kontrolna točka | Povratna informacija ili nalaz | Odluka o zahtjevu ili opsegu |
|---|---|---|
| Iteracija 1 | Entrio nema javni API | Odabran Ticketmaster API |