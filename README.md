# OpenAlex Analyseprojekt

Dette projekt demonstrerer struktureret databehandling, analyse og præsentation baseret på OpenAlex – en åben database for videnskabelig publicering. Læs også her: https://docs.openalex.org/

## Funktioner
- Automatisk datahentning via OpenAlex API
- Datamanagement: Strukturering og lagring i PostgreSQL
- Analyse i R med præsentation via Shiny
- Analyse i Python med præsentation via Dash
- Modulær opbygning med mulighed for dashboard eller videreanvendelse

## Struktur
- 'src/': Scripts til ETL og databasehåndtering
- 'notebooks/': Udforskende analyser og visualisering
- 'logs/: Logfiler fra automatiseret datakørsel

## Output
Levere output via flere værktøjer, for at vise overførbarhed af kompetencer - forskellighed relateret til såvel teknologi, som til hvilke beslutninger der kan understøttes - usecases

- 📊 Interaktive dashboards:
  - Python (Dash)
  - R (Shiny)
  - Microsoft Power BI

- 📝 Statisk rapport:
  - 'report.ipynb': Python-baseret rapport i notebook-format
  - 'report.Rmd': R-baseret rapport i markdown-format
  - Fokus på trends, netværk og beslutningsrelevante indsigter


  ## Miljø

- Python-version: 3.9.6  
- Virtuelt miljø: venv ('python3 -m venv openalex')
- Pakkehåndtering: pip  
- Krav: se 'requirements.txt'



