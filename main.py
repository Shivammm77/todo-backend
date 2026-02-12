#  user can see his tasks  perform crud
# pagination , 
#  auth logic
from fastapi import FastAPI ,   Depends
from router.auth import auth , require_role
from router.task import task_router
from database.db import create_db , get_db
from database.model import User
from sqlalchemy.orm import Session
from Businesslogic.auth import get_current_user 
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_db() 
    yield
app = FastAPI(lifespan=lifespan)
app.add_middleware(  CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/working/{name}")
def work(name : str):
 return{"mesaage" : f"hii {name}"}

app.include_router(auth , prefix="/api/v1")
app.include_router(task_router , prefix="/api/v2/task")
@app.get("/profile")
def profile(
    current_user=Depends(get_current_user)
):
    return current_user
@app.get("/admin/getall")
def allusers(current_user:dict = Depends(require_role(["admin"])) , db : Session = Depends(get_db) ):
   if not current_user :
      return {"message" : "invalid"}
   return db.query(User).all()