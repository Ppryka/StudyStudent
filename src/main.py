from fastapi import FastAPI

# InicjalizacjaFastAPI 
app = FastAPI(
    title="StudyStudent",
    version="1.0.0",
)
@app.get("/")
def read_root():
    return {"message": "Witaj w aplikacji}
