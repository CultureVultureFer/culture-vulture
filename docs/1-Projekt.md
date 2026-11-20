# 1. Opseg projekta

## 1.1 Problem i cilj projekta

### Problem
Ideja koja je dovela do ovog projekta zapravo je proizašla iz toga da je više ljudi u timu primijetilo kako dosta često vide plakate i objave događaja koji su već prošli, a na njega su zapravo htjeli otići.

### Cilj
    Cilj projekta je izraditi aplikaciju CultureVulture koja će na jednom mjestu prikazivati događaje koje objavljuju sami organizatori kao korisnici stranice ili događaji dohvaćeni s vanjskog izvora.

## 1.2 Ciljani korisnici i dionici
| Skupina korisnika ili dionika | Potreba ili interes relevantan za ovaj projekt |
|---|---|
| Korisnik | Pronaći događaje na jednoj mjestu |
| Organizator | Objava događaja kako bi drugi korisnici vidjeli i mogli sudjelovati u tim događajima |
| Administrator | Održavanje točnosti sadržaja i upravljanje profilima korisnika i organizatora |
| Ticketmaster | Neće koristiti aplikaciju, ali odlučuje o količini događaja koje mi smijemo povući s njega |

## 1.3 Granice projekta

**Uključeno:** Prikaz događaja s vanjskog izvora ili kreiranih od strane organizatora, pretraživanje događaja, prikaz događaja na karti, dodavanje događaja u kalendar, ostavljanje komentara i recenzija

**Isključeno:** Prodaja ulaznica; Aplikacija prikazuje cijenu, ali ne sudjeluje u kupnji

**Vanjske ovisnosti:** Ticketmaster za dohvat događaja, Google Maps API za karte, Google Calendar API za dodavanje događaja u kalendar i OAuth 2.0 za prijavu

## 1.4 Postojeći pristupi i opravdanost projekta

Korisnici trenutno koriste stranicu poput [Entria](https://www.entrio.hr/en)
ili ih pronalaze na društvenim mrežama i plakatima.
CultureVulture prikazuje događaje dohvaćene s vanjskog izvora (Ticketmaster)
i događaje koje organiziraju organizatori i objavljuju izravno u aplikaciji.
Korisniku također upoterbu olakšava i moguće dodavanje događaja u 
vlastiti kalendar i prikaz događaja na karti.