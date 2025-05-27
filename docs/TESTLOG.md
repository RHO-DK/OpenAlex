# TESTLOG

Her dokumenteres gennemførte tests: hvad blev testet, dato, hvordan og resultater

## FORMALIA - brug denne struktur for tilføjelser i loggen:

## [DD-MM-ÅÅÅÅ] [Testens formål]

**Mål**  
Hvad der testes/verificeres

**Handlinger/problemer/løsninger**  
Kørsler, scripts, parametre, værktøjer

**Resultat**  
✅ Succesfuld test  
❌ Fejl
⚠️ Afvigelser

___

## [27-05-2025] Robusthedstest: af parser simuleret ødelagte eller ufuldstændige datastrukturer, dobbeltID etc

**Mål**  
Sikre at fejl håndteres robust, at kun værker med gyldig id indsættes.
Sikre at værker med dobbelt eller samme id ikke indsættes
Sikre håndtering af diversitet af fejl i data: mangler i nestede strukturer, null, eller forkerte værdier, manglende felter etc.
Sikre præcis og velfungerende log på ID og antal indsatte værker
Sikre robust håndtering og fortsat parsing ved fejl.

**Handlinger/problemer/løsninger**  
- En fil med kunstigt indførte fejl blev anvendt til at trigge fejlmeldninger og arbejde med håndtering
- Bla fejl i `id`, `publication_date`, manglende `authorships`, ugyldige nøgler, manglende felter eller nestede elementer, dubletter
- Tilføjede eksisterende `work_id` for at udløse `ON CONFLICT DO NOTHING`
- Kørte paser på filen flere gange og tømte efter hver kørsel entries i tabellen
- Kørsler blev anvendt til iterativ tilretning og mere robust fejlhåndtering.
- Validering sket gennem log og visuel inspektion i pgAdmin
- Flyttet `conn.commit()` til `try`-blokken, for at sikre fortsættelse af parsing
- Tilføjet check af `cur.rowcount` for korrekt tælling af antal tilføjelser i db
- Tilføjet logging af ikke-indførte værker pga. `ON CONFLICT`

**Resultat**  
✅ Fejl i `publication_date`, `id`, `authorships` mv. logges, men indsættes ikke
✅ Transaktionen blev rullet tilbage, for hver fejl, dernæst fortsætter parser og efterfølgende indsættes igen i db
✅ Parseren blev opdateret til kun at øge `inserted` ved `cur.rowcount == 1`



## [27-05-2025] Test af parsing: works_page_001 med ID-stripping

**Mål**  
Teste om værker fra almene OpenAlex strukturer (`works_page_001.json`) kan parses korrekt,  og om ID felter strippes korrekt
Validering af datakvalitet
Test af logfunktioner

**Handlinger/problemer/løsninger**  
- Oprindelig parsing gav NULL i `host_venue_*`-felter, da `host_venue` manglede i mange JSON-entries
- Parser er nu udbedret med fallback-struktur:
  enten `host_venue` hvis ikke så `primary_location.source` ellers tom dict: `{}`
- DOI blev ikke strippet for præfix - dette er nu tilpasset
- licens returnerede udelukkende NULL værdier, da værdien blev forsøgt hentet i forkert dict. 
- licens hentes ikke - nu hentes istedet oa_status (som angiver niveau af åben tilgang)
- Feltet `host_venue_ror` kan også hentes via `.get("host_organization")`, accepter NULL
- Tømte `works`-tabel før ny kørsel (`DELETE FROM works`)
- Kørte parser igen på `works_page_001.json`
- Validerede data før og efter kørsel ved visuel inspektion i pgAdmin, Query tool: `SELECT * FROM public.works
ORDER BY work_id ASC`

**Resultat**  
✅ Fallback struktur virker og rækker indsættes nu korrekt
✅ DOI indsættes nu uden præfix
✅ `host_venue_name` og `issn_l` parses og indsættes tilfredsstillende
✅ Logfunktioner virker tilfredsstillende
✅ oa_status hentes og indføres problemfrit i db
⚠️ `host_venue_ror` er ofte NULL – acceptabelt. 



## [27-05-2025] Test af `strip_id()` – udtræk af ID fra URL-strenge

**Mål**  
Verificere at hjælpefunktionen `strip_id()` korrekt stripper ID'er for præfixer, samt kan håndtere mindre afvigelser

**Handlinger**  
- Kørt `tests/test_strip_id.py` via terminal
- `strip_id()` importeres fra `src/utils/helpers.py`
- Test af:
  - OpenAlex-ID: `"https://openalex.org/W123"`
  - ORCID: `"https://orcid.org/0000-0002-1234-5678"`
  - DOI: `"https://doi.org/10.18637/jss.v082.i13"`
  - Ingen præfix: `"JustAnID"`
  - Ikke-streng: `None`

**Resultat**  
✅ Tests gennemført uden fejl - ingen AssertionError
✅ `strip_id()`løser opgaven tilredsstillende og kan anvendes i parsing

---

## [2025-05-26] Hentning af data fra OpenAlex API

**Mål**  
Verificere at `extract_openalex.py` henter og gemmer alle relevante works relateret til danske forfattere.

**Handlinger**
- Kørte `python src/extract/extract_openalex.py`
- Overvågede `logs/extract_openalex.log`
- Tjekkede `data/raw/` for oprettede JSON-filer
- Bekræfter at sidste side returnerer tom og afslutter hentning.

**Resultat**  
✅ Hentning gennemført, 2248 sider hentet og gemt i ´data/raw`(.gitignore)
✅ Hver side gemt som JSON
✅ Sidste cursor returnerede tom side og script stoppede korrekt


## DB - oprettelse af tabeller

**Mål**  
Bekræfte at `db.py` opretter planlagte tabeller i `openalex_db`, med præcis og relevant logging

**Handlinger**
- Kørte `python src/db.py`
- Overvågede logfil `logs/db_setup.log`
- Verificerede i pgAdmin at alle tabeller blev oprettet.
- Indekser blev oprettet (bekræftet via log og pgAdmin).

**Resultat**  
✅ Alle tabeller og indekser blev oprettet uden fejl.  
⚠️ To tastefejl i fil blev fundet via loggen (rettet efterfølgende).






