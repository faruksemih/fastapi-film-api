from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from film_api.database import create_db_tables
from film_api.routers.filmler import router as film_router
from film_api.routers.kullanicilar import router as kullanici_router
from film_api.routers.yonetmenler import router as yonetmen_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(lifespan=lifespan)

izin_verilen_adresler = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST","PUT",
                   "DELETE","PATCH","OPTIONS"
    ],
    allow_headers=["Authorization",
                   "Content-Type"
    ]
)

app.include_router(film_router)
app.include_router(yonetmen_router)
app.include_router(kullanici_router)


@app.get("/")
def root():
    return {"Hello": "film API calisiyor"}