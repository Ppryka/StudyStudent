import json
import os
from datetime import datetime, timedelta
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(
    title="StudyStudent",
    version="1.0.0",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLIK_OGLOSZEN = os.path.join(BASE_DIR, "ogloszenia.json")


PROFIL_STUDENTA = {
    "imie": "Marek",
    "uczelnia": "AGH",
    "kierunek": "Informatyka",
    "rok_studiow": 2,
    "uzupelniony": True,
}


class Ogloszenie(BaseModel):
    tytul: Optional[str] = None
    opis: str
    kategoria: str
    tag: str
    forma: Literal["Stacjonarnie", "Online"] = "Stacjonarnie"
    status: str = "Aktywne"
    data_publikacji: Optional[str] = None


def dzis(dni_wstecz: int = 0) -> str:
    return (datetime.now() - timedelta(days=dni_wstecz)).strftime("%Y-%m-%d")


DOMYSLNE_OGLOSZENIA = [
    {
        "id": 1,
        "tytul": "Korepetycje z matematyki",
        "opis": "Szukam osoby do wspólnego przerobienia całek przed kolokwium z matematyki.",
        "kategoria": "Nauka",
        "tag": "Matma",
        "forma": "Stacjonarnie",
        "status": "Aktywne",
        "data_publikacji": dzis(),
    },
    {
        "id": 2,
        "tytul": "Pomoc z C++",
        "opis": "Pomogę w zrozumieniu wskaźników i programowania obiektowego w C++.",
        "kategoria": "Nauka",
        "tag": "Programowanie",
        "forma": "Online",
        "status": "Aktywne",
        "data_publikacji": dzis(),
    },
    {
        "id": 3,
        "tytul": "Piwo wieczorem",
        "opis": "Szukam ekipy na wspólne wyjście na piwo dziś wieczorem.",
        "kategoria": "Wspolne wyjscie",
        "tag": "Impreza",
        "forma": "Stacjonarnie",
        "status": "Aktywne",
        "data_publikacji": dzis(),
    },
    {
        "id": 4,
        "tytul": "Rajd rowerowy jutro zbiórka",
        "opis": "Jutro organizuję rajd rowerowy, zapraszam wszystkich chętnych na zbiórkę.",
        "kategoria": "Wspolne wyjscie",
        "tag": "Sport",
        "forma": "Stacjonarnie",
        "status": "Aktywne",
        "data_publikacji": dzis(),
    },
    {
        "id": 5,
        "tytul": "Nauka fizyki na kolokwium",
        "opis": "Potrzebuję pomocy z zadaniami z mechaniki klasycznej na zaliczenie z fizyki.",
        "kategoria": "Nauka",
        "tag": "Fizyka",
        "forma": "Online",
        "status": "Aktywne",
        "data_publikacji": dzis(35),
    },
]


def zapisz_ogloszenia(lista):
    with open(PLIK_OGLOSZEN, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)


def wczytaj_ogloszenia() -> list:
    if os.path.exists(PLIK_OGLOSZEN):
        with open(PLIK_OGLOSZEN, "r", encoding="utf-8") as f:
            return json.load(f)

    zapisz_ogloszenia(DOMYSLNE_OGLOSZENIA)
    return DOMYSLNE_OGLOSZENIA


OGLOSZENIA = wczytaj_ogloszenia()


def wyslij_strone():
    sciezka_html = os.path.join(BASE_DIR, "index.html")

    if os.path.exists(sciezka_html):
        return FileResponse(sciezka_html)

    return {"message": "Witaj w aplikacji"}


@app.get("/", include_in_schema=False)
def strona_glowna():
    return wyslij_strone()


@app.get("/admin", include_in_schema=False)
def strona_admina():
    return wyslij_strone()


@app.get("/api/ogloszenia")
def pobierz_ogloszenia(
    kategoria: Optional[str] = None,
    tag: Optional[str] = None,
):
    granica_30_dni = datetime.now() - timedelta(days=30)
    zmieniono = False

    for o in OGLOSZENIA:
        data_pub = datetime.strptime(o["data_publikacji"], "%Y-%m-%d")
        if o["status"] == "Aktywne" and data_pub < granica_30_dni:
            o["status"] = "Wygasłe"
            zmieniono = True

    if zmieniono:
        zapisz_ogloszenia(OGLOSZENIA)

    wyniki = [o for o in OGLOSZENIA if o["status"] == "Aktywne"]

    if kategoria:
        wyniki = [o for o in wyniki if o["kategoria"].lower() == kategoria.lower()]

    if tag:
        wyniki = [o for o in wyniki if o["tag"].lower() == tag.lower()]

    return wyniki


# Dodawanie nowego ogłoszenia
@app.post("/api/ogloszenia", status_code=201)

def dodaj_ogloszenie(dane: Ogloszenie):

    if not PROFIL_STUDENTA["uzupelniony"]:
        raise HTTPException(
            status_code=403,
            detail="Profil jest wymagany. Uzupełnij profil przed dodaniem ogłoszenia.",
        )

    opis_czysty = dane.opis.strip()
    if len(opis_czysty) < 20:
        raise HTTPException(
            status_code=400,
            detail="Opis problemu musi mieć co najmniej 20 znaków.",
        )
    if len(opis_czysty) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Opis problemu może mieć maksymalnie 1000 znaków.",
        )

    forma_czysta = dane.forma.strip().capitalize()


    tytul = (dane.tytul or "") or opis_czysty[:20]

    nowe_id = max((o["id"] for o in OGLOSZENIA)) + 1

    nowe = {
        "id": nowe_id,
        "tytul": tytul,
        "opis": opis_czysty,
        "kategoria": dane.kategoria,
        "tag": dane.tag,
        "forma": forma_czysta,
        "status": "Aktywne",
        "data_publikacji": dane.data_publikacji or dzis(),
    }

    OGLOSZENIA.insert(0, nowe)
    zapisz_ogloszenia(OGLOSZENIA)

    return nowe


@app.delete("/api/ogloszenia/{ogloszenie_id}")
def usun_ogloszenie(ogloszenie_id: int):
    for i, o in enumerate(OGLOSZENIA):
        if o["id"] == ogloszenie_id:
            OGLOSZENIA.pop(i)
            zapisz_ogloszenia(OGLOSZENIA)
            return {"message": "Ogłoszenie zostało usunięte.", "id": ogloszenie_id}

    raise HTTPException(status_code=404, detail="Nie znaleziono ogłoszenia o podanym id.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
