from fastapi import FastAPI

# Inicjalizacja frameworka FastAPI
app = FastAPI(
    title="StudyBuddy API",
    description="Aplikacja do laczenia studentow w celu nauki i wspólnych wyjsc.",
    version="1.0.0",
)
