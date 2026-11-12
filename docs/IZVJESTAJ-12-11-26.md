# Izvjestaj TG08.1(CultureVulture) 12.11.2026.
## Ono što je napravljeno (ili na `master` grani)
- Generalna integracija sa Googleom kao IdP (OIDC)
- Dizaj ključnih web puteva na Figmi
- Testiran Ticketmaster API (sadrži dovoljno podatak, i poslžiti će kao izvor vanjskih podataka)
#### Generalna integracija sa Googleom kao IdP (OIDC)
Izabran je BFF(Backend-for-frontend) OIDC obrazac, iako je i frontend kao klijet u jednome trenutku izgledao kao dobra alternativa. Django koristi sesije kao glavnu metodu authentikacije, koju smo i zadržali. Backend za sada (barem dok se ne integrira Google Kalendar), ne sprema OIDC tokene u bazu. Već se ID Korisnika koji pretvara u UUID i sprema u našu bazu kao korisnik (a kasnije tako i provjerava)
#### Dizajn ključnih web puteva na Figmi
Jedan primjer je homepage običnog korisnika koji izgleda ovako:
