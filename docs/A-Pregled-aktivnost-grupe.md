# A. Pregled aktivnosti grupe

## A.1 Evidencija sastanaka

**Kratice članova tima:** KČ = Karlo Čehulić; TF = Tomislav Facković; RG = Roko Gulić; MK = Matija Krivec; IB = Ivan Bunić; TB = Tibor Brestovac; VM = Vanda Meić.

|Datum i sudionici|Glavna tema|Donesena odluka ili zadatak|Poveznica na zadatak ili rezultat, ako postoji|
|-|-|-|-|
|15. 10. 2026.; svi (KČ, TF, RG, MK, IB, TB, VM)|Organizacija tima i početna raspodjela uloga|KČ je odabran za voditelja tima i full-stack člana. Tim je podijeljen na frontend (VM, IB, TF) i backend (TB, MK, RG). Dogovoreni su termini tjednih sastanaka i otvoren Discord poslužitelj za komunikaciju.|—|
|18. 10. 2026.; svi|Uspostava repozitorija i odabir tehnologija|Kreiran je GitHub repozitorij. Odabrani su Python/Django za backend, React za frontend i PostgreSQL za bazu podataka. TB je zadužen za početnu dokumentaciju (`README.md` i prijedlog teme).|[Issue #1](https://github.com/CultureVultureFer/culture-vulture/issues/1), [Issue #2](https://github.com/CultureVultureFer/culture-vulture/issues/2), [Issue #4](https://github.com/CultureVultureFer/culture-vulture/issues/4), [PR #7](https://github.com/CultureVultureFer/culture-vulture/pull/7), [PR #13](https://github.com/CultureVultureFer/culture-vulture/pull/13)|
|25. 10. 2026.; svi osim IB|Organizacija projektnog rada i proširenje opsega projekta|Odabran je GitHub Projects za praćenje zadataka. Dogovoreno je proširenje opsega projekta i korištenje Ticketmastera kao vanjskog API-ja. KČ je preuzeo izradu dokumentacijskih issuea, a VM je započela izradu dizajna u Figmi.|[PR #3](https://github.com/CultureVultureFer/culture-vulture/pull/3)|
|31. 10. 2026.; TB, RG, MK, KČ|Modeliranje baze i dohvat događaja|Dogovorena je organizacija i inicijalizacija baze podataka. MK je zadužen za ERD dijagram, izradu liste događaja i pozive Ticketmaster API-ja za dohvat događaja.|[Issue #14](https://github.com/CultureVultureFer/culture-vulture/issues/14), [Issue #16](https://github.com/CultureVultureFer/culture-vulture/issues/16), [PR #7](https://github.com/CultureVultureFer/culture-vulture/pull/7), [PR #13](https://github.com/CultureVultureFer/culture-vulture/pull/13), [PR #28](https://github.com/CultureVultureFer/culture-vulture/pull/28), [PR #29](https://github.com/CultureVultureFer/culture-vulture/pull/29), [PR #30](https://github.com/CultureVultureFer/culture-vulture/pull/30)|
|1. 11. 2026.; svi osim VM i IB|Raspodjela izrade dijagrama i prijave putem Google OIDC-a|KČ je raspodijelio izradu dijagrama: TB izrađuje UC dijagram, RG CD dijagram, a KČ SD dijagram. RG je zadužen za prijavu putem Google OIDC-a.|[Issue #17](https://github.com/CultureVultureFer/culture-vulture/issues/17), [PR #33](https://github.com/CultureVultureFer/culture-vulture/pull/33)|
|8. 11. 2026.; svi|Raspodjela frontend zadataka i dovršetak OAuth-a|Frontend zadaci raspodijeljeni su ovako: VM izrađuje funkcionalnosti kreiranja i brisanja događaja, TF početnu stranicu, IB prikaz detalja događaja, a KČ prijavu. TB dovršava OAuth.|[Issue #5](https://github.com/CultureVultureFer/culture-vulture/issues/5), [Issue #11](https://github.com/CultureVultureFer/culture-vulture/issues/11), [Issue #12](https://github.com/CultureVultureFer/culture-vulture/issues/12), [PR #46](https://github.com/CultureVultureFer/culture-vulture/pull/46), [PR #47](https://github.com/CultureVultureFer/culture-vulture/pull/47), [PR #56](https://github.com/CultureVultureFer/culture-vulture/pull/56)|
|15. 11. 2026.; svi|Pregled implementiranih funkcionalnosti i priprema beta-verzije|Predstavljene su dotad implementirane funkcionalnosti. Tim je započeo pripremu beta-verzije aplikacije i nastavio rad na projektnoj dokumentaciji i dijagramima.|[Issue #18](https://github.com/CultureVultureFer/culture-vulture/issues/18), [Issue #24](https://github.com/CultureVultureFer/culture-vulture/issues/24), [Issue #34](https://github.com/CultureVultureFer/culture-vulture/issues/34), [PR #57](https://github.com/CultureVultureFer/culture-vulture/pull/57), [PR #58](https://github.com/CultureVultureFer/culture-vulture/pull/58), [PR #60](https://github.com/CultureVultureFer/culture-vulture/pull/60), [PR #61](https://github.com/CultureVultureFer/culture-vulture/pull/61), [PR #65](https://github.com/CultureVultureFer/culture-vulture/pull/65)|

Evidencija prikazuje glavne odluke i dodjelu odgovornosti na sastancima. Pojedinačni zadaci i rezultati detaljnije su navedeni u A.2 i A.3.

## A.2 Plan rada

|Razdoblje/Tjedan|Glavni planirani rad|Odgovorni članovi|Poveznica na zadatke|
|-|-|-|-|
|Projektni tjedan 1 (15. 10. – 21. 10.)|Formiranje tima, odabir voditelja i podjela na frontend i backend. Dogovor načina komunikacije i termina sastanaka. Kreiranje GitHub repozitorija, odabir tehnologija i izrada početne dokumentacije.|Svi članovi; KC koordinira organizaciju tima, TB početnu dokumentaciju.|[Issue #1](https://github.com/CultureVultureFer/culture-vulture/issues/1), [Issue #2](https://github.com/CultureVultureFer/culture-vulture/issues/2), [Issue #4](https://github.com/CultureVultureFer/culture-vulture/issues/4), [PR #7](https://github.com/CultureVultureFer/culture-vulture/pull/7), [PR #13](https://github.com/CultureVultureFer/culture-vulture/pull/13), [PR #3](https://github.com/CultureVultureFer/culture-vulture/pull/3)|
|Projektni tjedan 2 (22. 10. – 28. 10.)|Organizacija zadataka putem GitHub Projects, proširenje opsega projekta i odabir Ticketmaster API-ja. Započinjanje izrade dizajna aplikacije i definiranje zadataka vezanih uz dokumentaciju.|KC, VM, svi članovi tima.||
|Projektni tjedan 3 (29. 10. – 4. 11.)|Izrada ERD dijagrama, organizacija i inicijalizacija baze podataka te implementacija dohvata događaja putem Ticketmaster API-ja. Raspodjela izrade UML dijagrama i početak implementacije prijave putem Google OIDC-a.|MK, TB, RG, KC.|[Issue #14](https://github.com/CultureVultureFer/culture-vulture/issues/14), [Issue #16](https://github.com/CultureVultureFer/culture-vulture/issues/16), [Issue #17](https://github.com/CultureVultureFer/culture-vulture/issues/17), [PR #28](https://github.com/CultureVultureFer/culture-vulture/pull/28), [PR #29](https://github.com/CultureVultureFer/culture-vulture/pull/29), [PR #30](https://github.com/CultureVultureFer/culture-vulture/pull/30), [PR #33](https://github.com/CultureVultureFer/culture-vulture/pull/33)|
|Projektni tjedan 4 (5. 11. – 11. 11.)|Raspodjela frontend zadataka među članovima tima: izrada funkcionalnosti kreiranja i brisanja događaja, homepagea, detalja događaja i prijave. Dovršavanje OAuth autentifikacije.|VM, TF, IB, KC, TB.|[Issue #5](https://github.com/CultureVultureFer/culture-vulture/issues/5), [Issue #11](https://github.com/CultureVultureFer/culture-vulture/issues/11), [Issue #12](https://github.com/CultureVultureFer/culture-vulture/issues/12), [PR #46](https://github.com/CultureVultureFer/culture-vulture/pull/46), [PR #47](https://github.com/CultureVultureFer/culture-vulture/pull/47), [PR #56](https://github.com/CultureVultureFer/culture-vulture/pull/56)|
|Projektni tjedan 5 (12. 11. – 18. 11.)|Predstavljanje dosad implementiranih funkcionalnosti, priprema aplikacije za predaju beta verzije te nastavak rada na projektnoj dokumentaciji i preostalim funkcionalnostima.|Svi članovi tima.|[Issue #18](https://github.com/CultureVultureFer/culture-vulture/issues/18), [Issue #24](https://github.com/CultureVultureFer/culture-vulture/issues/24), [Issue #34](https://github.com/CultureVultureFer/culture-vulture/issues/34), [PR #57](https://github.com/CultureVultureFer/culture-vulture/pull/57), [PR #58](https://github.com/CultureVultureFer/culture-vulture/pull/58), [PR #60](https://github.com/CultureVultureFer/culture-vulture/pull/60), [PR #61](https://github.com/CultureVultureFer/culture-vulture/pull/61), [PR #65](https://github.com/CultureVultureFer/culture-vulture/pull/65)|

Plan rada prikazuje glavne aktivnosti i raspodjelu odgovornosti tijekom razvoja projekta. Navedene aktivnosti temelje se na održanim sastancima i dogovorima tima, dok se njihov stvarni napredak i rezultati mogu pratiti kroz povezane GitHub zadatke i promjene u repozitoriju.

## A.3 Aktivnosti i doprinosi članova

|Aktivnost ili rezultat|Član|Prijavljeni sati|Reprezentativni rezultat ili poveznica|
|-|-|-:|-|
|Frontend: implementacija kreiranja, uređivanja i brisanja događaja za organizatora|VM|15|[Issue #51](https://github.com/CultureVultureFer/culture-vulture/issues/51), [Issue #54](https://github.com/CultureVultureFer/culture-vulture/issues/54), [PR #61](https://github.com/CultureVultureFer/culture-vulture/pull/61)|
|Backend: implementacija kreiranja, uređivanja i brisanja događaja za organizatora|RG|4|[Issue #51](https://github.com/CultureVultureFer/culture-vulture/issues/51), [Issue #54](https://github.com/CultureVultureFer/culture-vulture/issues/54)|
|Dizajn stranica i korisničkog sučelja u Figmi|VM|10|[Issue #5](https://github.com/CultureVultureFer/culture-vulture/issues/5), [Issue #11](https://github.com/CultureVultureFer/culture-vulture/issues/11), [Issue #12](https://github.com/CultureVultureFer/culture-vulture/issues/12)|
|Frontend: prikaz detalja događaja|IB|5|[Issue #50](https://github.com/CultureVultureFer/culture-vulture/issues/50), [PR #66](https://github.com/CultureVultureFer/culture-vulture/pull/66)|
|Backend: dohvat pojedinačnog događaja i njegovih detalja|MK|6|[Issue #50](https://github.com/CultureVultureFer/culture-vulture/issues/50), [PR #64](https://github.com/CultureVultureFer/culture-vulture/pull/64)|
|Frontend: prijava/registracija organizatora|KČ|7|[PR #32](https://github.com/CultureVultureFer/culture-vulture/pull/32)|
|Backend: prijava/registracija organizatora|TB|10|[PR #46](https://github.com/CultureVultureFer/culture-vulture/pull/46)|
|Frontend: implementacija početne stranice|TF|6|[PR #56](https://github.com/CultureVultureFer/culture-vulture/pull/56)|
|Frontend: implementacija funkcionalnosti tražilice|KČ|4|[Issue #55](https://github.com/CultureVultureFer/culture-vulture/issues/55), [PR #62](https://github.com/CultureVultureFer/culture-vulture/pull/62)|
|Backend: implementacija funkcionalnosti tražilice|TB|3|[Issue #55](https://github.com/CultureVultureFer/culture-vulture/issues/55), [PR #62](https://github.com/CultureVultureFer/culture-vulture/pull/62)|
|Dokumentacija: `README.md`, opis projekta, analiza zahtjeva, obrasci uporabe i UC dijagram|TB|6|[Issue #8](https://github.com/CultureVultureFer/culture-vulture/issues/8), [Issue #21](https://github.com/CultureVultureFer/culture-vulture/issues/21), [Issue #22](https://github.com/CultureVultureFer/culture-vulture/issues/22), [Issue #23](https://github.com/CultureVultureFer/culture-vulture/issues/23), [PR #7](https://github.com/CultureVultureFer/culture-vulture/pull/7), [PR #65](https://github.com/CultureVultureFer/culture-vulture/pull/65)|
|Dokumentacija: arhitektura i oblikovanje, CMP dijagram te SD dijagram registracije i prijave|KČ|5|[Issue #24](https://github.com/CultureVultureFer/culture-vulture/issues/24), [PR #10](https://github.com/CultureVultureFer/culture-vulture/pull/10), [PR #48](https://github.com/CultureVultureFer/culture-vulture/pull/48)|
|Dokumentacija: CD dijagram|RG|1|[PR #49](https://github.com/CultureVultureFer/culture-vulture/pull/49)|
|Dokumentacija: SD dijagrami|VM|2|[Issue #35](https://github.com/CultureVultureFer/culture-vulture/issues/35), [Issue #59](https://github.com/CultureVultureFer/culture-vulture/issues/59)|
|Dokumentacija: ERD dijagram|MK|2|[Issue #16](https://github.com/CultureVultureFer/culture-vulture/issues/16), [Issue #42](https://github.com/CultureVultureFer/culture-vulture/issues/42)|

Prijavljeni sati predstavljaju procjenu uloženog rada članova tima. Broj sati sam po sebi nije mjera kvalitete ni dokaz dovršenosti; navedene poveznice upućuju na zadatke i rezultate povezane s pojedinom aktivnošću.

## A.4 Pregled promjena u repozitoriju

**Prikaz aktivnosti repozitorija**: Generirani graf doprinosa na GitHub-u: [CultureVulture – Contributors](https://github.com/CultureVultureFer/culture-vulture/graphs/contributors)

**Razdoblje:** Od početka aktivnosti repozitorija u listopadu 2026. do trenutka izrade pregleda.

GitHub-ov graf prikazuje doprinose u obliku commit-ova. Ne obuhvaća cjelokupan rad na dizajnu, planiranju, ispitivanju, pregledima koda i dokumentaciji, pa ga treba promatrati zajedno s tablicom A.3, a ne kao mjeru ukupnog rada pojedinog člana.

## A.5 Ključni inženjerski izazovi i rješenja

**Cilj:** Dokumentirati konkretne tehničke prepreke, poduzete korake i konačni ishod, uključujući ograničenja koja su ostala prisutna.

|Izazov|Poduzeta radnja|Ishod ili preostalo ograničenje|
|-|-|-|
|Ticketmaster API vraćao je velik broj događaja s različitih lokacija, što je otežavalo obradu i prikaz svih rezultata u opsegu projekta.|KČ i MK privremeno su ograničili dohvat događaja na jedan grad – Berlin.|Aplikacija dohvaća događaje samo za Berlin. Time je pojednostavljena obrada podataka, ali je geografska pokrivenost aplikacije trenutačno ograničena na jedan grad.|
|Sinkronizacija događaja u stvarnom vremenu putem Ticketmaster API-ja stvarala je prevelik broj poziva prema bazi podataka.|MK je odlučio dohvaćati i osvježavati događaje periodično, svakih 10 minuta.|Broj poziva prema bazi je smanjen, ali podaci se ne osvježavaju u stvarnom vremenu. Promjene na Ticketmaster-u mogu se u aplikaciji prikazati s odgodom do približno 10 minuta.|



