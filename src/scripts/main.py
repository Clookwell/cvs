from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routes import datasets, visualizations

app = FastAPI(title="Data Explorer API",
              description="API для аналізу та візуалізації даних",
              version="0.1.0")

# Налаштування CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ініціалізація бази даних
init_db()

# Підключення маршрутів
app.include_router(datasets.router, prefix="/api/datasets", tags=["datasets"])
app.include_router(visualizations.router, prefix="/api/visualizations", tags=["visualizations"])
