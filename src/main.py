import os
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(
    title="StudyStudent",
    version="1.0.0",
)

# Sciezka
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
        "tytul": "Zrobie za kogos zadania z c++",
        "kategoria": "Nauka",
        "tag": "Programowanie",
    },
    {
        "id": 3,
        "tytul": "Piwo wieczorem",
        "kategoria": "Wspolne wyjscie",
        "tag": "Impreza",
    },
    {   "id": 4,
        "tytul": "Rajd rowerowy jutro zbiorka",
        "kategoria": "Wspolne wyjscie",
        "tag": "Sport"},
    {
        "id": 5,
        "tytul": "Szukam osoby do nauki fizyki na jutrzejsze kolokwium",
        "kategoria": "Nauka",
        "tag": "Fizyka",
    },
]


@app.get("/", include_in_schema=False)
def strona_glowna():
    sciezka_html = os.path.join(BASE_DIR, "index.html")

    if os.path.exists(sciezka_html):
        return FileResponse(sciezka_html)

    return {"message": "Witaj w aplikacji"}


# Filtrowanie ogłoszen
@app.get("/api/ogloszenia")
def pobierz_ogloszenia(
    kategoria: Optional[str] = None,
    tag: Optional[str] = None
):
    wyniki = OGLOSZENIA

    # Filtrowanie po kategorii
    if kategoria:
        wyniki = [
            o for o in wyniki if o["kategoria"].lower() == kategoria.lower()
        ]

    # Filtrowanie po
    if tag:
        wyniki = [
            o for o in wyniki if o["tag"].lower() == tag.lower()
        ]

    return wyniki


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
