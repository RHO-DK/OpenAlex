## Tabelstruktur OpenAlex DB
 - Nedenfor databasestruktur dokumenteret stuktureret
 - Relevante noter inkluderet - tabeltype, inklusionskriterie
 - Inklusionskriterie: authorship-liste > 0
 - 'concepts' depracated i OpenAlex: https://docs.openalex.org/api-entities/concepts - derfor også 'topics'
 - generelt hentes id og serials osv uden url præfix
 
***

### authorships 

**authorships relationstabel** 
**NB: hvis liste tom, så ingen hentning**
Bemærk også primærnøgle:  (work_id, author_id)

| Kolonnenavn      | Type     | Beskrivelse                                                     |
|------------------|----------|-----------------------------------------------------------------|
| work_id          | TEXT     | Fremmednøgle til 'works.work_id'                                |
| author_id        | TEXT     | Fremmednøgle til 'authors.author_id'                            |
| institution_id   | TEXT     | Fremmednøgle til 'institutions.institution_id' (kan være NULL)  |
| author_position  | TEXT     | Position i forfatterrækkefølgen: 'first', 'middle', 'last'      |
| is_corresponding | BOOLEAN  | 'true' hvis kontaktperson på work_id                            |

***

### authors 

**authors entitetstabel** 

**NB: OpenAlex og Orcid ID hentes uden urlpræfix**

| Kolonnenavn | Type     | Beskrivelse                                           |
|-------------|----------|-------------------------------------------------------|
| author_id   | TEXT     | Primærnøgle - OpenAlex ID for forfatteren             |
| name        | TEXT     | Navn ('display_name' fra OpenAlex)                    |
| orcid       | TEXT     | ORCID ID (format:'0000-0000-0000-0000', uden præfix)  |

***

### works 

**works entitetstabel** 

**Om reliabilitet af OpenAlex citationsoptælling se her: https://arxiv.org/abs/2401.16359**

| Kolonnenavn        | Type     | Beskrivelse                                                     |
|--------------------|----------|-----------------------------------------------------------------|
| work_id            | TEXT     | Primærnøgle - OpenAlex ID for værket                            |
| doi                | TEXT     | DOI – 'Digital Object Identifier (kan være NULL)                |
| title              | TEXT     | Værkets titel                                                   |
| publication_date   | DATE     | Udgivelsesdato                                                  |
| publication_year   | INTEGER  | Udgivelsesår                                                    |
| type               | TEXT     | Værkets type - fx 'journal-article', 'book-chapter'             |
| language           | TEXT     | Artikelens sprog, fx 'en', 'da', 'fr'                           |
| cited_by_count     | INTEGER  | Antal gange værk er citeret (OpenAlex opgørelse)                |
| is_oa              | BOOLEAN  | Open Access (`TRUE`/`FALSE`)                                    |
| oa_status          | TEXT     | 'gold', 'green', 'hybrid', 'closed'                             |
| license            | TEXT     | Licens for open access, fx. 'cc-by'                             |
| host_venue_name    | TEXT     | Udgiver/forlag/konference for udgivelse                         |
| host_venue_issn    | TEXT     | ISSN (International Standard Serial Number) fx '1234-5678' unikt|
| host_venue_ror     | TEXT     | ROR-ID for udgiverinstitution (kan være NULL)                   |
| created_date       | DATE     | Hvornår værk registreret i OpenAlex                             |

***

### topics
  - er organiseret hierarkisk:
        1. 'domain' - domæne fx. Health Sciences
        2. 'field' - felt - fx. Medicine
        3. 'subfield' - underkategori - fx. Onkologi
  - entitetstabel - til topics - og der næst relationstabeller for hierarkiet af topics.


 **NB: hentninger uden url-præfix**

 **topics entitetstabel** 


| Kolonnenavn    | Type | Beskrivelse                                                                                   |
| ------------- | ---- | -----------------------------------------------------------------------------------------------|
| topic_id      | TEXT | Primærnøgle – OpenAlex ID for topic (format: 'T0000', uden præfix)                             |
| display_name  | TEXT | Navn på emne                                                                                   |
| subfield_id   | TEXT | Fremmednøgle til 'subfields.subfield_id' - OG - ID for subfield (format: '0000', uden præfix)  |
| subfield_name | TEXT | Navn på subfield, fx 'Oncology'                                                                |
| field_id      | TEXT | ID for felt (format: '00', uden præfix)                                                        |
| field_name    | TEXT | Navn på felt, fx 'Medicine'                                                                    |
| domain_id     | TEXT | ID for domæne (format: '0', uden præfix)                                                       |
| domain_name   | TEXT | Navn på domæne, fx 'Health Sciences'                                                           |


---

**domains entitetstabel** 

| Kolonnenavn  | Type | Beskrivelse                                               |
| ------------ | ---- | --------------------------------------------------------- |
| domain_id    | TEXT | Primærnøgle – ID for domæne (format: '0', uden præfix)    |
| domain_name  | TEXT | Navn på domæne, fx 'Health Sciences'                      |


---

**fields entitetstabel** 


| Kolonnenavn | Type | Beskrivelse                                             |
| ----------- | ---- | --------------------------------------------------------|
| field_id    | TEXT | Primærnøgle –  ID for felt (format: '00', uden præfix)  |
| field_name  | TEXT | Navn på felt, fx 'Medicine'                             |
| domain_id   | TEXT | Fremmednøgle til 'domains.domain_id'                    |


---

**subfields entititestabel** 

| Kolonnenavn   | Type | Beskrivelse                                                 |
| ------------- | ---- | ----------------------------------------------------------- |
| subfield_id   | TEXT | Primærnøgle – ID for subfield (format: '0000', uden præfix) |
| subfield_name | TEXT | Navn på subfield, fx 'Oncology'                             |
| field_id      | TEXT | Fremmednøgle til 'fields.field_id'                          |


***

### work_topics

**work_topics relationstabel**

**NB: score udtrykker relevans - fra 0.0-1.0 - jo højere score jo stærkere relation til emnet**
**is_primary angiver om det er primary_topic (højeste score)**
Bemærk også primærnøgle:  (work_id, topic_id)

| Kolonnenavn | Type    | Beskrivelse                                                                  |
|-------------|---------|------------------------------------------------------------------------------|
| work_id     | TEXT    | Fremmednøgle til 'works.work_id'                                             |
| topic_id    | TEXT    | Fremmednøgle til 'topics.topic_id'                                           |
| score       | FLOAT   | Relevans af topic for værket, OpenAlex system, AI baseret                    |
| is_primary  | BOOLEAN | true hvis topic er værkets 'primary_topic'                                   |


***

### concepts
**NB: LEGACY - concepts udfases til fordel for topics**

 **concepts entitetstabel** 

 | Kolonnenavn   | Type    | Beskrivelse                                                               |
| -------------- | ------- | ------------------------------------------------------------------------- |
| concept_id     | TEXT    | Primærnøgle – ID for concept (format: 'C0000000', uden præfix)            |
| display_name   | TEXT    | Navn på emne, fx 'Cancer'                                                 |
| level          | INTEGER | Hierarkisk: 0 (domæne), 1 (felt), 2 (subfelt), 3 (detaljeret emne)        |
| wikidata_id    | TEXT    | Wikidata-ID (format: 'Q00000', uden præfix)                               |


---

**work_concepts relationsstabel** 

**NB: score udtrykker relevans - fra 0.0-1.0 - jo højere score jo stærkere relation til emnet**
Bemærk også primærnøgle: (work_id, concept_id)

| Kolonnenavn   | Type  | Beskrivelse                                             |
| ------------- | ----- | --------------------------------------------------------|
| work_id       | TEXT  | Fremmednøgle til 'works.work_id'                        |
| concept_id    | TEXT  | Fremmednøgle til 'concepts.concept_id'                  |
| score         | FLOAT | Relevans af concept for værket, OpenAlex score          |


***

### institutions

**institutions entititestabel** 

| Kolonnenavn      | Type | Beskrivelse                                                                            |
| ---------------- | ---- | -------------------------------------------------------------------------------------- |
| institution_id   | TEXT | Primærnøgle – ID for institution (format: 'I00000000', uden præfix)                    |
| display_name     | TEXT | Navn på institution, fx 'University of British Columbia'                               |
| ror              | TEXT | ID for ROR (format: fx '03yrm5c26' uden præfix) - institutionelle metadata via ROR API |
| type             | TEXT | Institutionstype, fx. 'government', 'nonprofit' etc.                                   |
| country_code     | TEXT | Landekode, fx. 'AU', 'USA' etc.                                                        |


***

### citations

**citations relationstabel**

**NB: Relation mellem to værker – vises ved citation** 
Bemærk også primærnøgle: (citing_work_id, cited_work_id)

| Kolonnenavn      | Type   | Beskrivelse                                                     |
|------------------|--------|-----------------------------------------------------------------|
| citing_work_id | TEXT | ID for værk der laver citatet – OpenAlex ID (format: 'W0000000000') |
| cited_work_id  | TEXT | ID for citeret værk – OpenAlex ID (format: 'W0000000000')           |

