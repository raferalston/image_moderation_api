from fastapi import FastAPI
from routers import moderate


app = FastAPI()

app.include_router(moderate.router)
