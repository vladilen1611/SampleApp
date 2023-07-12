import logging
from fastapi import FastAPI
from api.endpoints import router
import uvicorn

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("loging.log"),
        logging.StreamHandler()
    ]
)

app.include_router(router)

logger = logging.getLogger()


if __name__ == '__main__':
    logger.info("Run app with 8000 port")
    uvicorn.run(app, port=8000, log_level=logging.INFO)
