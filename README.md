Valitsen aiheekseni resurssienhallinnan työkalun, koska olen tehnyt töitä SAP MRP:n parissa, niin aihe tuntuu luontevalta.
Sovelluksessani käyttäjä voi lisätä luoda tarpeita eri resursseille, lisätä materiaaleja fyysisiin sijainteihin ja 
allokoida niitä erilaisiin projekteihin. Käyttäjä voi myös käynnistää projekteja, jotka kuluttavat resursseja. Rerursseille voi 
asettaa erilaisia ominaisuuksia määrän ja tarpeiden/varauksien lisäksi kuten muistiinpanoja ja päivämääriä. Käyttäjille voi 
asettaa erilaisia oikeuksia. 

Aja appsetup.py aluksi. Tietokantasovelluksesta puuttuu vielä kokonaan projektien hallinta, materiaalinhallinta, projektikohtaiset materiaalin tarpeet ja mahdollisuus jakaa projekteja toiselle käyttäjälle, sekä lokit.

Jos on ongelmia aja komento "pip3 install werkzeug python-dotenv flask", jos appsetup.py ei onnistu virtuaaliympäristön luomisessa, niin luo se käsin: "python3 -m venv venv", "source venv/bin/activate".
