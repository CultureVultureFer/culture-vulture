# Obrasci uporabe

## Dijagram obrazaca uporabe

![Dijagram obrazaca uporabe](images/usecase.svg)

## Specifikacije obrazaca uporabe 

**UC1: Registracija i prijava** 
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-001 |
|Preduvjeti, ako postoje| nema |
|Glavni tijek| 1. Korisnik odabire prijavu ili registraciju<br>2. Aplikacija preusmjerava korisnika na OAuth 2.0 servis.<br>3. Korisnik se prijavljuje kod vanjskog servisa<br>4. Aplikacija prima potvrdu identiteta<br>5. Aplikacija priakazuje početnu stranicu prijavljenog korisnika|
|Alternativni ili neuspješni tijekovi, ako postoje| **3a. Korisnik odustaje**: aplikacija ga vraća na početnu stranicu prijave<br>**4a. Autentikacija nije uspjela**: aplikacija ga vraća na početnu stranicu prijave|
|Rezultat| Korisnik je prijavljen ili pri prvoj prijavi kreiran je novi račun|

**UC2: Komentiranje i recenzija**
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-002 |
|Preduvjeti, ako postoje| Korisnik je uspješno prijavljen |
|Glavni tijek| 1. Korisnik odabire događaj<br>2. Korisnik ostavlja ocjenu<br>3. Korisnik ostavlja komentar|
|Alternativni ili neuspješni tijekovi, ako postoje| **3b.** Korisnik ne ostavlja komentar nego samo ocjenu |
|Rezultat| Ocjena i opcionalno komentar ostavljeni na nekom događaju |

**UC3: Sortiranje događaja**
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-015 |
|Preduvjeti, ako postoje| Korisnik je prijavljen |
|Glavni tijek| 1.Korisnik odabire način sortiranja |
|Alternativni ili neuspješni tijekovi, ako postoje| nema |
|Rezultat| Događaji sortirani po odabranom načinu |

**UC4: Dodavanje i brisanje događaja**
|Polje|Opis|
|---|---|
|Primarni akter| Organizator |
|ID zahtjeva| F-010 |
|Preduvjeti, ako postoje| Organizator prijavljjen |
|Glavni tijek| 1. Organizator unosi podatke događaja<br>2. Organizator objavljuje događaj|
|Alternativni ili neuspješni tijekovi, ako postoje|**1a. Organizator unese krive podatke (lokacija, datum, itd)**: Aplikacija upozorava na pogrešne podatke i ne dozvoljava objavu |
|Rezultat| Događaj je objavljen i vidljiv korisnicima |

**UC5: Prikaz lokacije na karti**
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-005 |
|Preduvjeti, ako postoje| Korisnik je prijavljen u sustav |
|Glavni tijek| 1. Korisnik otvara detalje događaja<br>2. Aplikacija dohvaća kartu od Google Maps API-ja<br>3. Aplikacija prikazuje kartu s označenom lokacijom događaja|
|Alternativni ili neuspješni tijekovi, ako postoje| **2.a neuspješan dohvat lokacije** Aplikacija prikazuje adresu događaja kao tekst bez karte |
|Rezultat| Korisnik vidi lokaciju događaja |

**UC6: Pregled događaja u radijusu trenutne lokacije**
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-006 |
|Preduvjeti, ako postoje| Korisnik je prijavljen |
|Glavni tijek| 1. Korisnik u pregledu događaja odabire pregled događaja u svojoj blizini<br>2. Aplikacija traži dopuštenje za pristup lokaciji<br>3. Korisnik odabire radijus<br>4. Aplikacija prikazuje kartu s događajima unutar odabranog radijusa trenutne lokacije |
|Alternativni ili neuspješni tijekovi, ako postoje| **2a. Korisnik odbija dopuštenje** Aplikacija ga obavještava kako je dopuštenje pristupu lokaciji nužno i vraća ga na stranicu pregleda događaja<br>**4a. Lokaciju nije moguće odrediti** Aplikacija obavještava korisnika i nudi ponovni pokušaj |
|Rezultat| Korisnik vidi događaje unutar odabranog radijusa svoje trenutne lokacije |

**UC7: Uređivanje profila**
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-007 |
|Preduvjeti, ako postoje| Korsnik je prijavljen |
|Glavni tijek| 1. Korisnik otvara svoj profil<br>2. Aplikacija prikazuje podatke profila<br>3. Korisnik mijenja podatke i potvrđuje promjene<br>4. Aplikacija provjerava podatke i sprema promjene<br>5. Aplikcija prikazuje promjene |
|Alternativni ili neuspješni tijekovi, ako postoje| **4a. Uneseni podatci su netočni** Aplikacija obavještava korisnika i vraća ga na korak 3 |
|Rezultat| Korisnik uspješno mijenja svoje podatke profila |

**UC8: Pretraživanje događaja**
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-008 |
|Preduvjeti, ako postoje| Korisnik je prijavljen |
|Glavni tijek| 1. Korisnik upisuje naziv organizatora ili događaja po kojem želi pretraživati<br>2. Aplikacija pretražuje događaje po zadanom nazivu i prikazuje ih korisniku |
|Alternativni ili neuspješni tijekovi, ako postoje||
|Rezultat| Korisnik vidi događaje koji odgovaraj pretraživanom pojmu |

**UC9: Dodavanje događaja u kalendar**
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-009 |
|Preduvjeti, ako postoje| Korisnik je prijavljen |
|Glavni tijek| 1. Korisnik odabire željeni događaj<br>2. Korisnik odabire opciju dodaj u kalendar<br>3. Aplikacija korisnika traži dopuštenje za Google Calendar<br>4. Aplikacija dodaje događaj u korisnikov kalendar |
|Alternativni ili neuspješni tijekovi, ako postoje| **3a. Korisnik odbija dopuštenje** Aplikacija ga obavještava kako radnju nije moguće dovršiti bez dopuštenja i vraća korisnika na stranicu pregleda detalja događaja<br>**4a. Google Calendar API nije dostupan** Aplikacija obavještava korisnika o neupsjehu i nudi mu opciju ponovnog pokušaja |
|Rezultat| Korisnik može dodati događaj u svoj Google Calendar |

**UC10: Pregled događaja**
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-003 |
|Preduvjeti, ako postoje| Korisnik je prijavljen |
|Glavni tijek| 1. Korisniku prikazani svi dosutpni događaji |
|Alternativni ili neuspješni tijekovi, ako postoje||
|Rezultat| Korisnik ima pregled događaja |

**UC11: Upravljanje događajima**
|Polje|Opis|
|---|---|
|Primarni akter| Organizator |
|ID zahtjeva| F-004, F-010 |
|Preduvjeti, ako postoje| Organizator je prijavljen |
|Glavni tijek| 1. Organizator odabire kreiranje događaja ili upravljanje već postojećim vlastitim događajem<br>2. Organizator unosi podatke i sprema promjene<br>3. Aplikacija provjerava podatke i sprema promjene<br>4. Aplikacija prikazuje unesene podatke |
|Alternativni ili neuspješni tijekovi, ako postoje| **3a. Uneseni podaci su netočni** Aplikacija upozorava organizatora i vraća ga na korak 2 |
|Rezultat| Organizator kreira, uređuje ili briše vlastite događaje |

**UC12: Upravljanje profilima**
|Polje|Opis|
|---|---|
|Primarni akter| Administrator |
|ID zahtjeva| F-013 |
|Preduvjeti, ako postoje| Administrator je prijavljen |
|Glavni tijek| 1. Administrator odabire popis korisnika i organizatora<br>2. Administrator odabire željeni profil<br>3. Administrator mijenja podatke profila i potvrđuje promjene<br>4. Aplikacija provjerava podatke i sprema ih<br>5. Aplikacija prikazuje ažurirane podatke profila |
|Alternativni ili neuspješni tijekovi, ako postoje| **4a. Uneseni podaci su netočni** Aplikaija upozorava Administratora i vraća ga na korak 3 |
|Rezultat| Podaci odabranog profila su promijenjeni |

**UC13: Pregled detalja događaj**
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-014 |
|Preduvjeti, ako postoje| Korisnik je prijavljen |
|Glavni tijek| 1.Korisnik odabire željeni događaj<br>2. Aplikacija korisniku pokazuje detalje događaja |
|Alternativni ili neuspješni tijekovi, ako postoje||
|Rezultat| Korisnik vidi detalje događaja |

**UC14: Filtriranje događaja**
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-016 |
|Preduvjeti, ako postoje| Korisnik je prijavljen |
|Glavni tijek| 1. Korisnik na stranici pregleda događaja odabire filter<br>2. Aplikacija filtira podatke po kateogorijama i prikazuje ih korisniku |
|Alternativni ili neuspješni tijekovi, ako postoje||
|Rezultat| Korisnik vidi događaje samo iz odabranih kategorija |

**UC15: Brisanje komentara**
|Polje|Opis|
|---|---|
|Primarni akter| Korisnik |
|ID zahtjeva| F-017 |
|Preduvjeti, ako postoje| Korisnik je prijavljen i komentar već postoji |
|Glavni tijek| 1. Korisnik odabire događaj na kojem želi obrisati svoj komentar<br>2. Korisnik briše svoj komentar<br>3. Aplikacija  briše komentar i ažurira prikaz komentara na događaju |
|Alternativni ili neuspješni tijekovi, ako postoje||
|Rezultat| Korisnikov komentar je obrisan i više nije vidljiv |

**UC16: Pregled vlastitih događaja**
|Polje|Opis|
|---|---|
|Primarni akter| Organizator |
|ID zahtjeva| F-011 |
|Preduvjeti, ako postoje| Organizator je prijavljen |
|Glavni tijek| 1. Organizator odabire prikaz vlastitih događaja<br>2. Aplikacija prikazuje događaje organizatora |
|Alternativni ili neuspješni tijekovi, ako postoje||
|Rezultat| Organizator ima pregled nad vlastitim događajima |