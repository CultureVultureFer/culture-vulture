# CultureVulture

CultureVulture pruža svim korisnicima pregled budućih događaja za Berlin (za potrebe prve predaje), a organizatorima mogućnost objave vlastitih događaja.

**Projekt na kolegiju:** Ovu je aplikaciju razvio studentski tim u sklopu kolegija [Programsko inženjerstvo](https://www.fer.unizg.hr/predmet/proinz) na Fakultetu elektrotehnike i računarstva Sveučilišta u Zagrebu (FER).

## Opis aplikacije

Prikaz događaja s vanjskog izvora ili kreiranih od strane organizatora, pretraživanje događaja, prikaz događaja na karti, dodavanje događaja u kalendar, ostavljanje komentara i recenzija.


Mnogi gradovi Europe sadrže mnoga kulturna i društvena zbivanja poput koncerata, predstava, utakmica, sajmova i festivala. Međutim, budući da su informacije o tim događajima sadržane na pojedinim stranicama institucija ili organizatora, korisnicima može biti teško dobiti pregled nadolazećih događaja koji se održavaju u gradu. Aplikacija CultureVulture rješava taj problem agregiranjem informacija o kulturnim događajima te izravnim povezivanjem organizatora i korisnika dostupnim objavama na samoj aplikaciji.

**Ključne funkcionalnosti**
- Pregled događaja za obične korisnike
- Kreiranje događaja za organizatore

Za potpuni opseg, zahtjeve, oblikovanje i dokaze ispitivanja pogledajte [docs](docs/Home.md).

<a id="deployment"></a>
## Postavljanje (engl. deployment)

<!-- UPUTA: Ovaj odjeljak opisuje već postavljenu aplikaciju koju se može otvoriti i isprobati bez lokalnog pokretanja izvornog koda.
Za Iteraciju 1 i Završni pregled navedite konkretne podatke. Provjerite vodi li URL na javno dostupnu pokrenutu aplikaciju i radi li navedeni tijek uporabe. Nikada ne objavljujte lozinke ni pristupne tokene. -->

**Javno dostupna aplikacija:** https://culture-vulture-front.up.railway.app/ (frontend), https://culture-vulture-production.up.railway.app/admin/login/?next=/admin/ (backend – administratori)

**Isprobajte:** 
Nakon prijave kao korisnik, početni zaslon će prikazivati popis događaja koje je aplikacija pohranila. Nakon prijave kao organizator, u gornjem desnom kutu aplikacije prikazat će se i gumb za kreiranje vlastitih događaja (POST EVENT) pomoću kojeg organizatori mogu objaviti vlastite događaje.

**Demonstracija:** Prijava kao obični korisnik može se obaviti pomoću Googlea na https://culture-vulture-front.up.railway.app ako korisnik nije prijavljen; ako jest, mora se prvo odjaviti. Ako se želite prijaviti kao organizator MORATE koristiti drugi Google račun, a ne onaj kojim ste se prijavili kao obični korisnik. Nakon odjave (ako ste bili prijavljeni kao obični korisnik), ponovnim odlaskom na https://culture-vulture-front.up.railway.app i klikom na `Want to become an organizer? Register here` ili izravnim odlaskom na https://culture-vulture-front.up.railway.app/org/register možete se registrirati kao organizator.

[Vodič za postavljanje i pokretanje](docs/6-Postavljanje-instalacija-i-konfiguracija.md) opisuje smještaj aplikacije (engl. hosting) koji tim stvarno koristi. Tim može koristiti Render ili drugu platformu koju ste dogovorili s asistentom/demonstratorom.

<a id="quick-start"></a>
## Brzi početak / instalacija

**Preduvjeti:** [Navedite potrebno izvršno okruženje (engl. runtime) i verzija, upravitelj paketa (engl. package manager), baza podataka ili vanjska usluga ako je nužna.]

```bash
git clone [repository URL]
cd [repository directory]
[install dependencies]
[run the application]
```

**Adresa:** [Stvarna adresa koju aplikacija ispiše nakon pokretanja.]

**Konfiguracija:** [Navedite potrebne varijable okruženja (engl. environment variables) ili uputite na sigurnu datoteku `.env.example`; objasnite gdje se dobivaju vrijednosti. Nikada ne stavljajte stvarne pristupne podatke u ovu datoteku, primjer konfiguracije, snimke zaslona, zapise ni zapise promjena (engl. commits).]

[Dodajte kratak korak provjere, primjerice koja se stranica treba otvoriti ili koja naredba pokreće osnovnu provjeru.] Za detaljno postavljanje pogledajte [projektnu dokumentaciju](docs/Home.md).

## Tehnologije

Navedite nekoliko tehnologija i vanjskih usluga koje bitno određuju kako vaša aplikacija radi. Za svaku navedite njezinu konkretnu ulogu i jedan razlog ili ograničenje važno za projekt. Alat za razvoj ili ispitivanje uključite samo ako je njegova uloga važna za razumijevanje načina na koji je projekt izrađen ili provjeren. Nemojte prepisivati popis ovisnosti (engl. dependencies), statistiku programskih jezika ni popis razvojnih okruženja i komunikacijskih alata. Tablicu provjerite prema stvarnom repozitoriju i pokrenutoj aplikaciji; potrebne verzije i konfiguraciju dokumentirajte u vodiču za instalaciju.

| Tehnologija ili alat | Uloga u ovom projektu | Razlog uporabe ili važno ograničenje |
| --- | --- | --- |
| Docker | Pruža produkcijske i razvojne slike aplikacije | Aplikacija je postavljena (engl. deployed) pomoću produkcijskih slika, a timu je olakšano pokretanje bilo koje inačice aplikacije putem datoteke docker-compose.yml |
| Django | Backend | Sadrži sve API-je, usluge i poslovnu logiku aplikacije te web sučelje za administratore |
| React  | Frontend | Web sučelje |
| PostgreSQL | Baza | Sadrži podatke o korisnicima, događajima... |
| TicketMaster | Vanjski API | Služi za dohvat relevantnih događaja koji nisu nužno kreirani na CultureVulture aplikaciji, povećava popis događaja |

<a id="team-members"></a>
## Članovi tima

| Član | Glavna uloga ili doprinos |
| --- | --- |
| Karlo Čehulić | Team Lead |
| Ivan Bunić | Frontend engineer |
| Matija Krivec | Backend engineer |
| Roko Gulić | Backend engineer |
| Tomislav Facković | Frontend engineer |
| Vanda Meić | Frontend engineer |
| Tibor Brestovac | Backend engineer |

<a id="license"></a>
## Status licence: MIT

<a id="ai-usage"></a>
## Uporaba umjetne inteligencije [![AI Usage: Disclosed](https://img.shields.io/badge/AI%20Usage-Disclosed-blue.svg)](https://www.fer.unizg.hr/_download/repository/Policy%20on%20the%20appropriate%20use%20of%20artificial%20intelligence%20at%20the%20faculty%20of%20electrical%20engineering%20and%20computing%5B1%5D.pdf)

Ovaj projekt slijedi FER-ova [pravila o primjerenoj uporabi umjetne inteligencije](https://www.fer.unizg.hr/_download/repository/Policy%20on%20the%20appropriate%20use%20of%20artificial%20intelligence%20at%20the%20faculty%20of%20electrical%20engineering%20and%20computing%5B1%5D.pdf).

**Izjava:** Tim je koristio AI prilikom izrade projekta, detaljniji opis se nalazi u [Home.md - Koristenje](./docs/Home.md#ai-usage)

<a id="code-of-conduct-and-support"></a>
## Kodeks ponašanja i podrška [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

Od članova tima očekuje se pridržavanje **Kodeksa ponašanja studenata** Fakulteta elektrotehnike i računarstva Sveučilišta u Zagrebu, pravila timskog rada na kolegiju i [Etičkog kodeksa IEEE-a](https://www.ieee.org/about/corporate/governance/p7-8.html). [Postavite poveznicu na `CODE_OF_CONDUCT.md` ako se ta datoteka koristi u vašem repozitoriju.]

---

Struktura dokumentacije prilagođena je predlošku kolegija Programsko inženjerstvo FER-a autora [Vlade Sruka](https://www.fer.unizg.hr/vlado.sruk), licenciranom pod [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Aplikaciju i njezin sadržaj izradio je gore navedeni studentski tim.
