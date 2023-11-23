Valitsen aiheekseni resurssienhallinnan työkalun, koska olen tehnyt töitä SAP MRP:n parissa, niin aihe tuntuu luontevalta.
Sovelluksessani käyttäjä voi lisätä luoda tarpeita eri resursseille, lisätä materiaaleja fyysisiin sijainteihin ja 
allokoida niitä erilaisiin projekteihin. Käyttäjä voi myös käynnistää projekteja, jotka kuluttavat resursseja. Rerursseille voi 
asettaa erilaisia ominaisuuksia määrän ja tarpeiden/varauksien lisäksi kuten muistiinpanoja ja päivämääriä. Käyttäjille voi 
asettaa erilaisia oikeuksia. 

Tietokantasovelluksesta puuttuu vielä kokonaan projektien hallinta, materiaalinhallinta, projektikohtaiset materiaalin tarpeet ja mahdollisuus jakaa projekteja toiselle käyttäjälle, sekä lokit.

## ohjeet

Kopioi repo omalle koneellesi johonkin johonkin sopivaan hakemistoon (git clone git@github.com:attepajula/Web-tietokanta.git). Aja appsetup.py aluksi. Sitten aja tablesetup.py VIRTUAALIYMPÄRISTÖSSÄ.

Todennäköisesti virtuaaliympäristö ei jää sinulle päälle, joten käynnistä se itse uudestaan "source venv/bin/activate", ennekuin ajat "flask run --reload"

Jos appsetup.py ei onnistu virtuaaliympäristön luomisessa, niin luo se käsin: "python3 -m venv venv", "source venv/bin/activate". Sitten aja komento "pip3 install werkzeug python-dotenv flask" virtuaaliympäristössä, jonka jälkeen pääset ajamaan tablesetup.py ja luomaan palvelimen "flask run --reload".
