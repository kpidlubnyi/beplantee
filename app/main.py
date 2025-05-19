from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import auth, plants, user_plants, password_reset, password_validation, faq, plant_types
from app.utils.init_defaults import init_default_images

default_images = init_default_images() 

app = FastAPI(
    title="BePlantee API",
    description="API for the BePlantee plant management application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(plants.router)
app.include_router(user_plants.router)
app.include_router(password_reset.router)
app.include_router(password_validation.router)
app.include_router(faq.router)
app.include_router(plant_types.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to BePlantee API"}
