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

___

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






