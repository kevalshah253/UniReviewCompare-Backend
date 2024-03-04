import uvicorn
from fastapi import FastAPI
from auth.router import router as auth_rauter
from utils.config import Config

print(Config.MONGO_URI)


app = FastAPI(docs_url="/docs",openapi_url="/docs/openapi.json")
app.include_router(auth_rauter,prefix= "/v1")

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True,host="127.0.0.1",port=8000)