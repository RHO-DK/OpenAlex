# Changelog

Tilføjes med logikken: MAJOR.MINOR.PATCH (1.1.1), og dertil dato for ændring. 

## [0.9.0] – 2025-05-29

### Ændring:
- Ny arbejdsform: CI-workflow via GitHub Actions - der arbejdes med kodevalidering
  - Workflowfil `lint-og-test.yml` oprettet under `.github/workflows/`
  - Validerer kodekvalitet med `pylint`
  - Tester funktionalitet med `pytest` på testfiler (unittests)
  - Kører ved `push` og `pull_request` til `main`
- Eksisterende testfiler for parsing og instering til`works` anvendes fortsat og har fokus på datavalidering
- Etableret klar adskillelse mellem automatiserede CI-tests og manuelle datavalideringstests
  - CI-tests skal være uafhængige af database og ydre afhængigheder
  - Parsertests med realdata udføres manuelt, dokumenteres i `TESTLOG.md`

### Fremadrettet praksis:
- Nye parserkomponenter opdeles i `parse_*` og `insert_*` - med henblik på automatiseret unittesting
- `parse_*` skal være CI-testbare og rene for sideeffekter
- `insert_*` holdes testbare via de etablerede manuelle datavalideringsprocedurer
- `parse_and_insert_*` bruges kun som wrapper i `__main__`-konteksten


## [0.8.0] – 2025-05-27

### Ændring i Databasestruktur
- I tabel works ændres lices til oa_status
- Årsag: mere intuitivt og let at forstå niveau af åben tilgang til udgivelsen


## [0.7.0] – 2025-05-27

### Ændring:
- ny mappestruktur: test og doc mappe tilføjet
- flyttet alle sekundære docs filer til docmappe (DMP, db-struktur-notes)
- oprettet "TESTLOG.md" til bedre dokumentation af tests (i dir docs)
- fremadrettet dokumenteres resultater af tests ikke her - men i TESTLOG.md
- unittesting etc køres ikke fra filer i "sandbox" (.gitignore), men via filer i dir tests


---

## [0.6.0] – 2025-05-26


### Tilføjet
- Første version af 'extract_openalex.py' klar - der er kørt tests af hent og log og gem via sandbox
- Hetede filer gemmes gemmes i rodmappen i 'data/raw/03', sidevis som json filer, klar til parsing
- Tilføjet diverse fejlhåndtering: timeout, HTTP-fejl, ukendte fejl
- Logging sat op med RotatingFileHandler til `logs/extract_openalex.log`


## [0.5.0] – 2025-05-26

## Ændring: Robust fejlhåndtering og udvidet logging i db.py og constraints_db.py

- Tilføjet try/except-blokke omkring tabel- og indeksering af.
- Inkluderet traceback.format_exc() for detaljeret fejlsporing
- Logging fortsat til både konsol og fil for al kritisk funktionalitet
- Forbedringen af fejlovervågning, giver mere detaljeret indsigt og adgang til forståelse og håndtering af fejl
- fokuseret på udvikling, ikke drift.


---


## [0.4.0] – 2025-05-22

### Tilføjet: Normalisering af topics-tabellen
 - Redundante felter subfield_name, field_name og domain_name er fjernet fra topics-tabel. 
 - Names skal nu hentes med JOIN med hhv subfields- , fields- og domains-tabeller
 - Hensigt: sikre emnehieriarkiet og reducere risiko for datadivergens.


### Tilføjet simple PowerBI og Shiny usecases i NOTES.md
- Tjekket db struktur vha simple usecases relevant for OpenAlex data
- Usecases er unikt tilpasset kodningskontekst/visualiseringsredskab

### Ændret:: 'db_structure.md'
- dokumenteret `institutions`og `citations`tabeller

### Tilføjet 'CHANGELOG.md'
- indført logging som fast struktur
- ført tilbagedateret log (nedenfor) via løbende versionskontrol

---

## [0.3.0] – 2025-05-21

### Tilføjet 'db_strukture.md'
- Dokumenteret `topics` og `concepts` som entitetstabeller med relationstabeller
- Tilføjet hierarkisk struktur med `domains`, `fields`, `subfields`
- Tilføjet `work_topics` og `work_concepts` relationstabeller
- Ydereligere Afklaring og struktur for integration med data fra ORCID og ROR

### Ændret 'db_structure.md'
- Ensretning og præcisering af beskrivelser i 'works' og 'topics'

---

## [0.2.0] – 2025-05-15

### Tilføjet til projekt
- Første databaseplan: 'works', 'authors', 'authorships'
- Oprettet dokumenationsfil for db strukturer ('db_structure.md')


---

## [0.1.0] – 2025-05-14

### Påbegyndt projekt
- Oprettelse af projektstruktur og dokumentationsfiler
