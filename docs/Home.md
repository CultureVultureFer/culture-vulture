# CultureVulture — Projektna dokumentacija
 
**Kolegij:** [Programsko inženjerstvo](https://www.fer.unizg.hr/predmet/proinz), Fakultet elektrotehnike i računarstva Sveučilišta u Zagrebu  
**Akademska godina:** 2026./2027.  
**Tim:** CultureVulture, TG08.1  
**Nastavnik:** Vlado Sruk  
**Asistent:** Marin Matjanec  
**Demonstrator:** Kristijan Gašpar
 
## Pregled projekta
 
**Cilj:** Izrada 
 
CultureVulture je timski projekt izrađen u sklopu kolegija Programsko inženjerstvo na Fakultetu elektrotehnike i računarstva Sveučilišta u Zagrebu. Aplikacija na jednom mjestu omogućuje korisniku pregled događaja u njegovoj blizini te njihovu lokaciju na karti. Događaje su izravno objavili organizatori ili su dohvaćeni s vanjskog izvora. Koristi vanjski API Ticketmastera za dohvat podataka o događajima, sprema ih u bazu i prikazuje na stranici. Putem vanjskog Google Maps API-ja korisnici mogu pregledati događaje na karti unutar aplikacije, a putem vanjskog Google Calendar API-ja dodati događaj u osobni kalendar. Autentifikacija korisnika provodi se preko vanjskog servisa koristeći OAuth 2.0.
 
**Aplikacija i osnovno postavljanje:** [README repozitorija](../README.md#quick-start)  
**Javno dostupna aplikacija:** pogledajte [README – Postavljanje](../README.md#deployment)
 
## Članovi tima i uloge
 
Ažurirani popis članova, njihovih GitHub profila i glavnih uloga ili doprinosa nalazi se u [README-u repozitorija](../README.md#članovi-tima).
 
## Kazalo dokumentacije
 
| Stranica | Svrha |
| --- | --- |
| [1. Opseg projekta](1-Projekt.md) | Problem, cilj i granice projekta |
| [2. Analiza zahtjeva](2-Analiza-zahtjeva.md) | Zahtjevi, ograničenja i sljedivost |
| [3. Obrasci uporabe](3-Obrasci-uporabe.md) | Akteri i reprezentativne interakcije korisnika |
| [4. Arhitektura i oblikovanje](4-Arhitektura-i-oblikovanje.md) | Glavne odluke oblikovanja, struktura, podaci i ponašanje |
| [5. Ispitivanje](5-Ispitivanje.md) | Pristup ispitivanju, stvarni rezultati i poznati nedostaci |
| [6. Postavljanje, instalacija i konfiguracija](6-Postavljanje-instalacija-i-konfiguracija.md) | Lokalna instalacija, konfiguracija, javno postavljanje i administracija |
| [7. Zaključak i budući rad](7-Zakljucak-i-buduci-rad.md) | Zaključak i moguća daljnja poboljšanja |
| [A. Pregled aktivnosti grupe](A-Pregled-aktivnosti-grupe.md) | Aktivnosti tima, doprinosi i izazovi |
 
## Ključne točke projekta
 
| Kontrolna točka | Demonstracija | Video |
| --- | --- | --- |
| Iteracija 1 (beta) | Demonstracija uživo na laboratorijskoj vježbi | Nije snimljen |
| Završni pregled | Bit će dodano nakon završne implementacije | Bit će dodano |
 
Dokumentacija se kontinuirano ažurira kako se aplikacija razvija.
 
## Organizacija projekta i razvojni proces
 
**Način rada:** Tim se jednom tjedno sastaje putem aplikacije Discord kako bi članovi podijelili individualni napredak i dogovorili ciljeve za idući tjedan. Zadaci se oblikuju kao GitHub Issues koji se organiziraju alatom GitHub Projects.  
**Praćenje trenutačnih zadataka i nedostataka:** [GitHub Issues](https://github.com/CultureVultureFer/culture-vulture/issues)
 
## Pravila dokumentacije
 
Dokumentacija se sastoji od međusobno povezanih Markdown stranica, a UML dijagrami izrađeni su u PlantUML-u. UML izvori čuvaju se u `.puml` datotekama u mapi `docs/puml`, a slike u `.svg` datotekama u mapi `docs/assets/diagrams`.
 
## Akademski integritet, ponašanje i licenciranje
 
README repozitorija sadrži projektnu [izjavu o uporabi umjetne inteligencije](../README.md#uporaba-umjetne-inteligencije), [informacije o kodeksu ponašanja i podršci](../README.md#kodeks-ponašanja-i-podrška) te [status licence ili ponovne uporabe](../README.md#license). Pristupni podaci i druge tajne nikada se ne objavljuju u dokumentaciji niti dijele u običnim porukama.
 
## Izjava o uporabi umjetne inteligencije
 
Kratak sažetak: [README – Uporaba umjetne inteligencije](../README.md#uporaba-umjetne-inteligencije). Ovaj odjeljak bilježi koji su alati korišteni, za koju dokumentaciju ili kod te kako je tim provjerio rezultat. Slijedi FER-ova [pravila o primjerenoj uporabi umjetne inteligencije](https://www.fer.unizg.hr/_download/repository/Policy%20on%20the%20appropriate%20use%20of%20artificial%20intelligence%20at%20the%20faculty%20of%20electrical%20engineering%20and%20computing%5B1%5D.pdf).

### Korišteni alati
 
| Alat | Inačica ili model | Koristio/la | Glavna svrha |
| --- | --- | --- | --- |
| Claude | Sonnet 5.5 | Vanda Meić | Generiranje izvora dijagrama, ispravljanje koda, formatiranje dokumentacije |
| Claude | Opus 5.5 | Tibor Brestovac | Ispravljanje gramatičkih grešaka |
| Gemini | Argon 4 | Karlo Čehulić | Ispravljanje gramatičkih grešaka, formatiranje dokumentacije |
| Claude | Opus 5.5 | Roko Gulić | Generiranje izvora dijagrama |
 
### Opseg doprinosa umjetne inteligencije
 
| Stranica, datoteka ili artefakt | Vrsta pomoći | Što je alat proizveo | Što je tim zadao i promijenio | Lokacija |
| --- | --- | --- | --- | --- |
| UC dijagram | Ispravljanje gramatičkih grešaka | Gramatički ispravljen kod | Ulaz je bio gotovi kod | `docs/puml/3-1-culture-vulture-UC.puml` |
| Home.md | Formatiranje | Formatirana datoteka | Ulaz je bila tekstualna datoteka | `docs/Home.md` |
| SD dijagram, dodavanje događaja | Izvor dijagrama | `.puml` datoteka dijagrama | Ulaz su bili primjer SD dijagrama i opis potrebnog dijagrama | `docs/puml/4-8-culture-vulture-SD-create` |
| SD dijagrami, brisanje i uređivanje događaja | Izvor dijagrama, ispravljanje | Ispravci i cjeloviti kod `.puml` datoteka | Ulaz su bili vlastiti nacrti dijagrama i primjeri kolega | `docs/puml/4-8-culture-vulture-event-delete-SD.puml`, `docs/puml/4-10-culture-vulture-event-edit-SD.puml` |
| CD dijagram | Izvor dijagrama | `.puml` datoteka dijagrama | Ulaz je bio opis potrebnog dijagrama | `docs/puml/4-3-culturevulture-domain-CD` |
| SD dijagrami, prijava i registracija | Ispravljanje gramatičkih grešaka i formatiranje | Gramatički ispravljen i formatiran kod | Ulaz je bio gotovi kod | `docs/puml/4-4-culture-vulture-login-register-user-SD.puml`, `docs/puml/4-5-culture-vulture-login-register-admin-SD.puml` |
| Frontend, stranica za dodavanje i uređivanje događaja | Objašnjenje i ispravljanje koda | Objašnjenja i ispravci koda koji je autorica sama pisala | Ulaz su bili vlastiti isječci koda i upute backend dijela | `frontend/src/pages/EventFormPage.jsx`, `frontend/src/utils/eventForm.js`, `frontend/src/api/events.js` |
 
Stranice i artefakti koji nisu navedeni iznad izrađeni su bez pomoći generativne umjetne inteligencije.
 
### Provjera generiranog sadržaja
 
| Provjera | Kako je provedena | Dokaz |
| --- | --- | --- |
| Činjenična točnost | Svaki član tima pregledao je sadržaj koji je sam izradio uz pomoć umjetne inteligencije i usporedio ga s kodom i pokrenutom aplikacijom | Pregled pojedinih članova; [pregled PR-ova](https://github.com/CultureVultureFer/culture-vulture/pulls) |
| Izvori dijagrama | Generirani PlantUML je iscrtan, ispravljen i uspoređen s ponašanjem backenda (HTTP statusi) | `.puml` datoteke i `.svg` slike u `docs/assets/diagrams` |
| Povjerljivi sadržaj | U alate nisu unošeni pristupni podaci ni tajne | Dogovor tima, [pregled PR-ova](https://github.com/CultureVultureFer/culture-vulture/pulls) |
 
### Pogreške pronađene u izlazu umjetne inteligencije
 
| Problem | Kako je pronađen | Rješenje |
| --- | --- | --- |
| U nacrtu SD dijagrama višak `end` naredbi | PlantUML je javio `Cannot create group` | Uklonjen višak `end` |