import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.router import router as auth_router
from src.university.router import router as uni_router

# setup loggers
logging.config.fileConfig("src/logging.conf", disable_existing_loggers=False)



# get root logger
logger = logging.getLogger(
    __name__
)  # the __name__ resolve to "main" since we are at the root of the project.


app = FastAPI(docs_url="/docs", openapi_url="/docs/openapi.json")
app.include_router(auth_router, prefix="/v1")
app.include_router(uni_router, prefix="/v1")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)







