import os
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Model ogłoszenia do dodawania
class OgloszenieIn(BaseModel):
    tytul: str
    uczelnia: str
    przedmiot: str
    forma: str  # "stacjonarna" lub "online"
    dystans_km: float


# Początkowa baza ogłoszeń (spełniająca scenariusze BDD)
OGLOSZENIA = [
    {
        "id": 1,
        "tytul": "Korepetycje z Analizy",
        "uczelnia": "Politechnika Warszawska",
        "przedmiot": "Analiza matematyczna",
        "forma": "stacjonarna",
        "dystans_km": 1.5,
    },
    {
        "id": 2,
        "tytul": "Pomoc z Fizyki",
        "uczelnia": "AGH",
        "przedmiot": "Fizyka",
        "forma": "stacjonarna",
        "dystans_km": 2.5,
    },
    {
        "id": 3,
        "tytul": "Statystyka online",
        "uczelnia": "UJ",
        "przedmiot": "Statystyka",
        "forma": "online",
        "dystans_km": 0.0,
    },
]


@app.get("/")
def strona_glowna():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


# Endpoint do pobierania i filtrowania (US-03)
@app.get("/api/ogloszenia")
def pobierz_ogloszenia(
    uczelnia: str | None = Query(None),
    przedmiot: str | None = Query(None),
    forma: str | None = Query(None),
    max_dystans_km: float | None = Query(None),
):
    wyniki = OGLOSZENIA

    if uczelnia:
        wyniki = [
            o
            for o in wyniki
            if o["uczelnia"].lower() == uczelnia.strip().lower()
        ]

    if przedmiot:
        wyniki = [
            o
            for o in wyniki
            if przedmiot.strip().lower() in o["przedmiot"].lower()
        ]

    if forma:
        wyniki = [
            o for o in wyniki if o["forma"].lower() == forma.strip().lower()
        ]

    if max_dystans_km is not None:
        wyniki = [o for o in wyniki if o["dystans_km"] <= max_dystans_km]

    # Scenariusz BDD: Brak wyników
    if not wyniki:
        return {
            "message": "Brak ogłoszeń",
            "przycisk": "Wyczyść filtry",
            "dane": [],
        }

    return {"dane": wyniki}


# Endpoint do dodawania nowego ogłoszenia
@app.post("/api/ogloszenia")
def dodaj_ogloszenie(ogloszenie: OgloszenieIn):
    nowe_id = max([o["id"] for o in OGLOSZENIA], default=0) + 1
    nowy_wpis = {
        "id": nowe_id,
        "tytul": ogloszenie.tytul,
        "uczelnia": ogloszenie.uczelnia,
        "przedmiot": ogloszenie.przedmiot,
        "forma": ogloszenie.forma,
        "dystans_km": ogloszenie.dystans_km,
    }
    OGLOSZENIA.insert(0, nowy_wpis)
    return {"message": "Dodano ogłoszenie", "dane": nowy_wpis}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)