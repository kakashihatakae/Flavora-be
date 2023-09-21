from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from Models import User, Orders, Items, Menus
from NewMenu import NewMenuController


# from Email.EmailController import EmailRouter

app = FastAPI()
app.include_router(router=NewMenuController.NewMenuRouter)


# change this to allow access frontent
origins = [
    "https://remail-ai-fe-d6c47adb68c1.herokuapp.com",
    "https://www.careersasha.com",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origin_regex="https://www.careersasha.com/*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(router=EmailRouter)

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
