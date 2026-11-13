# Izvjestaj TG08.1(CultureVulture) 12. 11. 2026.
## Ono što je napravljeno (ili na `master` grani)
- Generalna integracija sa Googleom kao IdP (OIDC)
- Dizajn ključnih web puteva na Figmi
- Testiran Ticketmaster API (sadrži dovoljno podatak, i poslužiti će kao izvor vanjskih podataka)
#### Generalna integracija sa Googleom kao autentikacijski poslužitelj (OIDC)
Nalazi se na master grani i name je OIDC integraciji F-001, dva od tri sekvencijska dijagram su napravljena.
Izabran je BFF(Backend-for-frontend) OIDC obrazac, iako je i frontend kao klijet u jednome trenutku izgledao kao dobra alternativa. Django koristi sesije kao glavnu metodu autentikacije, koju smo i zadržali. Backend za sada (barem dok se ne integrira Google Kalendar), ne sprema OIDC tokene u bazu. Već se ID korisnika koje Google koristi (sud) koji pretvara u UUID i sprema u našu bazu kao korisnik (a kasnije tako i provjerava)
#### Dizajn ključnih web puteva na Figmi
Jedan primjer je homepage običnog korisnika koji izgleda ovako:
![Example](./assets/figma/home.png)
Ekipa za frontend koristi te dizajne, kako bi imali točno određeni cilj tijekom rada s CSS-om.
#### Testiran Ticketmaster API
Ticketmaster na području Europe ima dovoljno evenata da dođe do svoje internalne granice za API (10000 eventa), tako da smo odlučili za sada limitirati opseg na jedan grad (Berlin u kodu). Kada želimo od API-ja saznati broj evenata za Berlin, on vraća 972 eventa.
Konkretno, za to smo koristili [API Explorer.](https://developer.ticketmaster.com/api-explorer/v2/)
## Ono što će biti napravljeno do kraja tjedna
- F-003 (Sustav podatke dohvaća s vanjskog API-a) - grana `models-django`
- F-014 (Korisnik može pogledati detalje događaja)
- F-001 (sekvencijski dijagram prijave/registracije organizatora)
## Javni poslužitelj
Budući da postoje Dockerfile-ovi za razvojno okruženje u grani `master` koje tim koristi za razvoj aplikacije. Iste datoteke bi mogli promijeniti tako da budu spremi za javni poslužitelj, pa ih poslužiti kao Docker image u aplikaciji kao što je render.
