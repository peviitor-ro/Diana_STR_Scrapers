# Modificări necesare pentru a testa o nouă companie:

## Pentru SCRAPER:

1. Schimbă numele clasei de la `Akwel_scrapper` la `Noul_nume_companie_peviitor`.

2. Actualizează numele constantei `SCRAPER_URL` cu noul URL specific companiei.

## Pentru PEVIITOR:

1. Schimbă numele clasei de la `Akwel_peviitor` la `Noul_nume_companie_peviitor`.

2. La linia 19, înlocuiește `send.keys("nume companie")` cu `send.keys("noul nume al companiei")`.

## Pentru TEST:

1. Schimbă numele claselor din care se instantiază obiectele:
`NumeCompanie_scrapper(driver)`
`NumeCompanie_peviitor(driver)`