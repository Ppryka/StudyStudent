import os
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(
    title="StudyBuddy",
    version="1.0.0",
)

#sciezka dostepu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OGLOSZENIA = [
    {
        "id": 1,
        "tytul": "Korepetycje z matematyki",
        "kategoria": "Nauka",
        "tag": "Matma",
    },
    {
        "id": 2,
        "tytul": "Kurs Pythona dla początkujących",
        "kategoria": "Nauka",
        "tag": "Programowanie",
    },
    {
        "id": 3,
        "tytul": "Pokój jednoosobowy do wynajęcia",
        "kategoria": "Mieszkanie",
        "tag": "Wynajem",
    },
    {"id": 4, "tytul": "Sprzedam rower miejski", "kategoria": "Sport", "tag": "Rower"},
    {
        "id": 5,
        "tytul": "Oddam podręczniki do biologii",
        "kategoria": "Nauka",
        "tag": "Książki",
    },
]


@app.get("/", include_in_schema=False)
def strona_glowna():
    sciezka_html = os.path.join(BASE_DIR, "index.html")

    if os.path.exists(sciezka_html):
        return FileResponse(sciezka_html)

    return {
        "message": "Witaj w aplikacji"
    }


# Filtrowanie ogloszen
@app.get("/api/ogloszenia")
def pobierz_ogloszenia(kategoria: Optional[str] = None):

    if kategoria:
        return [
            o
            for o in OGLOSZENIA
            if o["kategoria"].lower() == kategoria.lower()
        ]

    return OGLOSZENIA


if __name__ == "__main__":
    import uvicorn

    
    uvicorn.run(app, host="127.0.0.1", port=8000)
