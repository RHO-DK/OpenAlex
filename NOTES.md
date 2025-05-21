## API-Overblik 

**OpenAlex**

- Begyndte med at hente data via Postman - få insigt i OpenAlex før konkret indhentning
    - prøvesøgning: https://api.openalex.org/works?filter=authorships.institutions.country_code:DK&group_by=concepts.id - works, fra danmark, grupperet på emner, giver indsigt i hvilke emner der udgives under i DK
    - mere konkret  - forstå OpenAlex' datastruktur - til at forme præcise requests: https://api.openalex.org/works?filter=from_publication_date:2020-01-01&per-page=1 
- Hentning baseret på OpenAlex dokumentation:
    https://docs.openalex.org/

  ### Hentning konkrete elementer:
    - cursor paging, relevant for at udtømme forespørgsler

    - enhedstyper: Works, Authors, Sources, Institutions, Concepts, Publishers, Funders



**ORCID**
 - giver mulighed for at analysere på forfatter via unikt ID:
  https://info.orcid.org/documentation/ - orcid api - dok.


**ROR** 
 - ORCID skal kombineres med ROR - research identification registry - for geodata:
  https://ror.readme.io/docs/basics



## Filtrering og datavalg

OpenAlex:



ORCID:

ROR



## Datamodel og database
**for detaljer se db_structure.md**



## Analyseovervejelser


1. Systematiske krydstjek og anden kvalitetssikring af data – herunder særligt på tværs af datakilder – for at vurdere validitet og sammenhæng.
2. Grundlæggende nøgletal og overblik via Power BI – overordnet forskningsaktivitet, publikationer og funding (statisk formidling).
3. Bibliometrisk analyse i R – visualisering af faglig udvikling, citationer og aktivitetsniveau over tid – evt. koblet til centrale hændelser (fx større reformer, policies/overordnede beslutninger, internationale begivenheder).
4. Netværksanalyse i Python – dybere undersøgelse af samarbejdsrelationer baseret på fund fra R-analysen (emnevalg afledt af mønstre i aktivitet).



### Power BI
**Formål:** KPI-orienteret overblik og grundlæggende indsigt
**Datakilder:**
- OpenAlex: `concepts, works, grants, institutions


### R
**Formål:** Bibliometrisk analyse – faglig aktivitet og udvikling
**Datakilder:** 
- OpenAlex: `concepts,`works, authors, citations, institutions


### Python
**Formål:** Netværksanalyse – samarbejdsmønstre og strukturelle sammenhænge
**Datakilder:**
- OpenAlex: `works, authors, institutions - in different particular concepts
- ORCID: forfatterkarriere, positioner
- ROR: instituitionsmetadata, geografi



## Resultater og refleksioner
