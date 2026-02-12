#  user - crud 

from fastapi import APIRouter , Depends , status
from sqlalchemy.orm import Session
from Businesslogic.auth import get_current_user 
from router.auth import require_role
from Businesslogic.task import create_task , update_task1 , get_task1 , delete_task
from database.db import get_db
from database.schema import task , update_task 


task_router = APIRouter()
@task_router.post("/create")
def create(task :task ,    user : dict = Depends(require_role(["user"])) , db:Session = Depends(get_db)):
  return create_task(task , user , db)

@task_router.put("/update/{id}")
def task_update(id: int , new_task : update_task, user: dict = Depends(require_role(["user"])), db : Session= Depends(get_db) ):
     return update_task1(id , new_task, user , db)
@task_router.get("/alltask") 
def get_task(user: dict = Depends(require_role(["user"])), db : Session= Depends(get_db)):
    return get_task1(user , db)
@task_router.delete("/delete/{id}")
def delete_task1(id : int ,user: dict = Depends(require_role(["user"])), db : Session= Depends(get_db)):
    return delete_task(id , user , db)
    