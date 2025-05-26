## API-Overblik database indhold og tests

**OpenAlex**

- Begyndte med at hente data via Postman - få insigt i OpenAlex før konkret indhentning
    - prøvesøgning: https://api.openalex.org/works?filter=authorships.institutions.country_code:DK&group_by=concepts.id - works, fra danmark, grupperet på emner, giver indsigt i hvilke emner der udgives under i DK
    - mere konkret  - forstå OpenAlex' datastruktur - til at forme præcise requests: https://api.openalex.org/works?filter=from_publication_date:2020-01-01&per-page=1 
- Hentning baseret på OpenAlex dokumentation:
    https://docs.openalex.org/

### Hentning konkrete elementer:
   - cursor paging, relevant for at udtømme forespørgsler
   - enhedstyper: Works, Authors, Sources, Institutions, Concepts (legacy), Topics, (Publishers, Funders)

**standardiseret blok til indsætning i alle filer der behøver path til config.py**
"
import sys
import os

# føjer src til eksportsti
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

"


### Tests

   - 25.5.22: en **test**hentning giver problemer: urllib3 advarer om manglende OpenSSL-kompatibilitet (LibreSSL 2.8.3). dog ingen praktiske problemer bemærket

**Test af fejllogning i fetch_works()** sandbox/testLoggingFetch.py

- Simuleret 'ValueError' manuelt for at sikre, at 'except' fanger ukendte fejl
- Testet forkert endpoint for at udløse HTTP-fejl (404)
- Testet lav 'timeout' for at udløse 'TimeoutError'
- Bekræftet:
  - Logging sker korrekt i logs/test.log
  - Kort INFO-logging ved succesfuldt kald.
  - Detaljeret fejllogging ved exceptions.
  - 'RotatingFileHandler' fungerer – log overskrives ikke men fortsættes

Status: Logging fungerer som ønsket.



**ORCID**
 - giver mulighed for at analysere på forfatter via unikt ID:
  https://info.orcid.org/documentation/ - orcid api - dok.


**ROR** 
 - ORCID skal kombineres med ROR - research identification registry - for geodata:
  https://ror.readme.io/docs/basics

---
## Datavalidering
multifaceteret:
- før hentning ved design fx. db-struktur - unique values, og FK'er, PK'er
- under hentning - parsinglogikker - fx. hvis liste med authorships er tom så skip
- efter implementering, men før analyse: krydstjek på dubletter, på tomme felter, inspicer nulls etc.

måske skal der laves en struktureret beskrivelse af dette for at sikre dokumentation af netop dette?
---

## OpenAlex data

### Citationer og begrænsninger

I det nuværende setup hentes kun danske værker, hvilket betyder:

- Langt størstedelen af de citerede værker ('cited_work_id') findes ikke som fulde dataposter i databasen
- Der kan ikke hentes institutions- eller emnedata for citerede værker uden yderligere kald til OpenAlex API
- Derfor er det vigtigt at understrege: 
    Analysen kan **ikke** anvendes til at vurdere bias i citationsmønstre mellem dansk og international forskning.
    En overvægt af "udenlandske citationer" afspejler umiddelbart mønster af global forskningsproduktion, og ikke en forskningspolitisk realitet.

Evt kan selektive udvidelser tilføjes på sigt - fx. mest citerede værker.

---

## ORCID data:

---


## ROR data

---

## Datamodel og database
**for detaljer se db_structure.md**

---
## Data Mangement Plan

**information der har været hjælpsom**

info og underlinks fra SDU (der er også adgang til at se åbne DMP'er og lade sig inspirere):
https://libguides.sdu.dk/godakademiskpraksis/datamanagement


online kursus - gratis:
https://mantra.ed.ac.uk/


___

## Logging
attributter: https://docs.python.org/3/library/logging.html#logrecord-attributes

## Analyseovervejelser og usecases


1. Systematiske krydstjek og anden kvalitetssikring af data – herunder særligt på tværs af datakilder – for at vurdere validitet og sammenhæng.
2. Grundlæggende nøgletal og overblik via Power BI – overordnet forskningsaktivitet, publikationer og funding (statisk formidling).
3. Bibliometrisk analyse i R – visualisering af faglig udvikling, citationer og aktivitetsniveau over tid – evt. koblet til centrale hændelser (fx større reformer, policies/overordnede beslutninger, internationale begivenheder).
4. Netværksanalyse i Python – dybere undersøgelse af samarbejdsrelationer baseret på fund fra R-analysen (emnevalg afledt af mønstre i aktivitet).

---

### Power BI
**Formål:** KPI-orienteret overblik og grundlæggende indsigt
**Datakilder:**
- OpenAlex: topics, works, grants, institutions

#### narrativ usecase

**Institutionsaktivitet i dansk forskning**

Narrativ:
“En beslutningstager i en dansk forskningsinstitution ønsker overblik over institutionens publikationsaktivitet og udvikling i relation til bestemte emner og adgangsformer. 

Jeg forbereder et visuelt overblik over udvikling i tid, fordelt på institutioner, (afgrænsende) emner og åben adgang til (type af) udgivelser."


Datakrav - med henvisning til db-table:
- works (publication_year, is_oa, oa_status, evt. license, evt. type)
- topics (field eller sub_field)
    -evt. filtrering via topics.subfield_name, fx 'Artificial Intelligence'.
- evt. concepts - samme fokus som ovenfor
- institutions (name og type)
- authorships (for institutions)


Spørgsmål:
 - Hvilke institutioner publicerer mest inden for eksempelvis "AI" og kan evt. sammenlignes med andre emner, der måske er mindre aktuelle?
 - Hvor mange af institutionernes artikler indenfor emnet er open access/type af access?
 - Hvordan ser udviklingen ud over tid, varierer leadership fx?


Output:
- Tidsserier (linje- og søjlediagrammer) med antal publikationer fordelt på emner og OA-status
- Overlagte diagrammer der sammenligner udvalgte institutioner over tid og emner.


---

### R
**Formål:** Bibliometrisk analyse – faglig aktivitet og udvikling
**Datakilder:** 
- OpenAlex: topics, works, authors, citations, institutions


#### narrativ usecase

**Forskersynlighed og faglig udvikling over tid - DK**

Narrativ:
“Jeg vil analysere danske forskeres aktivitet og synlighed over de seneste 10 år. Jeg vil kende til omfang af både publikationer og citationer, fordelt på fagområder. Jeg har særligt interesse i om særlige emner vinder frem, om der er områder der overses, eller måske endog stagnerer."


Datakrav – med henvisning til db-tabeller:
 - works (publication_year, cited_by_count, type)
 - topics (subfield_name, field_name, domain_name).
    - evt filtreres via topics.subfield_name, fx. Artifical Intelligence
 -  authorships og institutions (for institutionsnavne og typer)


Spørgsmål:
 - hvilke subfields vokser hurtigt målt i antal publikationer
 - emner med høj citationsvækst (både samlet og pr. publikation)
 - Skift over tid - i publikationstyper
 - Er der skift i forskningsfokus over tid – målt som percentilbaseret vækst i citationer inden for subfields


Output:
- Tidsserier - interaktive linje og søjlediagrammer - sortering på emne
- heatmaps der viser aktivitet og citationer - sortering på subfield+år
- percentil vækst i citationer baseret på subfield+år 
- (Evt.) Overblik over mest citerede danske authors sorteret på institution



### Python
**Formål:** Netværksanalyse – samarbejdsmønstre og strukturelle sammenhænge
**Datakilder:**
- OpenAlex: works, authors, institutions - in different particular concepts
- ORCID: forfatterkarriere, positioner
- ROR: instituitionsmetadata, geografi


#### narrativ usecase 
Nb - afventer integration med orcid og ror data 




## Resultater og refleksioner
