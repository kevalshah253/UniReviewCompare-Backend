import uvicorn
import logging
from fastapi import FastAPI
from auth.router import router as auth_router

# setup loggers
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(
    __name__
)  # the __name__ resolve to "main" since we are at the root of the project.


app = FastAPI(docs_url="/docs", openapi_url="/docs/openapi.json")
app.include_router(auth_router, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
