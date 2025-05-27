# OpenAlex Analyseprojekt

Dette projekt demonstrerer struktureret databehandling, analyse og præsentation baseret på OpenAlex, ROR og ORCID – åbne databaser for videnskabelig publicering, insitutionsdata og forskeridentifikator.

## Funktioner
- Automatisk datahentning via OpenAlex, ROR og ORCID AÅI
- Datamanagement: Strukturering og lagring i PostgreSQL
- Analyse visualiseret med PowerBI Pro
- Analyse i R med præsentation via Shiny
- Analyse i Python med præsentation via Dash
- Modulær opbygning med mulighed for dashboard eller videreanvendelse

## Struktur
- `src/`: Scripts til ETL og databasehåndtering
- `docs/`: Sekundære dokumenter, der understøtter/dokumenterer arkitektur, test, beslutninger og planlægning.
- `tests`: Testfiler - udviklingsstøtte i forhold til fejlscenarier, validering etc.
- `logs/`: Logfiler fra automatiseret datakørsel
- `notebooks/`: Udforskende analyser og visualisering

## Output
Levere output via flere værktøjer, for at vise overførbarhed af kompetencer - forskellighed relateret til såvel teknologi, som til hvilke beslutninger der kan understøttes - usecases

- Interaktive dashboards:
  - Python (Dash)
  - R (Shiny)
  - Microsoft Power BI

- Statisk rapport:
  - 'report.ipynb': Python-baseret rapport i notebook-format
  - 'report.Rmd': R-baseret rapport i markdown-format
  - Fokus på trends, netværk og beslutningsrelevante indsigter


## Miljø
- Python-version: 3.9.6  
- Virtuelt miljø: venv ('python3 -m venv openalex')
- Pakkehåndtering: pip  
- Krav: se 'requirements.txt'

## Datahåndtering

- Der benyttes offentligt tilgængelige metadata fra OpenAlex, ROR og ORCID. 
- Data struktureres og analyseres i en lokal PostgreSQL-database.

For beskrivelse af data håndtering: `docs/data_management.md`





