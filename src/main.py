
import logging
from fastapi import FastAPI
from src.api import extract, effectivepump   #import your routers

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI()

# Registering routers
app.include_router(extract.router, prefix="/extract")
app.include_router(effectivepump.router, prefix="/effectivepump")


#For Running the Application 
#uvicorn src.main:app --reload
