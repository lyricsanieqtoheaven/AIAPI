from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pages.router import router as router_pages
from chat.router import router as router_chat

app = FastAPI(
    title="DL App"
)

app.include_router(router_pages)
app.include_router(router_chat)

origins = [
    "http://localhost:3000",
    "http://localhost:7333",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],  
)



