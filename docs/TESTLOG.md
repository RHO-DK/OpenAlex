# TESTLOG

Her dokumenteres gennemførte tests: hvad blev testet, dato, hvordan og resultater

## FORMALIA - brug denne struktur for tilføjelser i loggen:

## [DD-MM-ÅÅÅÅ] [Testens formål]

**Mål**  
Hvad der testes/verificeres

**Handlinger**  
Kørsler, scripts, parametre, værktøjer

**Resultat**  
✅ Succesfuld test  
❌ Fejl
⚠️ Afvigelser

---

## [2025-05-28] Hentning af data fra OpenAlex API

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

---

## [2025-05-27] DB - oprettelse af tabeller

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






