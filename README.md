Valitsen aiheekseni resurssienhallinnan työkalun, koska olen tehnyt töitä SAP MRP:n parissa, niin aihe tuntuu luontevalta.
Sovelluksessani käyttäjä voi lisätä ja luoda tarpeita eri resursseille, lisätä materiaaleja fyysisiin sijainteihin ja 
allokoida niitä erilaisiin projekteihin. Käyttäjä voi myös käynnistää projekteja, jotka kuluttavat resursseja. Rerursseille voi 
asettaa erilaisia ominaisuuksia määrän ja tarpeiden/varauksien lisäksi kuten muistiinpanoja ja päivämääriä. Käyttäjille voi 
asettaa erilaisia oikeuksia. 

Tietokantasovelluksesta puuttuu vielä kokonaan materiaalinhallinta, projektikohtaiset materiaalin tarpeet, sekä lokit.

## Ohjeet

Kopioi repo omalle koneellesi johonkin johonkin sopivaan hakemistoon (git clone git@github.com:attepajula/Web-tietokanta.git). Sitten suorita "source venv/bin/activate", "pip install -r requirements.txt".

Luo tietokanta avaamalla psql, jossa suoritat: "CREATE DATABASE [uuden tietokantasi nimi]"
Sitten aseta schema uuteen tietokantaasi: "psql -U [käyttäjänimesi] -d [uuden tietokantasi nimi] -f schema.sql"

Luo ympäristömuuttuja itse tai aja envsetup.py. Itse se hoituu suorittamalla juurikansiossa "touch .env", "nano .env", jonne lisäät rivit: 
DATABASE_URL=postgresql:///[uuden tietokantasi nimi]
SECRET_KEY=[tämän saat ajamalla "python3", "import secrets", "secrets.token_hex(16)" ja lisäämällä tulosteen tämän paikalle]

Suorita: "flask run --reload"
