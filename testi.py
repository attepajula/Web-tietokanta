from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError

def testaa_tietokantayhteys():
    try:
        # Luo tietokantayhteys
        # Luo tietokantayhteys
        engine = create_engine("postgresql://localhost/attepajula")

        # Luo tietokantametadata
        metadata = MetaData()

        # Lataa taulujen nimet
        metadata.reflect(bind=engine)
        taulut = metadata.tables.keys()

        # Tulosta taulujen nimet
        print("Tietokannan taulut:")
        for taulu in taulut:
            print(f"- {taulu}")
    except Exception as e:
        print(f"Virhe tulostaessa taulujen nimiä: {e}")

if __name__ == "__main__":
    testaa_tietokantayhteys()