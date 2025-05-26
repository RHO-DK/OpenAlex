
# 📄 Datahåndtering og dokumentation

Nedenfor beskrives hvordan data indsamles, håndteres, valideres og opbevares i projektet. 

Projektet anvender udelukkende Open Access-data og er ikke underlagt institutionelle krav om en data management plan (DMP).

Projektet forholder sig til udvalgte principper for at sikre kvalitet af data og resultater, og transparens om formål og anvendte metoder.

Beskrivelsen er udformet gennem inspektion og gennemlæsning af enkeltstående åbne DMP'er på siden: https://dmp.deic.dk/public_plans

---

## 1. Projektbeskrivelse

- **Titel**: OpenAlex Analyseprojekt
- **Formål**: Illustrere/videreudvikle kompetence til struktureret databehandling, analyse og præsentation af fund. Alt baseret på data fra OpenAlex, ROR og ORCID
- **Data**: Videnskabelige/institutionelle/forskningsbaserede metadata
- **Teknisk ramme**: PostgreSQL, Python, OpenAlex API, ROR API, ORCID API
- **Ansvarlig**: Rikke Have Odgaard (privat projekt)

---

## 2. Datatyper

- Metadata om videnskabelige artikler: DOI, titel, sprog, udgivelsesdato, citationer
- Metadata om forfattere: navn, ORCID, institutionel tilknytning
- Metadata om emner: domæne, felt, subfelt, topics, (concepts - legacy)
- Relationer mellem værker, forfattere, institutioner og emner
- Ingen personfølsomme data
- Ingen originaldata kun beskrivende metadata fra åbne kilder


---

## 3. Datakilder

- Alle kilder er offentligt tilgængelige og har Open Access-licens
- **OpenAlex**  – metadata om værker, forfattere og emner
- **ROR API** – metadata om forskningsinstitutioner (lokation, type, relationer)
- **ORCID API** – supplerende metadata om forfattere (tilknytninger, publikationer)

---

## 4. Databehandling og struktur

- Data hentes via OpenAlex API i JSON-format
- Parser skrevet i Python indfører data i relationelle tabeller
- Database struktureret efter normaliseret relationsmodel (dokumenteret i 'db_structure.md')
- Redundans i strukturen er balanceret med hensyn til optimal analyse
- Det er planalagt at integrere supplerende metadata fra ROR og ORCID, gemmes i egne tabeller og kobles til OpenAlex-data med nøgler
- Formål med supplement er at anvende kontekstbasede oplysninger om geografi, relationer og karriereforløb, fx. til netværksanalyse


---

## 5. Dokumentation og metadata

- Databasens struktur og felter er dokumenteret i 'db_structure.md'
- Ændringer dokumenteres løbende i 'CHANGELOG.md'
- Kode til parsing og databehandling findes i projektets kildekode ('db.py', 'etl_openalex.py' etc)

---

## 6. Datavalidering og kvalitet

- **Før indsættelse**: Parsing filtrerer på fx 'authorships > 0'
- **Under indsættelse**: Unikke constraints og relationelle nøgler sikrer konsistens
- **Efter indsættelse**: Der valideres på tomme felter, dubletter og uventede relationer

---

## 7. Lagring og backup

- Data lagres lokalt i PostgreSQL
- DB Backup sker manuelt ved komprimering og eksport til eksternt drev
- Projektmapper versioneres i åbent projekt i GitHub

**Backupfil gemmes i et krypteret cloud-miljø (filen.io)**
**Backup består af læsbar .sql-fil som komprimeres og uploades**

læsbar, komprimeret SQL-backup:
"pg_dump -U postgres -d openalex_db -F p -f openalex_backup.sql"
"gzip openalex_backup.sql"

dekomprimer og gendan fra SQL-backup:
"gunzip openalex_backup.sql.gz"
"psql -U postgres -d openalex_db_restored -f openalex_backup.sql"

---

## 8. Adgang og deling

- Data deles ikke som del af projektet, men kan frit hentes via de åbne kilder.
- Kildestruktur og kode deles frit via GitHub

---

## 9. Langtidsbevaring

- Projektet afsluttes som statisk version 
- Der er ikke planlagt løbende vedligehold
- Projektet arkiveres som read-only med tydelig datering

---

## 10. Ansvar og roller

- Projektet drives og vedligeholdes af én person
- Ingen institutionel forankring eller ansvar
- Kode, dokumentation og datamodel er udarbejdet af projektets ejer

---

## 11. Fremtidig opdatering

- Der implementeres **ikke** løbende opdatering af data
- Projektets struktur muliggør fremtidig opdatering via OpenAlex API, fx:
  - Genindlæsning af værker med opdateret 'updated_date' (ikke del af nuværende DB struktur)
  - Selektiv opdatering af citationstal og tilknytninger
  - Planlagt automatiseret synkronisering, fx JS7 JobScheduler
- Opdateringslogik beskrives, men implementeres ikke

---


## 12. Licens og citation

- Projektet er et læringsprojekt til personlig brug
- Der anvendes udelukkende Open Access-kilder
- Ved brug af kode eller struktur henvises til projektets GitHub-repositorie

