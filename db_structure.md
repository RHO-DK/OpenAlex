## Struktur og indhold, keys og relationer  tables... works, authorships, institutions, (concepts?)
Overordnede guides for parsing: 
 - hvis authorshipsliste tom, så ingen placering



### authorships **relationstabel** – db-struktur
**NB: hvis liste tom, så ingen hentning**
Bemærk også primærnøgle:  (work_id, author_id)

| Kolonnenavn      | Type     | Beskrivelse                                                     |
|------------------|----------|-----------------------------------------------------------------|
| work_id          | TEXT     | Fremmednøgle til 'works.work_id'                                |
| author_id        | TEXT     | Fremmednøgle til 'authors.author_id'                            |
| institution_id   | TEXT     | Fremmednøgle til 'institutions.institution_id' (kan være NULL)  |
| author_position  | TEXT     | Position i forfatterrækkefølgen: 'first', 'middle', 'last'      |
| is_corresponding | BOOLEAN  | 'true' hvis kontaktperson på work_id                            |



### authors **entitetstabel** - db-struktur

**NB: OpenAlex og Orcid ID hentes uden urlpræfix**

| Kolonnenavn | Type     | Beskrivelse                                           |
|-------------|----------|-------------------------------------------------------|
| author_id   | TEXT     | Primærnøgle - OpenAlex ID for forfatteren             |
| name        | TEXT     | Navn ('display_name' fra OpenAlex)                    |
| orcid       | TEXT     | ORCID ID (format:'0000-0000-0000-0000', uden præfix)  |




### works **kombineret entitets og relationsstabel** – db-struktur

Bemærk også primærnøgle:  (work_id, author_id)


| Kolonnenavn      | Type     | Beskrivelse                                                     |
|------------------|----------|-----------------------------------------------------------------|
| work_id          | TEXT     | Fremmednøgle til 'works.work_id'                                |
| author_id        | TEXT     | Fremmednøgle til 'authors.author_id'                            |
| institution_id   | TEXT     | Fremmednøgle til 'institutions.institution_id' (kan være NULL)  |
| author_position  | TEXT     | Position i forfatterrækkefølgen: 'first', 'middle', 'last'      |
| is_corresponding | BOOLEAN  | 'true' hvis kontaktperson på work_id                            |