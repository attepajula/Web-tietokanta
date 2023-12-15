Valitsen aiheekseni resurssienhallinnan työkalun, koska olen tehnyt töitä SAP MRP:n parissa, niin aihe tuntuu luontevalta.
Sovelluksessani käyttäjä voi lisätä ja luoda tarpeita eri resursseille, lisätä materiaaleja fyysisiin sijainteihin ja 
allokoida niitä erilaisiin projekteihin. Käyttäjä voi myös käynnistää projekteja, jotka kuluttavat resursseja. Rerursseille voi 
asettaa erilaisia ominaisuuksia määrän ja tarpeiden/varauksien lisäksi kuten muistiinpanoja ja päivämääriä. Käyttäjille voi 
asettaa erilaisia oikeuksia. 

Tietokantasovelluksesta puuttuu vielä kokonaan materiaalinhallinta, projektikohtaiset materiaalin tarpeet, sekä lokit.

## Ohjeet

Kopioi repo omalle koneellesi johonkin johonkin sopivaan hakemistoon (git clone git@github.com:attepajula/Web-tietokanta.git). Sitten suorita "source venv/bin/activate", "pip install -r requirements.txt" ja "psql -U [käyttäjänimesi] -d [db] -f schema.sql.

Suorita: "flask run --reload"
